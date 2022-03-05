import socket
import os
import select
import sys

PATH = 'server/dataset/'
BUFFER_SIZE = 1024
NOT_FOUND = 'File doesn\'t exist'
WRONG_CMD = 'Wrong command'
server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(
            input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else:
                data = sock.recv(BUFFER_SIZE).decode('utf-8')
                print('>> ' + data)

                if data == 'exit':
                    sock.close()
                    input_socket.remove(sock)

                if data.startswith('unduh'):
                    command, filename = data.split(' ')
                    try:
                        os.path.exists(PATH + filename)

                        header = 'filename: ' + filename + '\nfilesize: ' + \
                            str(os.stat(PATH + filename).st_size) + '\n\n'
                        sock.send(header.encode())

                        with open(PATH + filename, 'rb') as f:
                            while True:
                                file_data = f.read(BUFFER_SIZE)
                                if not file_data:
                                    break
                                sock.send(file_data)

                    except FileExistsError:
                        sock.send(NOT_FOUND.encode())

                else:
                    sock.send(WRONG_CMD.encode())

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
