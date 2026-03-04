import tkinter as tk
from tkinter import ttk

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login / Register")
        self.root.geometry("300x180")
        self.root.configure(background="#EAF4F9")

        # Основной фрейм для полей
        self.frame = tk.Frame(self.root, bg="#EAF4F9")
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Поле Username
        tk.Label(self.frame, text="Username:", bg="#EAF4F9", fg="#243B4A").pack(anchor="w")
        self.username_entry = tk.Entry(self.frame, bg="#F5F9FC", fg="#243B4A", insertbackground="#243B4A")
        self.username_entry.pack(fill="x", pady=(0, 10))

        # Поле Password
        tk.Label(self.frame, text="Password:", bg="#EAF4F9", fg="#243B4A").pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, show="*", bg="#F5F9FC", fg="#243B4A", insertbackground="#243B4A")
        self.password_entry.pack(fill="x", pady=(0, 10))

        # Тип действия: Login / Register
        self.combo_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.combo_var,
            state="readonly",
            values=["Login", "Register"],
            width=12
        )
        self.combobox.current(0)
        self.combobox.pack(pady=(0, 10))

        # Кнопка отправки
        self.submit_button = tk.Button(
            self.frame,
            text="Submit",
            bg="#A0E9FF",
            fg="#243B4A",
            command=self.submit
        )
        self.submit_button.pack()

    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        action = self.combo_var.get()
        print(f"{action} -> Username: {username}, Password: {password}")
        # Здесь можно добавить проверку через модель
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    window = LoginWindow()
    window.run()