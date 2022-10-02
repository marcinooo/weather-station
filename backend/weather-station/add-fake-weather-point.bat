@echo off

echo Sending request...

curl -X POST ^
    -H "Content-Type: application/json" ^
    -d "{\"humidity\": \"68\", \"temperature\": \"27.2\", \"wind\": \"2.2\"}" ^
    "https://us-central1-weather-stations-w1.cloudfunctions.net/app/api/weather"
