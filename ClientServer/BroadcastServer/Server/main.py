from Model.model import Model
from Controller.controller import Controller
import queue

HOST = '127.0.0.1'
PORT = 4000

queue = queue.Queue()

model = Model(HOST, PORT, queue)
controller = Controller(model, queue)
controller.start()