from View.SView import SView

class SController:
    def __init__(self, smodel, queue):
        self.smodel = smodel
        self.queue = queue

        self.sview = SView(self)

    def poll_queue(self):
        while not self.queue.empty():
            message = self.queue.get()
            self.sview.show_client_message(message)

        self.sview.root.after(100, self.poll_queue)

    def to_stop_or_not_to_stop(self):
        if self.smodel.running == False:
            self.smodel.stop()

        self.sview.root.after(100, self.to_stop_or_not_to_stop)

    def send_message(self, message):
        self.smodel.send(message)

    def show_message(self, message):
        self.sview.show_client_message(message)


    def start(self):
        self.smodel.start()
        self.to_stop_or_not_to_stop()
        self.poll_queue()
        self.sview.start()
