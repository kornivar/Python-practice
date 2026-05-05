import json
import os
import time
from dotenv import load_dotenv
import requests
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO

load_dotenv(verbose=True, override=True)
API_KEY = os.getenv("API_KEY")

CACHE_FILE = 'cache_city.json'
CACHE_TIME = 86400


def get_data() -> dict | None:
    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)
        if file_age < CACHE_TIME:
            print("Loading cached data...")
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)

    response = requests.get('https://pixabay.com/api/?key=' + API_KEY + '&q=city' + '&image_type=photo' + '&orientation=horizontal')
    data = None

    if response.status_code == 200:
        data = response.json()
        print("Data retrieved from pixabay.com")

        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)

        return data
    elif response.status_code == 404:
        print("Error: Resource not found")
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data


root = tk.Tk()
root.title("City Gallery")
root.geometry("670x565")

data = get_data()
image_arr = data.get("hits", [])

if not image_arr:
    tk.Label(root, text="No images found or API error").pack()

row_idx = 0
col_idx = 0
columns_limit = 4

print("Starting image download...")

for i, image_data in enumerate(image_arr):
    if i > 8:
        break

    try:
        if i == 0:
            url = image_data.get("webformatURL")
            response = requests.get(url, timeout=3)
            img = Image.open(BytesIO(response.content))

            img = img.resize((600, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(root, image=photo)
            label.image = photo
            label.grid(row=0, column=0, columnspan=4, padx=5, pady=10)

            row_idx = 1
        else:
            url = image_data.get("previewURL")
            response = requests.get(url, timeout=3)
            img = Image.open(BytesIO(response.content))

            img = img.resize((150, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(root, image=photo)
            label.image = photo
            label.grid(row=row_idx, column=col_idx, padx=5, pady=5)

            col_idx += 1

            if col_idx >= columns_limit:
                col_idx = 0
                row_idx += 1

        root.update()
    except Exception as e:
        print(f"Failed to load image at index {i}: {e}")

print("Done.")
root.mainloop()