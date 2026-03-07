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
        buffer = ""

        while self.running:
            try:
                data = self.client.recv(1024)

                if not data:
                    break

                buffer += data.decode()

                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)

                    packet = json.loads(message)

                    p_type = packet["type"]
                    p_data = packet["data"]

                    if p_type == "message":
                        self.queue.put(p_data)

                    elif p_type == "response":
                        pass

                    elif p_type == "stop":
                        self.running = False
            except:
                break

        self.running = False

    def send(self, message):
        if not self.running:
            return

        packet = json.dumps(message)

        self.msg_to_server(self.to_packet(packet))

        if message == "stop":
            self.running = False

    @staticmethod
    def to_packet(packet, p_type ="message"):
        if  p_type == "request":
            packet = {
                "type": "request",
                "data": packet
            }
            return json.dumps(packet)
        elif  p_type == "message":
            packet = {
                "type": "message",
                "data": packet
            }
            return json.dumps(packet)

        return None

    def verification(self, login, password, action):

        packet = self.to_packet(login, password, action)

        if self.running:
            if action == "login":
                self.log_in(packet)
            elif action == "signup":
                self.sign_up(packet)


    def msg_to_server(self, packet):
        if self.running:
            self.client.send((packet + '\n').encode())
        else:
            return


    def log_in(self, packet):
        if self.running:
            self.client.send((packet + '\n').encode())
        else:
            return


    def sign_up(self, packet):
        if self.running:
            self.client.send((packet + '\n').encode())
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
