import socket
import os
import select
import sys

FOLDER_PATH = 'server/dataset/'
BUFFER_SIZE = 1024
NOT_FOUND = 'File doesn\'t exist'
WRONG_CMD = 'Wrong command'
print('Server is starting')
server_address = (socket.gethostbyname(socket.gethostname()), 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
print('Server', server_socket.getsockname(),
      'Waiting for connection\n-----------')

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(
            input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                print(client_socket.getpeername(), '>> connected')

            else:
                data = sock.recv(BUFFER_SIZE).decode('utf-8')
                # print('>> ' + data)

                if data.startswith('unduh'):
                    command, filename = data.split(' ')
                    try:
                        os.path.exists(FOLDER_PATH + filename)

                        header = 'filename: ' + filename + '\nfilesize: ' + \
                            str(os.stat(FOLDER_PATH + filename).st_size) + '\n\n'
                        sock.send(header.encode())

                        with open(FOLDER_PATH + filename, 'rb') as f:
                            while True:
                                file_data = f.read(BUFFER_SIZE)
                                sock.send(file_data)
                                # print(len(file_data))
                                if not file_data:
                                    break

                        print(sock.getpeername(), '>> ' + filename + ' (' +
                              str(os.stat(FOLDER_PATH + filename).st_size)
                              + ' bytes) ' + 'sent successfully to')

                    except FileNotFoundError:
                        sock.send(NOT_FOUND.encode())

                elif data:
                    sock.send(WRONG_CMD.encode())

                else:
                    print(sock.getpeername(), '>> disconnected')
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
