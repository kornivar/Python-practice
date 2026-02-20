import tkinter as tk

class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title('Client')

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 400) // 2
        y = (self.root.winfo_screenheight() - 550) // 2
        self.root.geometry(f"{400}x{550}+{x}+{y}")

        self.create_interface()


    def create_interface(self):
        self.root.configure(background="#EAF4F9")

        self.text_area = tk.Text(self.root, state="disabled", wrap="word", bg="#BFDCEB", fg="DarkBlue", insertbackground="#1C2E3A")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)


    def show_server_message(self, massage):
        if massage.strip():
            self.text_area.config(state="normal")
            self.text_area.insert(tk.END, f"Server message: {massage}\n")
            self.text_area.config(state="disabled")
            self.text_area.see(tk.END)


    def show_info(self, massage):
        if massage.strip():
            self.text_area.config(state="normal")
            self.text_area.insert(tk.END, f"{massage.upper()}\n")
            self.text_area.config(state="disabled")
            self.text_area.see(tk.END)


    def start(self):
        self.root.mainloop()