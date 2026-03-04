import socket
import threading
import time
import queue
import json

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

            except:
                break

        self.running = False


    def send(self, message, type_id=None):
        if not self.running:
            return

        if type_id is None or type_id == "message":
            self.msg_to_server(message)
        elif type_id == "sign in":
            self.log_in(message)
        elif type_id == "sign up":
            self.sign_up(message)

        if message == "stop":
            self.running = False


    def msg_to_server(self, message):
        if self.running:
            self.client.send(message.encode())
        else:
            return

        if message == "stop":
            self.running = False
            return


    def log_in(self, password):
        if self.running:
            self.client.send(password.encode())
        else:
            return


    def sign_up(self, password):
        if self.running:
            self.client.send(password.encode())
        else:
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
