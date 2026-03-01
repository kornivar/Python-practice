import socket
import threading
import time
import queue

class Model:
    def __init__(self, ip, port, queue):
        self.ip = ip
        self.port = port
        self.queue = queue

        self.running = False


    def receive(self):
        while self.running:
            try:
                data = self.client.recv(1024)

                if not data:
                    break

                message = data.decode()
                self.queue.put(message)

                if data.decode() == "stop":
                    self.running = False
                    break

            except:
                break

        self.running = False

    def send(self, message):
        if self.running:
            self.client.send(message.encode())
        else:
            return

        if message == "quit":
            self.running = False
            return


    def is_connected(self):
        if not self.connect_thread.is_alive():
            return True
        else:
            return False


    def connect(self):
        while True:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(5)
                self.client.connect((self.ip, self.port))
                self.client.settimeout(None)
                break

            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(1)

        self.receive_thread = threading.Thread(
            target=self.receive,
            daemon=False
        )
        self.receive_thread.start()


    def start(self):
        self.running = True

        self.connect_thread = threading.Thread(
            target=self.connect,
            daemon=False
        )
        self.connect_thread.start()


    def stop(self):
        self.running = False

        try:
            self.client.close()
        except:
            pass

        self.receive_thread.join()
        print(f"Client stopped")
