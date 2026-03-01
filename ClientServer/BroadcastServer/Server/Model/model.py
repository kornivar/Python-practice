import socket
import threading
from Model.ClientData import ClientData

class Model:
    def __init__(self, host, port, queue):
        self.host = host
        self.port = port
        self.queue = queue
        self.server = None

        self.clients = {}
        self.client_counter = 0

        self.running = False


    def handle_client(self, client: ClientData):
        try:
            while self.running:
                data = client.conn.recv(1024)
                if not data:
                    break

                message = data.decode()
                self.queue.put((client.id, message))

                if message == "stop":
                    self.running = False
        except:
            pass
        finally:
            client.conn.close()
            if client.id in self.clients:
                del self.clients[client.id]


    def accept_clients(self):
        while self.running:
            conn, addr = self.server.accept()

            self.client_counter += 1
            client_id = self.client_counter

            client = ClientData(conn, addr, client_id)
            self.clients[client_id] = client

            thread = threading.Thread(
                target=self.handle_client,
                args=(client,)
            )
            thread.start()


    def is_connected(self):
        return bool(self.clients)


    def send(self, message, target_id=None):
        if not self.running:
            return

        if target_id is None or target_id == "all":
            self.broadcast(message)
        else:
            self.send_to_client(target_id, message)

        if message == "quit":
            self.running = False


    def send_to_client(self, client_id, message):
        client = self.clients.get(client_id)
        if not client:
            return

        try:
            client.conn.sendall(message.encode())
        except:
            print("Error sending private message")


    def broadcast(self, message):
        data = message.encode()

        for client in list(self.clients.values()):
            try:
                client.conn.sendall(data)
            except:
                print("Error sending message")

        if message == "stop":
            self.running = False


    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.running = True

        self.accept_thread = threading.Thread(
            target=self.accept_clients,
            daemon=False
        )
        self.accept_thread.start()


    def stop(self):
        self.running = False

        for client  in self.clients.values():
            try:
                client.conn.close()
            except:
                print("Error closing connection with client")
                pass

        try:
            self.server.close()
        except:
            print("Error closing server")
            pass

        self.clients.clear()
        self.accept_thread.join()
        self.handle_thread.join()
        print("Threads closed")