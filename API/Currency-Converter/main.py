import requests
import tkinter as tk

def request_data() -> dict | None:
    response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    data = None
    if response.status_code == 200:
        data = response.json()
        print("Success:", data)

        for item in data:
            print(f"One {item['ccy']} costs {item['buy']} {item['base_ccy']}")

    elif response.status_code == 404:
        print("Error: Resource not found")
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data


def convert(amount: float, curr: str) -> float:
    if amount < 0:
        return 0

    data = request_data()
    result = 0
    for item in data:
        if item["ccy"] == curr:
            result = amount * float(item["sale"])

    return result


def convert_button_pressed(amount: str, curr: str) -> None:
    try:
        amount = float(amount)
        result = convert(amount, curr)
        result_label.config(text=f"{result}")
    except ValueError:
        result_label.config(text="Only numbers are allowed")


root = tk.Tk()
root.title("Currency Converter")
root.geometry("350x400")

input_label = tk.Label(root, text="Enter the amount you would like to convert(UAH):", font=("Arial", 12))
input_label.pack(pady=10)

entry = tk.Entry(root, width=35)
entry.pack()

options = ["EUR", "USD"]
selected = tk.StringVar(value=options[0])

dropdown = tk.OptionMenu(root, selected, *options)
dropdown.pack(pady=10)

convert_button = tk.Button(
    root,
    text="Convert",
    command=lambda: convert_button_pressed(entry.get(), selected.get())
)
convert_button.pack(pady=10)
convert_button.pack()

result_label = tk.Label(root, text=" ", font=("Arial", 16))
result_label.pack(pady=10)

root.mainloop()
