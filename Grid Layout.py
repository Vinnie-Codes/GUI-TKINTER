import tkinter as tk
root = tk.Tk()
root.title("Grid Layout")
for rowcol in range(5):
    root.rowconfigure(rowcol, weight =1 )
    root.columnconfigure(rowcol, weight=1)
label = tk.Label(root, text="Cell(0,0)")
label2 = tk.Label(root, text="Cell(1,0)")
label3 = tk.Label(root, text="Cell(2,0)")
label4 = tk.Label(root, text="Cell(3,0)")
label5 = tk.Label(root, text="Cell(2,1) column span 2")
button = tk.Button(root, text="Click Me")

label.grid(row=0, column=0)
label2.grid(row=0, column=1)
label3.grid(row=0, column=2)
label4.grid(row=0, column=3)
label5.grid(row=1,column=2, columnspan=2)
button.grid(row=1, column=1)


root.minsize(300,200)
root.maxsize(500,400)
root.attributes('-alpha', 0.9)
root.mainloop()

