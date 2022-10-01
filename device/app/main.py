from utime import sleep

from utils import WindSensor, DHT22Sensor
from sim868 import SIM868


sleep(10)


SIM868_PWR_EN = 14
SIM868_UART_ID = 0
SIM868_UART_BAUDERATE = 115200
APN = 'plus'
WIND_SENSOR_PIN = 27
DHT22_PIN = 28
API_URL = 'https://us-central1-weather-stations-w1.cloudfunctions.net/app/api/weather'


def main():

    print('SIM868 initialization...')
    sim868 = SIM868(SIM868_UART_ID, SIM868_UART_BAUDERATE, SIM868_PWR_EN)
    status = sim868.initialize(APN)
    print(status)
    status = sim868.bearer_config(APN)
    print(status)

    print('Wind sensor initialization...')
    wind_sensor = WindSensor(WIND_SENSOR_PIN)
    wind_sensor.initialize()

    print('DHT22 sensor initialization...')
    dht22 = DHT22Sensor(DHT22_PIN)

    print('Reading wind...')
    wind = wind_sensor.read()

    print('Reading temperature and humidity...')
    dht22.measure()
    temp = dht22.read_temperature()
    hum = dht22.read_humidity()

    data = {
        'wind': "{:.1f}".format(wind),
        'humidity': "{:.0f}".format(hum),
        'temperature': "{:.1f}".format(temp),
    }

    print('Data:', data)

    print('Sending data...')
    result = sim868.http_post(url=API_URL, data=data)
    print(result)

    print('Done')


main()


# import utime
# from sim868 import SIM868

# utime.sleep(10)

# SIM868_PWR_EN = 14
# SIM868_UART_ID = 0
# SIM868_UART_BAUDERATE = 115200
# APN = 'plus'
# sim868 = SIM868(SIM868_UART_ID, SIM868_UART_BAUDERATE, SIM868_PWR_EN)
# status = sim868.initialize(APN)
# utime.sleep(10)
# print(status)
# status = sim868.bearer_config(APN)
# utime.sleep(10)
# print(status)
# status = sim868.http_post(url='http://weather-stations-w1.web.app/api/weather', data={'humidity': '10%', 'temperature': '21.9', 'wind': '1.1'})
# print(status)


# import time

# from state_machine import StateMachine, State


# class Settings:
#     MEASUREMENT_INTERVAL = 10
#     


# class InitializationState(State):
#     name = 'InitializationState'

#     def run(self, sm):
#         print('InitializationState')

#     def error(self):
#         pass

#     def update(self, sm):
#         sm.go_to_state(MeasurementState.name)


# class WaitingState(State):
#     name = 'WaitingState'

#     def run(self, sm):
#         print('WaitingState')
#         time.sleep(2)  

#     def error(self):
#         pass

#     def update(self, sm):
#         sm.go_to_state(MeasurementState.name)


# class MeasurementState(State):
#     name = 'MeasurementState'

#     def run(self, sm):
#         print('MeasurementState')

#         start = time.ticks_ms()
#         delta = time.ticks_diff(time.ticks_ms(), start)

#     def error(self):
#         pass

#     def update(self, sm):
#         sm.go_to_state(WaitingState.name)


# sm = StateMachine()
# sm.add_state(InitializationState())
# sm.add_state(MeasurementState())
# sm.add_state(WaitingState())


# sm.go_to_state(InitializationState.name)

# #while True:
# for _ in range(8):
#     sm.update()

