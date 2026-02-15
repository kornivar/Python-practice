from View.CView import CView

class CController:
    def __init__(self, model, queue):
        self.model = model
        self.queue = queue

        self.view = CView(self)
        self.flag = False

    def poll_queue(self):
        while not self.queue.empty():
            message = self.queue.get()
            self.view.show_server_message(message)

        self.view.root.after(100, self.poll_queue)

    def to_stop_or_not_to_stop(self):
        if self.model.running == False:
            self.view.disable_button()
            self.view.show_info("quit used, disconnecting")
            self.model.stop()
            return

        self.view.root.after(1500, self.to_stop_or_not_to_stop)

    def send_message(self, message):
        self.model.send(message)

    def show_message(self, message):
        self.view.show_client_message(message)

    def is_connected(self):
        if self.model.is_connected() == True:
            self.show_info("connected to server")
            self.view.enable_button()
            self.poll_queue()
            return
        elif self.flag == False:
            self.flag = True
            self.show_info("trying to reach the server...")
            self.view.disable_button()

        self.after_id = self.view.root.after(1000, self.is_connected)

    def show_info(self, message):
        self.view.show_info(message)

    def start(self):
        self.model.start()
        self.is_connected()
        self.to_stop_or_not_to_stop()
        self.view.start()
