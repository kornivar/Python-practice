import tkinter as tk
root = tk.Tk()
root.title("Zodiac sign finder")
root.geometry("400x400")
root.configure(bg="lightblue")

labelD = tk.Label(root, text="Enter day", font=('Arial', 14), bg = "lightblue")
labelD.pack(padx=20,pady=10)

entryD = tk.Entry(root, width=20, font=('Arial', 14))
entryD.pack(padx=20,pady=0)

labelM = tk.Label(root, text="Enter month", font=('Arial', 14), bg = "lightblue")
labelM.pack(padx=20,pady=10)
entryM = tk.Entry(root, width=20, font=('Arial', 14))
entryM.pack(padx=20,pady=0)

labelY = tk.Label(root, text="Enter year", font=('Arial', 14), bg = "lightblue")
labelY.pack(padx=20,pady=10)
entryY = tk.Entry(root, width=20, font=('Arial', 14))
entryY.pack(padx=20,pady=0)

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def find_zodiac():
    try:
        day = int(entryD.get())
        month = int(entryM.get())
        year = int(entryY.get())
    except ValueError:
        result_label.config(text="Please enter valid integers for day, month, and year.", fg="coral")
        return

    days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30,
                     31, 31, 30, 31, 30, 31]
    
    if month < 1 or month > 12 or day < 1 or day > days_in_month[month-1]:
        result_label.config(text="Invalid date!", fg="coral")
        return

    if (month == 1 and day >= 20) or (month == 2 and day <= 18):
        zodiaс = "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        zodiaс = "Pisces"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        zodiaс = "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        zodiaс = "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        zodiaс = "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        zodiaс = "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        zodiaс = "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        zodiaс = "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        zodiaс = "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        zodiaс = "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        zodiaс = "Sagittarius"
    else:
        zodiaс = "Capricorn"

    result_label.config(text=f"Your Zodiac sign is: {zodiaс}", fg="black")

    try:
        img = tk.PhotoImage(file=f"./img/{zodiaс}.png")
        image_label.config(image=img)
        image_label.image = img       
    except Exception:
        image_label.config(text="Image not found", image="")
        image_label.image = None


button = tk.Button(root, text="Find Zodiac Sign", font=('Arial', 14), bg="black", fg="whitesmoke", command=find_zodiac)
button.pack(padx=20,pady=20)
result_label = tk.Label(root, text="", font=('Arial', 14), bg = "lightblue")
result_label.pack(padx=20,pady=0)
image_label = tk.Label(root, bg="lightblue")
image_label.pack(pady=10)
image = tk.PhotoImage(file="")


root.mainloop()