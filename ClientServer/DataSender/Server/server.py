import socket
import os

HOST = '127.0.0.1'
PORT = 4000
FILE_PATH = 'test.txt'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server started at ' + HOST + ':' + str(PORT))

conn, addr = server.accept()
print('Connected by', addr)

filename = os.path.basename(FILE_PATH)
filesize = os.path.getsize(FILE_PATH)
conn.sendall(filename.encode() + b'\n')
conn.sendall(str(filesize).encode() + b'\n')

with open(FILE_PATH, 'rb') as f:
    while chunk := f.read(1024):
        conn.sendall(chunk)

print("File sent")

conn.close()
server.close()