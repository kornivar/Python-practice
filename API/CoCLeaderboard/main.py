import json
import os
import time
from dotenv import load_dotenv
import requests
import tkinter as tk


load_dotenv(verbose=True, override=True)

API_TOKEN = os.getenv("API_TOKEN")
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}
BASE_URL = "https://api.clashofclans.com/v1"

CACHE_TIME = 86400

COUNTRIES_FILE = "country_ids.json"

current_after = None
current_location_id = None


def load_countries() -> dict:
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    countries = {}

    for item in data["items"]:
        if item.get("isCountry"):
            countries[item["name"]] = item["id"]

    return countries


COUNTRIES = load_countries()
COUNTRY_NAMES = sorted(COUNTRIES.keys())


def get_clan_rankings(location_id, limit=25, after=None):

    os.makedirs("cache", exist_ok=True)

    cache_file = f"cache/cache_{location_id}.json"

    cache_key = f"{limit}_{after}"

    cache_data = {}

    if os.path.exists(cache_file):
        file_age = time.time() - os.path.getmtime(cache_file)

        if file_age < CACHE_TIME:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            if cache_key in cache_data:
                print("Loading cached page...")
                return cache_data[cache_key]

    url = f"{BASE_URL}/locations/{location_id}/rankings/clans"

    params = {
        "limit": limit
    }

    if after:
        params["after"] = after

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        data = response.json()

        cache_data[cache_key] = data

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=4)

        return data

    elif response.status_code == 404:
        print("Error: Resource not found")

    else:
        print(f"Request failed with status code: {response.status_code}")

    return None


# ---------------- UI ----------------


def update_suggestions(event=None):
    value = country_var.get().lower()

    listbox.delete(0, tk.END)

    if not value:
        listbox_frame.place_forget()
        return

    matches = [
        c for c in COUNTRY_NAMES
        if value in c.lower()
    ][:3]

    if not matches:
        listbox_frame.place_forget()
        return

    for m in matches:
        listbox.insert(tk.END, m)

    x = entry.winfo_rootx() - root.winfo_rootx()
    y = entry.winfo_rooty() - root.winfo_rooty()

    listbox_frame.place(
        x=x,
        y=y + entry.winfo_height() + 2
    )

    listbox_frame.lift()


def select_country(event):
    if listbox.curselection():
        value = listbox.get(listbox.curselection())
        country_var.set(value)
        listbox_frame.place_forget()


def render_data(data):
    global current_after, rank_counter

    if not data:
        return

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)

    for clan in data.get("items", []):
        result_text.insert(
            tk.END,
            f"{clan['rank']}. {clan['name']} | {clan['clanPoints']}\n"
        )
        rank_counter += 1

    result_text.config(state="disabled")

    current_after = data.get("paging", {}).get("cursors", {}).get("after")


def search():
    global current_after, current_location_id

    name = country_var.get()

    if name not in COUNTRIES:
        result_label.config(text="Country not found")
        return

    current_location_id = COUNTRIES[name]
    current_after = None

    data = get_clan_rankings(current_location_id, after=None)

    render_data(data)


def next_page():
    global current_after, current_location_id

    if current_after is None or not current_location_id:
        next_page_button.config(state="disabled")
        return

    data = get_clan_rankings(
        current_location_id,
        after=current_after
    )

    render_data(data)


# ---------------- window ----------------

root = tk.Tk()
root.title("Leaderboard")
root.geometry("400x550")

root.grid_columnconfigure(0, weight=1)

search_frame = tk.Frame(root)
search_frame.grid(row=0, column=0, pady=20)

tk.Label(search_frame, text="Country:").grid(row=0, column=0, padx=5)

country_var = tk.StringVar()
entry = tk.Entry(search_frame, textvariable=country_var, width=40)
entry.grid(row=0, column=1)
entry.bind("<KeyRelease>", update_suggestions)

tk.Button(search_frame, text="Search", command=search).grid(row=0, column=2, padx=5)

listbox_frame = tk.Frame(root)
listbox = tk.Listbox(listbox_frame, height=3, width=40)
listbox.pack()
listbox.bind("<<ListboxSelect>>", select_country)

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0)

result_text = tk.Text(root, width=70, height=25)
result_text.grid(row=2, column=0, padx=10, pady=10)
result_text.config(state="disabled")

footer_frame = tk.Frame(root)
footer_frame.grid(row=3, column=0, pady=(0,10))
next_page_button = tk.Button(footer_frame, text="Next Page", command=next_page)
next_page_button.grid(row=3, column=1, padx=5)


root.mainloop()