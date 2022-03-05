import socket
import sys

FOLDER_PATH = 'client/'
BUFFER_SIZE = 1024
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        command = str(input('Input command: '))
        client_socket.send(command.strip('\n').encode())
        received = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        # print('>> ' + received)
        x = received.split('\n')
        x, filename = x[0].split(': ')
        print('>> ' + filename)

        with open(FOLDER_PATH + filename, 'wb') as f:
            file_data = client_socket.recv(BUFFER_SIZE)
            if not file_data:
                break
            f.write(file_data)

        print('>> success')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
