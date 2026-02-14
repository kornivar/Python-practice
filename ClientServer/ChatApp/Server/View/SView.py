import tkinter as tk
from importlib.metadata import pass_none


class SView:
    def __init__(self, scontroller):
        self.scontroller = scontroller
        self.root = tk.Tk()
        self.root.title('Server')

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 400) // 2
        y = (self.root.winfo_screenheight() - 550) // 2
        self.root.geometry(f"{400}x{550}+{x}+{y}")



    def create_interface(self):
        self.root.configure(background="#EAF4F9")

        self.text_area = tk.Text(self.root, state="disabled", wrap="word", bg="#BFDCEB", fg="#243B4A", insertbackground="#1C2E3A")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)

        self.entry = tk.Entry(self.bottom_frame, bg="#F5F9FC", fg="#243B4A", insertbackground="#F5F9FC")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.send_button = tk.Button(self.bottom_frame, text="SEND MESSAGE", bg="#A0E9FF", fg="#243B4A", command=self.send_message)
        self.send_button.pack(side="right")


    def send_message(self):
        message = self.entry.get()
        self.scontroller.send_message(message)
        self.show_my_message(message)

    def show_client_message(self, massage):
        if massage.strip():
            self.text_area.config(state="normal")
            self.text_area.insert(tk.END, f"Client: {massage}\n")
            self.text_area.config(state="disabled")
            self.text_area.see(tk.END)
            self.entry.delete(0, tk.END)

    def show_my_message(self, massage):
        if massage.strip():
            self.text_area.config(state="normal")
            self.text_area.insert(tk.END, f"Server: {massage}\n")
            self.text_area.config(state="disabled")
            self.text_area.see(tk.END)
            self.entry.delete(0, tk.END)

    def start(self):
        self.create_interface()
        self.root.mainloop()
