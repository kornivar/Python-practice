import socket
import os
import json
import hashlib
import threading

# generates a random 128-bit number, which almost guarantied to be unique (3f8c5d7a-6c4e-4d61-9c32-7d0c4e2a9f0f)
import uuid

HOST = '127.0.0.1'
PORT = 4000
running = True
DB_FILE = "database.json"
AVATAR_DIR = "avatars"
receive_thread = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Server started at ' + HOST + ':' + str(PORT))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_db():
    if not os.path.exists(DB_FILE):
        db = {
            "users": {}
        }

        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)

        return db

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)


def handle_client(conn):
    buffer = ""

    while True:
        try:
            data = conn.recv(1024)

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
                        conn.close()
                        return

                    print("message:", p_data)

                elif p_type == "login":
                    print("login:", p_data)
                    login(conn, p_data["username"], p_data["password"])

                elif p_type == "signup":
                    print("signup:", p_data)
                    signup(conn, p_data["username"], p_data["password"])

                elif p_type == "avatar":
                    print("avatar:", p_data)
                    username = p_data["username"]
                    filename = p_data["filename"]
                    size = p_data["size"]

                    receive_avatar(conn, username, filename, size)

        except:
            break

    conn.close()


def receive_avatar(conn, username, filename, size):
    ext = filename.split(".")[-1]
    unique_name = str(uuid.uuid4()) + "." + ext

    path = os.path.join(AVATAR_DIR, unique_name)

    received = 0

    with open(path, "wb") as f:
        while received < size:

            chunk = conn.recv(min(4096, size - received))

            if not chunk:
                break

            f.write(chunk)
            received += len(chunk)

    set_avatar(username, path)


def set_avatar(username, path):
    db = load_db()

    db["users"][username]["avatar"] = path
    save_db(db)


def verification(conn, status):
    global running
    if running:
        temp_packet = {
            "type": "response",
            "data": status
        }
        packet = json.dumps(temp_packet)
        conn.sendall((packet + '\n').encode())


def login(conn, username, password):
    db = load_db()

    if username not in db["users"]:
        verification(conn, False)
        return

    hashed = hash_password(password)

    if db["users"][username]["password"] == hashed:
        verification(conn, True)
        return

    verification(conn, False)


def signup(conn, username, password):
    db = load_db()

    if username in db["users"]:
        verification(conn, False)
        return

    hashed = hash_password(password)

    db["users"][username] = {
        "password": hashed,
        "avatar": None
    }

    save_db(db)

    verification(conn, True)


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

def start():
    global running

    running = True

    while running:
        conn, addr = server.accept()
        print("Connected:", addr)

        thread = threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        )

        thread.start()

load_db()
start()
