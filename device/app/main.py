from utime import sleep

from state_machine import StateMachine, State
from logger import set_logger, stdout_log
from settings import settings
from utils import WindSensor, DHT22Sensor
from sim868 import SIM868


class InitializationState(State):
    name = 'InitializationState'

    def __init__(self):
        self._logger = set_logger('main.' + self.name, dest=stdout_log(), loglevel=0, format=settings.LOGGING_FORMAT)

    def run(self, sm):

        self._logger.info('SIM868 initialization...')
        sim868 = SIM868(settings.SIM868_UART_ID, settings.SIM868_UART_BAUDERATE, settings.SIM868_PWR_EN)
        status = sim868.initialize(settings.APN)

        self._logger.info('Wind sensor initialization...')
        wind_sensor = WindSensor(settings.WIND_SENSOR_PIN)
        wind_sensor.initialize()

        self._logger.info('DHT22 sensor initialization...')
        dht22 = DHT22Sensor(settings.DHT22_PIN)

        resources = {
            'sim868': {
                'instance': sim868,
            },
            'wind_sensor': {
                'instance': wind_sensor,
            },
            'dht22': {
                'instance': dht22,
            },
        }
        sm.context['resources'] = resources

    def error(self):
        pass

    def update(self, sm):
        sm.go_to_state(MeasurementState.name)


class WaitingState(State):
    name = 'WaitingState'

    def __init__(self):
        self._logger = set_logger('main.' + self.name, dest=stdout_log(), loglevel=0, format=settings.LOGGING_FORMAT)

    def run(self, sm):
        self._logger.info('Waiting...')
        sleep(settings.WAITING_TIME)

    def error(self):
        pass

    def update(self, sm):
        sm.go_to_state(MeasurementState.name)


class MeasurementState(State):
    name = 'MeasurementState'

    def __init__(self):
        self._logger = set_logger('main.' + self.name, dest=stdout_log(), loglevel=0, format=settings.LOGGING_FORMAT)

    def run(self, sm):

        wind_sensor = sm.context['resources']['wind_sensor']['instance']
        dht22 = sm.context['resources']['dht22']['instance']

        self._logger.info('Wind measurement')
        wind = wind_sensor.read()

        self._logger.info('Temperature measurement')
        temp = dht22.read_temperature()

        self._logger.info('Humidity measurement')
        hum = dht22.read_humidity()

        measurements = {
            'wind': "{:.1f}".format(wind),
            'humidity': "{:.0f}".format(hum),
            'temperature': "{:.1f}".format(temp),
        }
        sm.context['measurements'] = measurements
        self._logger.info('Measured data: {}'.format([k + ' = ' + v for k, v in measurements.items()]))

    def error(self):
        pass

    def update(self, sm):
        sm.go_to_state(SendingDataState.name)


class SendingDataState(State):
    name = 'SendingDataState'

    def __init__(self):
        self._logger = set_logger('main.' + self.name, dest=stdout_log(), loglevel=0, format=settings.LOGGING_FORMAT)

    def run(self, sm):
        self._logger.info('Sending data...')
        sim868 = sm.context['resources']['sim868']['instance']
        data = sm.context['measurements']
        status = sim868.http_post(url=settings.API_URL, data=data)

        print(status)

    def error(self):
        pass

    def update(self, sm):
        sm.go_to_state(WaitingState.name)


def wait_before_sturtup(time=10):
    sleep(time)


def main():
    sm = StateMachine()
    sm.add_state(InitializationState())
    sm.add_state(WaitingState())
    sm.add_state(MeasurementState())
    sm.add_state(SendingDataState())

    sm.go_to_state(InitializationState.name)

    #while True:
    for _ in range(4):
        sm.update()


wait_before_sturtup()
main()
