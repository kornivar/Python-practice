import socket
import threading
import time

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.running = False


    def receive(self):
        while self.running:
            try:
                data = self.client.recv(1024)

                if not data:
                    break

                message = data.decode()
                print(f"Message from server: {message}")

                if data.decode() == "quit":
                    self.running = False
                    break

            except:
                break

        self.running = False


    def connect(self):
        while True:
            try:
                print("Connecting to server...")
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(5)
                self.client.connect((self.ip, self.port))
                self.client.settimeout(None)
                break

            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(1)

        print("Connection established")
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


IP = '127.0.0.1'
PORT = 4000
Client = Client(IP, PORT)
Client.start()