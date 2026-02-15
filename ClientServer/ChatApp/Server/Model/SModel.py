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
        if not self.accept_thread.is_alive():
            return True
        else:
            return False

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

        self.receive_thread = threading.Thread(
            target=self.receive,
            daemon=True
        )
        self.receive_thread.start()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.running = True

        self.accept_thread = threading.Thread(
            target=self.accept_client,
            daemon=True
        )
        self.accept_thread.start()

    def stop(self):
        self.running = False

        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.conn.close()
        except:
            pass

        try:
            self.server.close()
        except:
            pass

        self.receive_thread.join()
        print("Thread closed")
