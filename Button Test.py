import tkinter as tk
root= tk.Tk()
root.title("Button Test")
root.geometry("300x200+100+150")
root.resizable(True,True)
root.minsize(300,400)
canvas = tk.Canvas (root, width = 70, height = 70)
canvas.grid(row=3, column=4)

def buttongreen_pressed():
    label_output.config(text="Green Button Pressed", foreground="Green")
    canvas.delete("all")
    
    canvas.create_rectangle(0,0,50,50, fill = "Green")
def buttonred_pressed():
    label_output.config(text="Red Button pressed", foreground="Red")
    canvas.delete("all")
    canvas.create_rectangle(0,0,50,50, fill = "Red")
def buttonblue_pressed():
    label_output.config(text="Blue Button pressed", foreground="blue")
    canvas.delete("all")
    canvas.create_rectangle(0,0,50,50, fill = "Blue")
def buttonwhite_pressed():
    label_output.config(text="Grey Button pressed", foreground="Grey")
    canvas.delete("all")
    canvas.create_rectangle(0,0,50,50, fill = "Grey")
def clicked_label(event):
    label_output.config(text="label reset")
for rowcol in range(10):
    root.rowconfigure(rowcol, weight =1 )
    root.columnconfigure(rowcol, weight=1)
    
label_output = tk.Label(root,text="")
buttongreen = tk.Button(root, text = "Green", command=buttongreen_pressed)
buttonred =tk.Button(root, text="Red", command=buttonred_pressed)
buttonblue =tk.Button(root, text="Blue", command=buttonblue_pressed)
buttonwhite=tk.Button(root, text="Grey", command=buttonwhite_pressed)
label_output.grid(row=1, column=0, columnspan=10)
buttongreen.grid(row=6, column=1)
buttonred.grid(row=6, column=3)
buttonblue.grid(row=6, column=5)
buttonwhite.grid(row=6, column=7)
label_output.bind('<Button>', clicked_label)
root.mainloop()
