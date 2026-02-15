# import socket
# import logging
# import threading

# logging.basicConfig(
#     level=logging.INFO,
#     format="{asctime} - {levelname} - {name} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M",
#     handlers=[logging.FileHandler("server.log", mode="a", encoding="utf-8")]
# )
#
# logger = logging.getLogger(__name__)

import queue

from Model.SModel import  SModel
from Controller.SController import SController

HOST = '127.0.0.1'
PORT = 4000
queue = queue.Queue()

smodel = SModel(HOST, PORT, queue)
scontroller = SController(smodel, queue)
scontroller.start()


# HOST = '127.0.0.1'
# PORT = 4000
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen()
#
# logger.info("SERVER: Started on %s:%s", HOST, PORT)
#
# conn, addr = server.accept()
# logger.info("SERVER: Client connected: %s", addr)
#
# running = True
#
# print("TYPE OK TO EXIT")
#
# def receive():
#     global running
#
#     while running:
#         try:
#             data = conn.recv(1024)
#
#             if not data:
#                 logger.info("SERVER: Client disconnected: %s", addr)
#                 break
#
#             logger.info("SERVER: Message received on %s:%s", HOST, PORT)
#             print("\nClient:", data.decode())
#
#         except:
#             logger.info("SERVER: Client disconnected: %s", addr)
#             break
#
#     running = False
#
# def send():
#     global running
#
#     while running:
#         msg = input()
#         conn.send(msg.encode())
#         logger.info("SERVER: Message sent on %s:%s", HOST, PORT)
#
#         if msg == "OK":
#             logger.info("SERVER: Resieved OK %s:%s", HOST, PORT)
#             running = False
#             break
#
# t1 = threading.Thread(target=receive)
# t2 = threading.Thread(target=send)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# logger.info("SERVER: Shutting down server on %s:%s", HOST, PORT)
# conn.close()
# server.close()
