import tkinter as tk
root = tk.Tk ()
root.title("My GUI Program")
label = tk.Label(root, text="Hello World! ", bg= "blue", fg="white").pack(side = "left", fill="x", expand=False)
button = tk.Button(root,text="Button 1").pack()
label = tk.Label(root, text="Hello World! ", bg= "blue", fg="white").pack(side = "right", fill="x", expand=False)
button = tk.Button(root,text="Button 2").pack()
root.geometry("300x300-200+200")
root.tk.call('tk', 'scaling', 2.0)
root.mainloop()