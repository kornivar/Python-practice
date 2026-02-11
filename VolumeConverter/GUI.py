import tkinter as tk

UNIT_TO_LITERS = {
    "milliliter (ml)": 0.001,
    "liter (l)": 1.0,
    "cubic centimeter (cm³)": 0.001,
    "cubic meter (m³)": 1000.0,
    "US gallon (gal)": 3.785411784,
}

root = tk.Tk()
root.title("Volume Converter")
root.geometry("420x320")
root.configure(bg="lightblue")

title = tk.Label(root, text="Volume Converter", font=("Arial", 18, "bold"), bg = "lightblue")
title.pack(pady=(12, 8))

frame = tk.Frame(root, bg="lightblue")
frame.pack(pady=6)

label_value = tk.Label(frame, text="Value", font=("Arial", 12), bg="lightblue")
label_value.grid(row=0, column=0, padx=8, pady=6, sticky="w")
entry_value = tk.Entry(frame, font=("Arial", 12), width=12, justify="center", bg = "lightblue")
entry_value.grid(row=1, column=0, padx=8)

label_from = tk.Label(frame, text="From", font=("Arial", 12), bg="lightblue")
label_from.grid(row=0, column=1, padx=8, pady=6, sticky="w")
from_var = tk.StringVar(value="liter (l)")
from_menu = tk.OptionMenu(frame, from_var, *UNIT_TO_LITERS.keys())
from_menu.config(font=("Arial", 11), width=20)
from_menu.grid(row=1, column=1, padx=8)

label_to = tk.Label(frame, text="To", font=("Arial", 12), bg="lightblue")
label_to.grid(row=0, column=2, padx=8, pady=6, sticky="w")
to_var = tk.StringVar(value="milliliter (ml)")
to_menu = tk.OptionMenu(frame, to_var, *UNIT_TO_LITERS.keys())
to_menu.config(font=("Arial", 11), width=20)
to_menu.grid(row=1, column=2, padx=8)

label_result = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="lightblue")
label_result.pack(pady=(14, 6))

def convert():
    s = entry_value.get().strip()
    if s == "":
        label_result.config(text="Enter a number", fg="red")
        return
    try:
        value = float(s.replace(",", "."))
    except ValueError:
        label_result.config(text="Error: invalid input", fg="red")
        return

    u_from = from_var.get()
    u_to = to_var.get()
    liters = value * UNIT_TO_LITERS[u_from]
    result = liters / UNIT_TO_LITERS[u_to]

    if abs(result - round(result)) < 1e-12:
        out = f"{int(round(result))}"
    else:
        out = f"{result:.6f}".rstrip("0").rstrip(".")

    label_result.config(text=f"{out} ({u_to})", fg="green")

def clear():
    entry_value.delete(0, tk.END)
    label_result.config(text="")

btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=(6, 8))

btn_convert = tk.Button(btn_frame, text="Convert", font=("Arial", 12), width=16, command=convert)
btn_convert.grid(row=0, column=0, padx=6, pady=6)

btn_clear = tk.Button(btn_frame, text="Clear", font=("Arial", 12), width=10, command=clear)
btn_clear.grid(row=0, column=1, padx=6, pady=6)

root.bind("<Return>", lambda event: convert())

root.mainloop()
