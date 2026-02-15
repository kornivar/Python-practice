import socket
import threading
import queue
import time

class CModel:
    def __init__(self, host, port, queue):
        self.host = host
        self.port = port
        self.client = None

        self.queue = queue

        self.running = False

    def receive(self):
        while self.running:
            try:
                data = self.client.recv(1024)

                if not data:
                    # logger.info("SERVER: Client disconnected: %s", addr)
                    break

                message = data.decode()
                self.queue.put(message)

                if data.decode() == "quit":
                    self.running = False
                    break

            except:
                # logger.info("SERVER: Client disconnected: %s", addr)
                break

        self.running = False

    def is_connected(self):
        if not self.connect_thread.is_alive():
            return True
        else:
            return False

    def send(self, message):
        if self.running:
            self.client.send(message.encode())
            # logger.info("SERVER: Message sent on %s:%s", HOST, PORT)
        else:
            return

        if message == "quit":
            self.running = False
            return

    def connect(self):
        while True:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(5)
                self.client.connect((self.host, self.port))
                self.client.settimeout(None)
                break

            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(1)

        self.receive_thread = threading.Thread(
            target=self.receive,
            daemon=True
        )
        self.receive_thread.start()

    def start(self):
        self.running = True

        self.connect_thread = threading.Thread(
            target=self.connect,
            daemon=True
        )
        self.connect_thread.start()

    def stop(self):
        self.running = False

        try:
            self.client.close()
        except:
            pass

        self.receive_thread.join()
        print("Thread closed")
