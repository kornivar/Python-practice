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
        self.verified = False

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


    def send(self, message):
        if not self.running:
            return

        self.msg_to_server(message)

        if message == "stop":
            self.running = False


    def verification(self, username, password, action):
        if self.running:
            if action == "login":
                self.log_in(username, password)
            elif action == "signup":
                self.sign_up(username, password)


    def msg_to_server(self, message):
        if self.running:
            self.client.send(message.encode())
        else:
            return

        if message == "stop":
            self.running = False
            return


    def log_in(self, username, password):
        if self.running:
            self.client.send(password.encode())
        else:
            return


    def sign_up(self, username, password):
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
