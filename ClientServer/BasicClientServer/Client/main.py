import socket
import logging

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    handlers=[logging.FileHandler("client.log", mode="a", encoding="utf-8"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

HOST = '127.0.0.1'
PORT = 4000


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
logger.info("CLIENT: connected to server on %s:%s", HOST, PORT)

while True:
    msg = input("Enter your message (type OK to exit): ")
    client.send(msg.encode())
    logger.info("CLIENT: Message sent on %s:%s", HOST, PORT)

    if msg == "OK":
        logger.info("CLIENT: Received OK, shutting down")
        break

client.close()
logger.info("CLIENT: Client closed")