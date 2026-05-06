from datetime import datetime
import json
import os
import time
# from dotenv import load_dotenv
import requests
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO

# load_dotenv(verbose=True, override=True)
# API_KEY = os.getenv("API_KEY")

CACHE_TIME = 86400

def get_data(year_start, year_end) -> dict | None:
    specific_cache = f"cache_{year_start}_{year_end}.json"

    if os.path.exists(specific_cache):
        file_age = time.time() - os.path.getmtime(specific_cache)
        if file_age < CACHE_TIME:
            print("Loading cached data...")
            with open(specific_cache, 'r') as f:
                return json.load(f)

    url = 'https://images-api.nasa.gov/search'
    params = {
        'q': 'planet space',
        'media_type': 'image',
        'page_size': '50',
        'year_start': year_start,
        'year_end': year_end
    }

    response = requests.get(url, params=params)
    data = None

    if response.status_code == 200:
        data = response.json()
        print("Data retrieved from images-api.nasa.gov")

        with open(specific_cache, 'w') as f:
            json.dump(data, f)

        return data
    elif response.status_code == 404:
        print("Error: Resource not found")
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data


def parse_year(year_str, default):
    clean_year = year_str.strip()

    if not clean_year:
        return default

    if clean_year.isdigit() and len(clean_year) == 4:
        year_int = int(clean_year)
        current_year = datetime.now().year

        if 1800 <= year_int <= current_year:
            return clean_year

    print(f"Incorrect year: {year_str}. Default value: {default}")
    return default


def search_button_pressed(year_start_input, year_end_input):
    DEFAULT_START = "1920"
    DEFAULT_END = str(datetime.now().year)

    valid_start = parse_year(year_start_input, DEFAULT_START)
    valid_end = parse_year(year_end_input, DEFAULT_END)

    for widget in gallery_frame.winfo_children():
        widget.destroy()

    data = get_data(valid_start, valid_end)
    image_arr = data.get("collection", {}).get("items", [])

    if not image_arr:
        tk.Label(root, text="No images found or API error").pack()
        return

    row_idx = 0
    col_idx = 0
    columns_limit = 4

    print("Starting image download...")

    for i, item in enumerate(image_arr):
        if i > 15:
            break

        try:
            links = item.get("links", [])
            if not links:
                continue

            url = links[0].get("href")

            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content))

            img = img.resize((150, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(gallery_frame, image=photo)
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


root = tk.Tk()
root.title("NASA Gallery")
root.geometry("670x550")

root.grid_columnconfigure(0, weight=1)

search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, pady=20, padx=10)

label_from = tk.Label(search_frame, text="From (year): ")
label_from.grid(row=0, column=0, padx=5, pady=5)

entry_from = tk.Entry(search_frame)
entry_from.grid(row=0, column=1, padx=5, pady=5)

label_to = tk.Label(search_frame, text="To (year): ")
label_to.grid(row=0, column=3, padx=5, pady=5)

entry_to = tk.Entry(search_frame)
entry_to.grid(row=0, column=4, padx=5, pady=5)

search_button = tk.Button(search_frame, text="Search", command=lambda: search_button_pressed(entry_from.get(), entry_to.get()))
search_button.grid(row=0, column=5, padx=5, pady=5)

gallery_frame = tk.Frame(root)
gallery_frame.grid(row=1, column=0, pady=10)


root.mainloop()