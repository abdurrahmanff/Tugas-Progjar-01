# import os
# import sys

# path = 'server/dataset/'
# filename = input('Input filename: ')

# try:
#     with open(path + filename, 'rb') as f:
#         data = f.read()

#     header = 'filename: ' + filename + '\nfilesize: ' + \
#         str(os.stat(path+filename).st_size)
#     print(header)

#     # print(data)
# except FileNotFoundError:
#     print('File not found')

import socket


print(socket.gethostbyname(socket.gethostname()))
