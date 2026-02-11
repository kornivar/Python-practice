import threading
import tkinter as tk
import time

threads = []
carrot_count = 0
harvestL = False
harvestM = False
harvestR = False

root = tk.Tk()
root.title("Carrot Growing Simulator")
root.geometry("300x350")
root.configure(bg="lightblue")

images = [tk.PhotoImage(file=f"Threads_practice/img/{i}.png") for i in range(1, 9)]

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

labelCCount = tk.Label(root, text=f"Carrot Count: {carrot_count}", bg="lightblue", font=("Arial", 12))
labelCCount.grid(row=0, column=0, columnspan=3, pady=10)

labelImgL = tk.Label(root, bg="lightblue")
labelImgL.grid(row=2, column=0)

labelImgM = tk.Label(root, bg="lightblue")
labelImgM.grid(row=2, column=1)

labelImgR = tk.Label(root, bg="lightblue")
labelImgR.grid(row=2, column=2)

label_map = {"L": labelImgL, "M": labelImgM, "R": labelImgR}

def grow(btn_name, harvest_flag_name):
    global harvestL, harvestM, harvestR

    img_label = label_map[harvest_flag_name]

    for stage in range(len(images)):
        time.sleep(1)
        img_label.config(image=images[stage])

    if harvest_flag_name == "L":
        harvestL = True
    elif harvest_flag_name == "M":
        harvestM = True
    elif harvest_flag_name == "R":
        harvestR = True

def harvest(btn_name, harvest_flag_name):
    global carrot_count
    carrot_count += 1
    labelCCount.config(text=f"Carrot Count: {carrot_count}")

    if harvest_flag_name == "L":
        global harvestL
        harvestL = False
    elif harvest_flag_name == "M":
        global harvestM
        harvestM = False
    elif harvest_flag_name == "R":
        global harvestR
        harvestR = False

    label_map[harvest_flag_name].config(image="") 

def start(btn_name, harvest_flag_name):
    if ((harvest_flag_name=="L" and not harvestL) or 
        (harvest_flag_name=="M" and not harvestM) or
        (harvest_flag_name=="R" and not harvestR)):
        
        grow_thread = threading.Thread(target=grow, args=(btn_name, harvest_flag_name))
        grow_thread.start()
        threads.append(grow_thread)
    else:
        harvest(btn_name, harvest_flag_name)

btnCarrotL = tk.Button(root, width=4, height=2, font=("Arial", 10), bg="brown",
                       command=lambda: start(btnCarrotL, "L"))
btnCarrotL.grid(row=1, column=0, padx=2, pady=10)

btnCarrotM = tk.Button(root, width=4, height=2, font=("Arial", 10), bg="brown",
                       command=lambda: start(btnCarrotM, "M"))
btnCarrotM.grid(row=1, column=1, padx=2, pady=10)

btnCarrotR = tk.Button(root, width=4, height=2, font=("Arial", 10), bg="brown",
                       command=lambda: start(btnCarrotR, "R"))
btnCarrotR.grid(row=1, column=2, padx=2, pady=10)

root.mainloop()
