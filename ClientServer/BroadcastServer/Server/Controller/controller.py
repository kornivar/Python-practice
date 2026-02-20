from View.view import View

class Controller:
    def __init__(self, model):
        self.model = model

        self.view = View(self)

    def to_stop_or_not_to_stop(self):
        if self.model.running == False:
            self.view.disable_button()
            self.view.show_info("stop used, disconnecting")
            self.model.stop()
            return

        self.view.root.after(1500, self.to_stop_or_not_to_stop)

    def send_message(self, message):
        self.model.send(message)

    def show_message(self, message):
        self.view.show_client_message(message)

    def is_connected(self):
        if self.model.is_connected() == True:
            self.show_info("client connected")
            self.view.enable_button()
            return
        else:
            self.view.disable_button()

        self.view.root.after(1000, self.is_connected)

    def show_info(self, message):
        self.view.show_info(message)

    def start(self):
        self.model.start()
        self.is_connected()
        self.to_stop_or_not_to_stop()
        self.view.start()