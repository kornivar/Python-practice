from View.view import View

class Controller:
    def __init__(self, model, queue):
        self.model = model
        self.queue = queue
        self.view = View(self)

        self.known_clients = set()

    def to_stop_or_not_to_stop(self):
        if self.model.running == False:
            self.view.disable_button()
            self.view.show_info("stop used, disconnecting")
            self.model.stop()
            return

        self.view.root.after(1500, self.to_stop_or_not_to_stop)

    def send_message(self, message, selected):
        if selected == "all":
            self.model.send(message, target_id="all")
        else:
            client_id = int(selected.split()[-1])
            self.model.send(message, target_id=client_id)
    def show_message(self, message):
        self.view.show_client_message(message)

    def is_connected(self):
        if self.model.is_connected() == True:
            self.show_info("client connected")
            self.view.enable_button()
            self.poll_queue()
            return
        else:
            self.view.disable_button()

        self.view.root.after(1000, self.is_connected)

    def poll_queue(self):
        while not self.queue.empty():
            client_id, message = self.queue.get()

            if client_id not in self.known_clients:
                self.known_clients.add(client_id)

                values = ["all"] + [f"Client {cid}" for cid in self.known_clients]
                self.view.update_combobox_values(values)

            self.view.show_client_message(message, client_id)

        self.view.root.after(100, self.poll_queue)

    def show_info(self, message):
        self.view.show_info(message)

    def start(self):
        self.model.start()
        self.is_connected()
        self.to_stop_or_not_to_stop()
        self.view.start()