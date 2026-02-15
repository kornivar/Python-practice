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
            self.sview.disable_button()
            self.sview.show_info("quit used, disconnecting")
            self.smodel.stop()

        self.sview.root.after(1000, self.to_stop_or_not_to_stop)

    def send_message(self, message):
        self.smodel.send(message)

    def show_message(self, message):
        self.sview.show_client_message(message)

    def is_connected(self):
        if self.smodel.is_connected() == True:
            self.show_info("client connected")
            self.sview.enable_button()
            self.poll_queue()
            return
        else:
            self.sview.disable_button()

        self.after_id = self.sview.root.after(1000, self.is_connected)

    def show_info(self, message):
        self.sview.show_info(message)

    def start(self):
        self.smodel.start()
        self.is_connected()
        self.to_stop_or_not_to_stop()
        self.sview.start()
