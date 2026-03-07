import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Login / Register")
        self.window_width = 300
        self.window_height = 180
        self.root.update_idletasks()
        self.center(self.root, self.window_width, self.window_height)
        self.root.configure(background="#EAF4F9")

        self.frame = tk.Frame(self.root, bg="#EAF4F9")
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(self.frame, text="Username:", bg="#EAF4F9", fg="#243B4A").pack(anchor="w")
        self.username_entry = tk.Entry(self.frame, bg="#F5F9FC", fg="#243B4A", insertbackground="#243B4A")
        self.username_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.frame, text="Password:", bg="#EAF4F9", fg="#243B4A").pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, show="*", bg="#F5F9FC", fg="#243B4A", insertbackground="#243B4A")
        self.password_entry.pack(fill="x", pady=(0, 10))

        self.combo_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.combo_var,
            state="readonly",
            values=["login", "signup"],
            width=12
        )
        self.combobox.current(0)
        self.combobox.pack(pady=(0, 10))

        self.submit_button = tk.Button(
            self.frame,
            text="Submit",
            bg="#A0E9FF",
            fg="#243B4A",
            command=self.submit
        )
        self.submit_button.pack()

    def center(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        action = self.combo_var.get()
        print(f"{action} -> Username: {username}, Password: {password}")
        result = self.controller.verification(username, password, action)
        if result:
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Username or password is incorrect")

    def start(self):
        self.root.mainloop()