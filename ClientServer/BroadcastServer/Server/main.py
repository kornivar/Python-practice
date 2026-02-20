from Model.model import Model
from Controller.controller import Controller

HOST = '127.0.0.1'
PORT = 4000

model = Model(HOST, PORT)
controller = Controller(model)
controller.start()