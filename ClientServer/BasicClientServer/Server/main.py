import socket
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    handlers=[logging.FileHandler("server.log", mode="a", encoding="utf-8"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

HOST = '127.0.0.1'
PORT = 4000


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

logger.info("SERVER: Started on %s:%s", HOST, PORT)

conn, addr = server.accept()
logger.info("SERVER: Client connected: %s", addr)

while True:
    data = conn.recv(1024)
    msg = data.decode()

    if msg == "OK":
        logger.info("SERVER: Received OK, shutting down")
        break

    try:
        result = eval(msg)
        logger.info("SERVER: Eval success: %s = %s", msg, result)
        print(msg+" =", result)
    except Exception as e:
        print("Error:", e)
        logger.error("SERVER: Eval error for '%s': %s", msg, e)


conn.close()
server.close()
logger.info("SERVER: Server closed")