import os
import socket
import json 
import ssl



def show_request(header, body):
    print('#' * 30)
    print(header, end='')
    print(body, end='')
    print('#' * 30)


host = 'us-central1-weather-stations-w1.cloudfunctions.net'

port = '80'
url_path = '/app/api/weather'


body = json.dumps({'humidity': '10%', 'temperature': '21.9', 'wind': '1.1'})

content_length = str(len(body))

header = \
    f'POST {url_path} HTTP/1.1\r\n' \
    f'Host: {host}:{port}\r\n' \
    f'Content-Length: {content_length}\r\n' \
    f'Content-Type: application/json\r\n' \
    f'\r\n'


show_request(header, body)

context = ssl.create_default_context()
with socket.create_connection((host, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
        print(ssock.version())

        request = header.encode('utf-8') + body.encode('utf-8')
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # ssock.connect((host, int(port)))
        ssock.send(request)
        response = ssock.recv(4096)
        ssock.close()
        print(response.decode())

