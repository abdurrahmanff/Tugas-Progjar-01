from math import ceil
import os
import socket
import sys

FOLDER_PATH = 'client/download/'
BUFFER_SIZE = 1024
hostname = str(input('Insert server address: '))
# hostname = '127.0.0.4'
server_address = (hostname, 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print('Connected. Press \'ctrl + c\' to stop')

try:
    while True:
        command = str(input('Input command: '))
        client_socket.send(command.strip('\n').encode())
        received = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        # print('>> ' + received)
        if received.startswith('filename'):
            z = received.split('\n')
            x, filename = z[0].split(': ')
            y, filesize = z[1].split(': ')
            # print('>> ' + filename + ' (' + filesize + ' bytes)')
            n = ceil(int(filesize)/BUFFER_SIZE)

            with open(FOLDER_PATH + filename, 'wb') as f:
                while n:
                    file_data = client_socket.recv(BUFFER_SIZE)
                    f.write(file_data)
                    # print(len(file_data))
                    if not file_data:
                        # print('Kelar\n')
                        break
                    n -= 1

            print('>> ' + filename + ' (' +
                  str(os.stat(FOLDER_PATH + filename).st_size)
                  + ' bytes) ' + 'received successfully')

        else:
            print('>> Wrong command. Try "unduh [filename].[extension]"')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
