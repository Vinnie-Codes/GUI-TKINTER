import tkinter as tk
from tkinter import ttk


def option_selected(event):
    canvas.delete("all")  
    shape = combobox.get()
    colour = combobox1.get()
    if shape == 'Square':
        canvas.create_rectangle(20, 20, 70, 70, fill=colour)
    elif shape == 'Rectangle':
        canvas.create_rectangle(20, 20, 80, 60, fill=colour)
    elif shape == 'Circle':
        canvas.create_oval(20, 20, 70, 70, fill=colour)
def colour_option_selected(event):
    canvas.delete("all")
    shape = combobox.get()
    colour = combobox1.get()
    if shape == 'Circle':
        canvas.create_oval(20, 20, 70, 70, fill=colour)
    elif shape == 'Rectangle':
        canvas.create_rectangle(20, 20, 80, 60, fill=colour)
    elif shape == 'Square':
        canvas.create_rectangle(20, 20, 70, 70, fill=colour)


root = tk.Tk()
root.title("Shape Selector and Color Buttons")
root.geometry("400x150")
root.resizable(True, True)
root.minsize(300, 100)

canvas = tk.Canvas(root, width=70, height=70)
canvas.grid(row=1, column=0, columnspan=4)


combobox = ttk.Combobox(root, values=["Square", "Rectangle", "Circle"])
combobox.current(0)  
combobox.bind('<<ComboboxSelected>>', option_selected)
combobox.grid(row=0, column=0, padx=10, pady=10)
combobox1 = ttk.Combobox(root, values=["Red", "Blue", "White"])
combobox1.current(0)  
combobox1.bind('<<ComboboxSelected>>', colour_option_selected)
combobox1.grid(row=0, column=4, padx=10, pady=10)

label_output = tk.Label(root, text="")
label_output.grid(row=2, column=0, columnspan=4)


root.mainloop()


