

class Settings:
    LOGGING_FORMAT = '|<time:20>|<logger:36>|<level:8>|<message>'
    WAITING_TIME = 10
    SIM868_PWR_EN = 14
    SIM868_UART_ID = 0
    SIM868_UART_BAUDERATE = 115200
    SIM868_SUCCESS_RESPONSE = 'New weather data'
    APN = 'plus'
    WIND_SENSOR_PIN = 27
    DHT22_PIN = 28
    API_URL = 'https://us-central1-weather-stations-w1.cloudfunctions.net/app/api/weather'


settings = Settings()
