import os
import socket
import sys

FOLDER_PATH = 'server/dataset/'
BUFFER_SIZE = 1024
NOT_FOUND = 'File doesn\'t exist'
WRONG_CMD = 'Wrong command'
print('Server is starting')
# define server address, create socket, bind, and listen
server_address = (socket.gethostbyname(socket.gethostname()), 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print('Server (20.212.58.178) Waiting for connection\n-----------------')

# infinite loop accepting client
try:
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(client_socket.getpeername(), '>> connected')

            while True:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                print(client_socket.getpeername(), '>> ' + data)

                if data.startswith('unduh'):
                    command, filename = data.split(' ')
                    try:
                        os.path.exists(FOLDER_PATH + filename)

                        header = 'filename: ' + filename + '\nfilesize: ' + \
                            str(os.stat(FOLDER_PATH + filename).st_size) + '\n\n'
                        client_socket.send(header.encode())
                        client_socket.recv(1)

                        with open(FOLDER_PATH + filename, 'rb') as f:
                            while True:
                                file_data = f.read(BUFFER_SIZE)
                                # print(len(file_data))
                                if not file_data:
                                    break
                                client_socket.send(file_data)
                                client_socket.recv(1)

                        print(client_socket.getpeername(), '>> ' + filename + ' (' +
                              str(os.stat(FOLDER_PATH + filename).st_size)
                              + ' bytes) ' + 'sent successfully')

                    except FileNotFoundError:
                        client_socket.send(NOT_FOUND.encode())
                        client_socket.recv(1)

                elif data:
                    client_socket.send(WRONG_CMD.encode())
                    client_socket.recv(1)

                else:
                    print(client_socket.getpeername(), '>> disconnected')
                    client_socket.close()
                    break
        except ConnectionResetError:
            continue

# if user press ctrl + c, close socket client and exit
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
