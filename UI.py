from customtkinter import *
from tkinter import messagebox
import pickle
import customtkinter as custom
import pandas as pd

with open('classifier.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

custom.set_appearance_mode("Dark") 

global root
root = custom.CTk()
root.geometry("800x780+510+95")
root.resizable(0, 0)
root.title("BlazeForecast")

title = custom.CTkLabel(root, text="Blaze Anticipation",text_color="orange", font=custom.CTkFont(size=34, family="Calibri", weight="bold"))
title.pack(padx=10, pady=15)

entries = {}
labels = ['Temperature', 'RH', 'WS', 'Rain', 'FFMC', 'DMC', 'DC', 'ISI', 'FWI']
default_values = [30, 65, 14, 0, 85.4, 16, 44.5, 4.5, 6.5, 1]

for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
    new_label = custom.CTkLabel(root, text=f"{label_text} : ", font=custom.CTkFont(size=16, family="Times New Roman"))
    new_label.place(x=220, y=85 + i * 40)

    new_entry = custom.CTkEntry(root, width=140)
    new_entry.place(x=420, y=85 + i * 40)

    # Set placeholder values
    new_entry.insert(0, str(default_value))
    entries[label_text] = new_entry

result_frame = custom.CTkFrame(root,bg_color="black",border_color="white")
result_frame.place(x=120, y=550)

result_label = custom.CTkLabel(result_frame, width=580, height=180, text="Preserve the green, Quench the red. Just Protect Environment", font=custom.CTkFont(size=16, family="Times New Roman"), bg_color="black", text_color="white")  # Set text color to black and background color to white
result_label.pack()

def check_values():
    data = {label: entry.get() for label, entry in entries.items()}
    
    if any(value == '' for value in data.values()):
        messagebox.showwarning("Empty Field", f"All respective fields are required to be filled")
        return

    input_list = [float(value) for value in data.values()]

    df = pd.DataFrame([input_list], columns=labels)
    df = df.astype(float)
    predictions = loaded_model.predict(df)

    result_frame.place(x=120, y=550)
    
    if predictions[0] == 1:
        message = "Nature seems to be clearing its throat with a symphony of dry leaves and crackling twigs.\nIts hinting at an imminent forest inferno"
    else:
        message = "NO need for fire extinguishers today...!\nThe predictor is telling us that the forest gets to relax without the worry of a fiery surprise"

    result_label.configure(text=f"The predicted class is: {predictions}\n\n{message}")

check_button = custom.CTkButton(root, text="Check", command=check_values, fg_color='green')
check_button.place(x=220, y=480)

clear_button = custom.CTkButton(root, text="Clear", command=lambda: [entry.delete(0, 'end') for entry in entries.values()] and result_frame.place_forget(), fg_color='purple')
clear_button.place(x=420, y=480)

root.mainloop()
