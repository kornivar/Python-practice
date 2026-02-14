import socket
import threading
import queue

class SModel:
    def __init__(self, host, port, queue):
        self.host = host
        self.port = port
        self.server = None

        self.queue = queue

        self.running = False

    def receive(self):
        while self.running:
            try:
                data = self.conn.recv(1024)

                if not data:
                    # logger.info("SERVER: Client disconnected: %s", addr)
                    break

                if data.decode() == "quit":
                    self.running = False
                    break

                message = data.decode()
                self.queue.put(message)
            except:
                # logger.info("SERVER: Client disconnected: %s", addr)
                break

        self.running = False

    def send(self, message):
        if self.running:
            self.conn.send(message.encode())
            # logger.info("SERVER: Message sent on %s:%s", HOST, PORT)
        else:
            return

        if message == "quit":
            self.running = False
            return

    def accept_client(self):
        self.conn, self.addr = self.server.accept()
        # logger.info("SERVER: Client connected: %s", addr)
        threading.Thread(target=self.receive, daemon=True).start()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.running = True

        threading.Thread(target=self.accept_client, daemon=True).start()

    def stop(self):
        self.running = False
        self.t1.join()
        self.conn.close()
        self.server.close()
