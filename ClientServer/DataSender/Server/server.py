import socket
import os
import json

HOST = '127.0.0.1'
PORT = 4000
FILE_PATH = 'test.txt'
running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server started at ' + HOST + ':' + str(PORT))

conn, addr = server.accept()
print('Connected by', addr)

def receive():
    buffer = ""
    global running

    while running:
        try:
            data = conn.recv(1024)
            print(f"Server received a message: {data}")

            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                packet = json.loads(message)

                p_type = packet["type"]
                p_data = packet["data"]

                if p_type == "message":
                    if p_data == "stop":
                        running = False
                    else:
                        pass
                        print(f"Server received a message: {p_data}")

                elif p_type == "login":
                    # login(p_data)
                    verification()
                    print(f"Server received a login request: {p_data}")
                elif p_type == "signup":
                    # signup(p_data)
                    verification()
                    print(f"Server received a signup request: {p_data}")
        except:
            break


def send(self, message):
    if not self.running:
        return

    packet = self.to_packet(message)

    self.conn.sendall((packet + '\n').encode())

    if message == "stop":
        self.running = False


def verification(status = True):
    global running
    if running:
        if status:
            temp_packet = {
                "type": "response",
                "data": True
            }
            packet = json.dumps(temp_packet)
            conn.sendall((packet + '\n').encode())
        elif not status:
            temp_packet = {
                "type": "response",
                "data": False
            }
            packet = json.dumps(temp_packet)
            conn.sendall((packet + '\n').encode())


def login(login_data):
    global running
    if running:
        pass


def signup(signup_data):
    global running
    if running:
        pass


def to_packet(data, d_type="message"):
    if d_type == "request":
        packet = {
            "type": "request",
            "data": data
        }
        return json.dumps(packet)
    elif d_type == "message":
        packet = {
            "type": "message",
            "data": data
        }
        return json.dumps(packet)

    return None

receive()

conn.close()
server.close()