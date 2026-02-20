import socket
import threading

class Model:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}

        self.running = False

    def broadcast(self, message):
        data = message.encode()

        for conn in list(self.clients.values()):
            try:
                conn.sendall(data)
            except:
                print("Error sending message")

        if message == "stop":
            self.running = False
            return

    def handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
        except:
            pass
        finally:
            conn.close()
            if addr in self.clients:
                del self.clients[addr]

    def accept_clients(self):
        while self.running:
            conn, addr = self.server.accept()
            self.clients[addr] = conn

            self.handle_thread = threading.Thread(
                target=self.handle_client,
                args=(conn, addr)
            )
            self.handle_thread.start()

    def is_connected(self):
        if self.clients != {}:
            return True
        else:
            return False

    def send(self, message):
        if self.running:
            self.broadcast(message)
        else:
            return

        if message == "quit":
            self.running = False
            return


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

        for conn in self.clients.values():
            try:
                conn.close()
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