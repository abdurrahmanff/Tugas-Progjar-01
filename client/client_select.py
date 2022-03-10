from math import ceil
from tqdm import tqdm
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
        client_socket.send(b'\x01')
        # print('>> ' + received)
        if received.startswith('filename'):
            z = received.split('\n')
            x, filename = z[0].split(': ')
            y, filesize = z[1].split(': ')
            # print('>> ' + filename + ' (' + filesize + ' bytes)')
            n = ceil(int(filesize)/BUFFER_SIZE)

            with open(FOLDER_PATH + filename, 'wb') as f:
                # temp = 0
                for i in tqdm(range(n)):
                    file_data = client_socket.recv(BUFFER_SIZE)
                    # client_socket.send(b'\x01')
                    # temp += len(file_data)
                    # print('progress ', len(file_data), ' | ', temp)
                    if not file_data:
                        # print('Kelar\n')
                        break
                    f.write(file_data)

            print('>> ' + filename + ' (' +
                  str(os.stat(FOLDER_PATH + filename).st_size)
                  + ' bytes) ' + 'received successfully')

        else:
            print('>> Wrong command. Try "unduh [filename].[extension]"')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
