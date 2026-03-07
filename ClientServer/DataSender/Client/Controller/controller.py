from Client.View.view import View
from Client.View.login_window import LoginWindow

class Controller:
    def __init__(self, model, queue):
        self.model = model
        self.queue = queue
        self.login_window = LoginWindow(self)

        self.view = View(self)
        self.flag = False


    def poll_queue(self):
        while not self.queue.empty():
            message = self.queue.get()
            self.view.show_server_message(message)

        self.view.root.after(100, self.poll_queue)


    def to_stop_or_not_to_stop(self):
        if not self.model.running:
            self.view.show_info("stop used, disconnecting")
            self.model.stop()
            self.view.root.destroy()
            return

        self.view.root.after(1500, self.to_stop_or_not_to_stop)


    def send_message(self, message, selected = None):
        if selected is None or selected == "message":
            self.model.send(message, type_id="message")


    def show_message(self, message):
        self.view.show_server_message(message)


    def is_connected(self):
        if self.model.is_connected():
            self.view.show_connection("connected to server")
            self.login_window.enable_button()
            self.poll_queue()
            return
        elif not self.flag:
            self.flag = True
            self.login_window.disable_button()
            self.view.show_connection("not connected")

        self.view.root.after(1000, self.is_connected)


    def verification(self, login, password, action):
        result = self.model.verification(login, password, action)
        if result:
            return True

        return False

    def check_verification(self):
        if self.model.verified:
            self.to_stop_or_not_to_stop()
            self.view.start()
            return

    def show_info(self, message):
        self.view.show_info(message)


    def start(self):
        self.model.start()
        self.is_connected()
        self.login_window.start()

        self.check_verification()
