import tkinter as tk
from tkinter import ttk

def open_shape_window():
    shape_window.deiconify()

def open_selection_window():
    selection_window.deiconify()

def draw_shape(event=None):
    shape_canvas.delete("all")
    w, h = shape_canvas.winfo_width(), shape_canvas.winfo_height()
    min_dimension = min(w, h)
    shape = shape_combobox.get()
    colour = color_combobox.get()

    cx, cy = w / 2, h / 2

    if shape == 'Circle':
        radius = min_dimension * 0.25
        shape_canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=colour)
    elif shape == 'Ellipse':
        shape_canvas.create_oval(w * 0.1, h * 0.25, w * 0.9, h * 0.75, fill=colour)
    elif shape == 'Rectangle':
        shape_canvas.create_rectangle(w * 0.25, h * 0.25, w * 0.75, h * 0.75, fill=colour)
    elif shape == 'Square':
        side = min_dimension * 0.5
        shape_canvas.create_rectangle(cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2, fill=colour)
    elif shape == 'Triangle':
        shape_canvas.create_polygon(cx, cy - radius, cx - radius, cy + radius, cx + radius, cy + radius, fill=colour)

def update_shape():
    draw_shape()

root = tk.Tk()
root.title("Main Window")
root.geometry("300x150")

button_shape_window = tk.Button(root, text="Open Shape Window", command=open_shape_window)
button_shape_window.pack(pady=10)

button_selection_window = tk.Button(root, text="Open Selection Window", command=open_selection_window)
button_selection_window.pack(pady=10)

shape_window = tk.Toplevel(root)
shape_window.title("Shape Window")
shape_window.geometry("300x200")
shape_window.withdraw()

shape_canvas = tk.Canvas(shape_window)
shape_canvas.pack(fill="both", expand=True)
shape_canvas.bind("<Configure>", draw_shape)

selection_window = tk.Toplevel(root)
selection_window.title("Selection Window")
selection_window.geometry("300x200")
selection_window.withdraw()

shape_combobox = ttk.Combobox(selection_window, values=["Square", "Rectangle", "Circle", "Ellipse", "Triangle"])
shape_combobox.current(0)
shape_combobox.pack(pady=10)

color_combobox = ttk.Combobox(selection_window, values=["Red", "Blue", "Green", "Yellow"])
color_combobox.current(1)
color_combobox.pack(pady=10)

update_button = tk.Button(selection_window, text="Update Shape", command=update_shape)
update_button.pack(pady=10)

menubar = tk.Menu(root)

mainmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Windows", menu=mainmenu)

mainmenu.add_command(label="Open Shape Window", command=open_shape_window)
mainmenu.add_command(label="Open Selection Window", command=open_selection_window)

root.config(menu=menubar)

root.mainloop()
