"""
Raspberry Pi Pico (MicroPython) exercise:
work with SIM868 GSM/GPRS/GNSS Module
"""
import machine
import os
import utime
import binascii
import ujson


class ActionStatus:
    def __init__(self, status, message) -> None:
        self.status = status
        self.message = message

    def __str__(self):
        status = 'FAIL' if self.status else 'PASS'
        return status + ': ' + self.message

    def __bool__(self):
        return not self.status


class SIM868:
    """Creates object to control SIM868 module."""

    def __init__(self, uart_id, uart_baudrate, pwr_en=14):
        self.uart = machine.UART(uart_id, uart_baudrate)
        self.pwr_en = machine.Pin(pwr_en, machine.Pin.OUT)

    def initialize(self, apn, timeout=25000):
        result = self.start_module(timeout=timeout)
        if result:
            result = self.start_network(apn)
            if result:
                return ActionStatus(0, 'SIM868 was initialized: {}'.format(result.message))
        return ActionStatus(1, 'SIM868 was not initialized: {}'.format(result.message))

    def start_module(self, timeout):
        prvmills = utime.ticks_ms()
        while (utime.ticks_ms() - prvmills) < timeout:
            self.uart.write(bytearray(b'ATE1\r\n'))
            utime.sleep(2)
            self.uart.write(bytearray(b'AT\r\n'))
            rec_temp = self.wait_resp_info()
            if 'OK' in rec_temp:
                return ActionStatus(0, 'SIM868 is ready ' + rec_temp)
            self.power_on_off()
            utime.sleep(8)
        return ActionStatus(1, 'SIM868 is not ready')

    def start_network(self, apn, trials=3):
        """
        Connects module to phone network.
        :param apn: access point
        :param trials: number of trials
        :return: tuple of status (status is 0 for success, otherwise 1)
            and information about network readiness
        """
        status = 0
        message = 'SIM868 is connected'
        for i in range(0, trials):
            response = self.send_at("AT+CGREG?", "0,1")
            if response:
                break
            if i == 3:
                status, message = 1, 'SIM868 is not connected: ' + response.message
            utime.sleep(5)
        if not status:
            commands = (
                ("AT+CPIN?", "OK"),
                ("AT+CSQ", "OK"),
                ("AT+COPS?", "OK"),
                ("AT+CGATT?", "OK"),
                ("AT+CGDCONT?", "OK"),
                ("AT+CSTT?", "OK"),
                ("AT+CSTT=\"{}\"".format(apn), "OK"),
                ("AT+CIICR", "OK", 4000),
                ("AT+CIFSR", "OK"),
            )
            response = self.send_set_of_at_commands(commands)
            if not response:
                status, message = 1, 'SIM868 is not connected: {}'.format(response.message)
        return ActionStatus(status, message)

    def bearer_config(self, apn):
        """
        Configures bearer.
        :param apn: access point
        :return: tuple of status (status is 0 for success, otherwise 1) and message (message contains reason of failure)
        """
        commands = (
            ('AT+SAPBR=3,1,"Contype","GPRS"', 'OK', 5000),
            ('AT+SAPBR=3,1,"APN","{}"'.format(apn), 'OK', 5000),
            ('AT+SAPBR=1,1', 'OK', 5000),
            ('AT+SAPBR=2,1', 'OK', 5000),
        )
        status = self.send_set_of_at_commands(commands)
        if not status:
            return ActionStatus(1, 'Bearer initialisation fialed: ' + status.message)
        return ActionStatus(0, 'Bearer initialized successfully')

    def http_post(self, url, data, headers=[]):
        """
        Sends http or https post request with json data.

        .. warning::
            Module SIM868 uses an older version of the TLS protocol. Some web servises do not support it, but
            it worked fine with the firebase service on 17.04.2022.

        :param url: url
        :param data: data to send
        :param headers: additional headers
        :return: tuple of status (status is 0 for success, otherwise 1)
            and message (message contains received data or reason of failure)
        """
        body = ujson.dumps(data)
        body_length = len(body)
        trials = 3
        
        for i in range(1, trials):
            response = self.send_at('AT+HTTPINIT', 'OK', 3500)
            if response:
                break
            if i == 3:
                return ActionStatus(1, 'HTTPS POST request initialisation failed: {}'.format(response.message))
            utime.sleep(5)
        commands = (
            ('AT+HTTPPARA=\"CID\",1', 'OK'),
            ('AT+HTTPPARA="URL","{}"'.format(url), 'OK'),
            ('AT+HTTPPARA="REDIR",1', 'OK'),
            ('AT+HTTPPARA="CONTENT","application/json"', 'OK'),
        )
        if headers:
            commands += self._parse_headers(headers)
        commands += (
            ('AT+HTTPSSL=1', 'OK'),
            ('AT+HTTPDATA={},15000'.format(body_length), 'DOWNLOAD', 4000),
        )
        response = self.send_set_of_at_commands(commands)
        if not response:
            _ = self.send_at('AT+HTTPTERM', 'OK')
            return ActionStatus(1, 'HTTPS POST request initialisation failed: {}'.format(response.message))
        self.uart.write(bytearray(body))
        _ = self.wait_resp_info()
        response = self.send_at('AT+HTTPACTION=1', 'OK', 84200)
        if not response:
            _ = self.send_at('AT+HTTPTERM', 'OK')
            return ActionStatus(1, "HTTPS POST request failed: {}".format(response.message))
        response = self.send_at('AT+HTTPREAD', 'OK', 25000)
        if not response:
            _ = self.send_at('AT+HTTPTERM', 'OK')
            return ActionStatus(1, "HTTPS POST request failed: {}".format(response.message))
        status, message = 0, response.message
        _ = self.send_at('AT+HTTPTERM', 'OK')
        return ActionStatus(status, message)

    def power_on_off(self):
        """
        Restarts module.
        :return: None
        """
        self.pwr_en.value(1)
        utime.sleep(2)
        self.pwr_en.value(0)
        utime.sleep(2)

    def wait_resp_info(self, timeout=2000):
        prvmills = utime.ticks_ms()
        info = b""
        while (utime.ticks_ms() - prvmills) < timeout:
            if self.uart.any():
                info = b"".join([info, self.uart.read(1)])
        return info.decode()

    def send_at(self, cmd, back, timeout=2000):
        """
        Sends single AT command to module.
        :param cmd: AT command
        :param back: required part of response
        :param timeout: response timeout in ms
        :return: tuple of status (status is 0 if required part of response is in response,
                                            1 if required part of response is not in response,
                                            2 if no response in given timeout,
                                            3 if response can not be decoded)
            and information about module readiness
        """
        rec_buff = b''
        self.uart.write((cmd+'\r\n').encode())
        prvmills = utime.ticks_ms()
        while (utime.ticks_ms() - prvmills) < timeout:
            if self.uart.any():
                rec_buff = b"".join([rec_buff, self.uart.read(1)])
        if rec_buff != b'':
            try:
                if back in rec_buff.decode():
                    return ActionStatus(0, rec_buff.decode())
                return ActionStatus(1, rec_buff.decode())
            except UnicodeError:
                return ActionStatus(3, 'Cannot decode response due to UnicodeError')
        return ActionStatus(2, 'No response for command {}'.format(cmd))

    def send_set_of_at_commands(self, commands):
        """
        Sends list of AT commands.
        :param commands: list of commands e.g.: (
            ('<command - required>', '<response - required, but it can be empty string>', <timeout - optional>))
        :return: status and message from 'self.send_at' method
        """
        status, message = 0, 'Commands successfully sent'
        commands = self._unify_set_of_at_commands(commands)
        for command, result, timeout in commands:
            response = self.send_at(command, result, timeout)
            if not response:
                return response
        return ActionStatus(status, message)

    @staticmethod
    def _unify_set_of_at_commands(commands):
        """
        Checks and unifies commands before sending to module. It appends default timeout for commands without timeout.
        :param commands: list of commands
        :return: unified commands
        """
        unified_commands = []
        for command in commands:
            unified_command = [command[0], command[1]]
            if len(command) == 2:
                unified_command.append(2000)
            elif len(command) == 3:
                unified_command.append(command[2])
            else:
                raise IndexError('Command should be list of two or three values.')
            unified_commands.append(unified_command)
        return unified_commands

    @staticmethod
    def _parse_headers(headers):
        """
        Parses user headers for http request.
        :param headers: list of headers
        :return: list of commands to set headers in module
        """
        if not isinstance(headers, list):
            raise ValueError("Headers should be list.")
        commands = ()
        for header in headers:
            commands += (('AT+HTTPPARA="USERDATA","{}"'.format(header), 'OK', 4000),)
        return commands
