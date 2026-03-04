# import socket
# import os

from Model.model import Model
from Controller.controller import Controller
import queue

IP = '127.0.0.1'
PORT = 4000

queue = queue.Queue()

model = Model(IP, PORT, queue)
controller = Controller(model, queue)
controller.start()

# IP = '127.0.0.1'
# PORT = 4000
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((IP, PORT))
# print("Connected to server")
#
# filename = b''
# while not filename.endswith(b'\n'):
#     filename += client.recv(1)
# filename = filename.strip().decode()
#
# filesize = b''
# while not filesize.endswith(b'\n'):
#     filesize += client.recv(1024)
# filesize = int(filesize.strip())
#
# with open(filename, 'wb') as f:
#     received = 0
#     while received < filesize:
#         chunk = client.recv(1024)
#         if not chunk:
#             break
#         f.write(chunk)
#         received += len(chunk)
#
# print("File received:", filename)
#
# client.close()