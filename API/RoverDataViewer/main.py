from datetime import datetime
import json
import os
import time
import requests
import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO

CACHE_TIME = 86400
selected_rover = "perseverance"
ROVER_CAMERAS = {
    "perseverance": {
        "All": "",
        "Navcam Left": "NAVCAM_LEFT",
        "Navcam Right": "NAVCAM_RIGHT",
        "Mastcam Z Left": "MCZ_LEFT",
        "Mastcam Z Right": "MCZ_RIGHT",
        "Front Hazard": "FHAZ",
        "Rear Hazard": "RHAZ",
        "Skycam": "SKYCAM"
    },
    "curiosity": {
        "All": "",
        "Front Hazard": "FHAZ",
        "Rear Hazard": "RHAZ",
        "Mast": "MAST",
        "ChemCam RMI": "CHEMCAM_RMI",
        "Navigation": "NAVCAM"
    }
}


def get_data(date_str, rover, camera) -> dict | None:
    specific_cache = f"{rover}_cache/cache_{rover}_{date_str}_{camera}.json"

    if os.path.exists(specific_cache):
        file_age = time.time() - os.path.getmtime(specific_cache)
        if file_age < CACHE_TIME:
            print(f"Loading cached data for {date_str}...")
            with open(specific_cache, 'r') as f:
                return json.load(f)

    url = f'https://rovers.nebulum.one/api/v1/rovers/{rover}/photos'
    params = {
        'earth_date': date_str,
        'page': '1'
    }
    if camera:
        params['camera'] = camera

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            with open(specific_cache, 'w') as f:
                json.dump(data, f)
            print(f"Data retrieved for {date_str}")
            return data
    except Exception as e:
        print(f"Request failed: {e}")

    return None


def parse_date(date_str, rover):
    clean_date = date_str.strip()

    limits = {
        "perseverance": datetime(2021, 2, 18),
        "curiosity": datetime(2012, 8, 6)
    }

    try:
        input_dt = datetime.strptime(clean_date, '%Y-%m-%d')

        if input_dt < limits.get(rover, datetime(2000, 1, 1)):
            print(f"Warning: {rover.capitalize()} was not on Mars yet.")
            return limits[rover].strftime('%Y-%m-%d')

        return clean_date
    except ValueError:
        print(f"Invalid format: {clean_date}. Use YYYY-MM-DD.")
        return "2023-01-01"


def search_button_pressed(date_input, camera_label):
    global selected_rover
    valid_date = parse_date(date_input, selected_rover)

    camera_code = ROVER_CAMERAS[selected_rover].get(camera_label, "")

    for widget in gallery_frame.winfo_children():
        widget.destroy()

    data = get_data(valid_date, selected_rover, camera_code)
    image_arr = data.get("photos", []) if data else []

    if not image_arr:
        tk.Label(gallery_frame, text=f"No photos found for {valid_date}").grid(row=0, column=0)
        return

    row_idx, col_idx = 0, 0
    columns_limit = 4

    for i, item in enumerate(image_arr):
        if i > 11: break

        try:
            url = item.get("img_src")
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 110), Image.Resampling.LANCZOS)
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
            print(f"Error loading image: {e}")


def start_with_rover(rover_name):
    global selected_rover
    selected_rover = rover_name

    menu = camera_menu["menu"]
    menu.delete(0, "end")

    rover_cams = ROVER_CAMERAS.get(rover_name, {})
    for label in rover_cams.keys():
        menu.add_command(label=label, command=tk._setit(camera_var, label))

    camera_var.set("All")

    choose_rover_window.destroy()
    root.deiconify()
    root.title(f"Mars Rover Viewer - {rover_name.capitalize()}")


# --- UI SETUP ---
root = tk.Tk()
root.withdraw()
root.title("Mars Rover Viewer")
root.geometry("700x480")
root.grid_columnconfigure(0, weight=1)

search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, pady=20)

tk.Label(search_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
entry_date = tk.Entry(search_frame, width=12)
entry_date.insert(0, "2023-05-20")  # Пример даты
entry_date.grid(row=0, column=1, padx=5)

tk.Label(search_frame, text="Camera:").grid(row=0, column=2, padx=5)
camera_var = tk.StringVar(root)
camera_var.set("All")
camera_menu = tk.OptionMenu(search_frame, camera_var, *ROVER_CAMERAS.keys())
camera_menu.grid(row=0, column=3, padx=5)

search_button = tk.Button(search_frame, text="Get Photos", bg="#ff4500", fg="white",
                          command=lambda: search_button_pressed(entry_date.get(), camera_var.get()))
search_button.grid(row=0, column=4, padx=10)

gallery_frame = tk.Frame(root)
gallery_frame.grid(row=1, column=0, pady=10)


# --- ROVER SELECTION WINDOW ---
choose_rover_window = tk.Toplevel()
choose_rover_window.title("Select Mission")
choose_rover_window.geometry("750x450")
choose_rover_window.grid_columnconfigure(0, weight=1)

tk.Label(choose_rover_window, text="Select Mars Rover", font=("Arial", 20, "bold")).grid(row=0, column=0, pady=20)
content_frame = tk.Frame(choose_rover_window)
content_frame.grid(row=1, column=0)


def create_rover_card(name, column, img_path):
    try:
        img = Image.open(img_path)
        img = img.resize((300, 220))
        photo = ImageTk.PhotoImage(img)
        btn = tk.Button(content_frame, image=photo, command=lambda: start_with_rover(name))
        btn.image = photo
        btn.grid(row=0, column=column, padx=20)
        tk.Button(content_frame, text=f"Launch {name.capitalize()}", font=("Arial", 12),
                  command=lambda: start_with_rover(name)).grid(row=1, column=column, pady=10)
    except:
        tk.Button(content_frame, text=name.upper(), width=20, height=10,
                  command=lambda: start_with_rover(name)).grid(row=0, column=column, padx=20)


create_rover_card("perseverance", 0, "images/perseverance_rover.jpg")
create_rover_card("curiosity", 1, "images/curiosity_rover.jpg")

root.mainloop()