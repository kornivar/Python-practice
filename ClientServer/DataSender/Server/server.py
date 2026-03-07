import socket
import os
import json

HOST = '127.0.0.1'
PORT = 4000
FILE_PATH = 'test.txt'
running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server started at ' + HOST + ':' + str(PORT))

conn, addr = server.accept()
print('Connected by', addr)

data = conn.recv(1024)
message = data.decode().strip()
packet = json.loads(message)
print("Server received a packet: " + message)


conn.close()
server.close()