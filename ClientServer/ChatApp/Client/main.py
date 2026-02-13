import socket
import threading
import logging

logging.basicConfig(
    level=logging.WARNING,
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    handlers=[logging.FileHandler("client.log", mode="a", encoding="utf-8")]
)

logger = logging.getLogger(__name__)

HOST = '127.0.0.1'
PORT = 4000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
logger.info("CLIENT: Connected to server on %s:%s", HOST, PORT)

running = True

print("TYPE OK TO EXIT")

def receive():
    global running
    while running:
        try:
            data = client.recv(1024)
            if not data:
                logger.info("CLIENT: Server disconnected")
                break
            logger.info("CLIENT: Message received")
            print("\nServer:", data.decode())
        except:
            logger.info("CLIENT: Connection error")
            break
    running = False

def send():
    global running
    while running:
        msg = input()
        client.send(msg.encode())
        logger.info("CLIENT: Message sent")
        if msg == "OK":
            logger.info("CLIENT: Sent OK, stopping")
            running = False
            break

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)

t1.start()
t2.start()

t1.join()
t2.join()

logger.info("CLIENT: Closing connection")
client.close()