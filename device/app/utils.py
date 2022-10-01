from time import ticks_us, sleep
from machine import Pin
from dht import DHT22


class Counter:
    def __init__(self):
        self._ticks = 0

    def update(self):
        self._ticks += 1

    def clear(self):
        self._ticks = 0
    
    def get(self):
        return self._ticks


class WindSensor:
    def __init__(self, pin):
        self.pin = pin
        self._pin_obj = Pin(self.pin, Pin.IN, Pin.PULL_UP)
        self._counter = Counter()

    def initialize(self):
        self._pin_obj.irq(self._irq_callback, Pin.IRQ_FALLING)

    def _irq_callback(self, pin):
        self._counter.update()

    def read(self):
        self._counter.clear()
        start_ticks = self._counter.get()
        sleep(20)
        end_ticks = self._counter.get()
        ticks_per_second = (end_ticks - start_ticks) / 20
        return ticks_per_second

    
class DHT22Sensor:
    def __init__(self, pin):
        self.pin = pin
        self._sensor = DHT22(Pin(self.pin))

    def measure(self):
        self._sensor.measure()

    def read_temperature(self):
        return self._sensor.temperature()
    
    def read_humidity(self):
        return self._sensor.humidity()
