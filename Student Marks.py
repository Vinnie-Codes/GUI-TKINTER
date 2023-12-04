import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def connect_to_db():
    return sqlite3.connect('StudentData.db')

def create_student_table():
    conn = connect_to_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (student_id INTEGER PRIMARY KEY, first_name TEXT, surname TEXT, dob TEXT)''')
    conn.commit()
    conn.close()

def insert_student(student_id, first_name, surname, dob):
    conn = connect_to_db()
    conn.execute("INSERT INTO students (student_id, first_name, surname, dob) VALUES (?, ?, ?, ?)",
                 (student_id, first_name, surname, dob))
    conn.commit()
    conn.close()

current_record_index = 0
students_list = []

def load_students():
    conn = connect_to_db()
    cursor = conn.execute('SELECT * FROM students')
    for row in cursor:
        students_list.append(row)
    conn.close()

def refresh_student_details(index):
    if 0 <= index < len(students_list):
        student_id, first_name, surname, dob = students_list[index]
        entries['Student ID'].delete(0, tk.END)
        entries['Student ID'].insert(0, student_id)
        entries['First name'].delete(0, tk.END)
        entries['First name'].insert(0, first_name)
        entries['Surname'].delete(0, tk.END)
        entries['Surname'].insert(0, surname)
        entries['DOB'].delete(0, tk.END)
        entries['DOB'].insert(0, dob)

def create_record():
    global current_record_index, students_list
    new_student_id = simpledialog.askstring("Input", "Enter new student ID:", parent=root)
    if new_student_id:
        insert_student(new_student_id, '', '', '')
        students_list = []
        load_students()
        current_record_index = len(students_list) - 1
        refresh_student_details(current_record_index)

def first_record():
    global current_record_index
    current_record_index = 0
    refresh_student_details(current_record_index)

def previous_record():
    global current_record_index
    if current_record_index > 0:
        current_record_index -= 1
        refresh_student_details(current_record_index)

def next_record():
    global current_record_index
    if current_record_index < len(students_list) - 1:
        current_record_index += 1
        refresh_student_details(current_record_index)

def last_record():
    global current_record_index
    current_record_index = len(students_list) - 1
    refresh_student_details(current_record_index)

def save_record():
    global current_record_index, students_list
    if 0 <= current_record_index < len(students_list):
        student_id = entries['Student ID'].get()
        first_name = entries['First name'].get()
        surname = entries['Surname'].get()
        dob = entries['DOB'].get()
        conn = connect_to_db()
        conn.execute('UPDATE students SET first_name = ?, surname = ?, dob = ? WHERE student_id = ?',
                     (first_name, surname, dob, student_id))
        conn.commit()
        conn.close()
        students_list[current_record_index] = (student_id, first_name, surname, dob)

root = tk.Tk()
root.title("Student Mark System")
root.geometry("400x300")

frame_student_details = tk.Frame(root)
frame_student_details.grid(row=0, column=0, sticky="nsew")

entries = {}
labels = ['Student ID', 'First name', 'Surname', 'DOB']
for i, label in enumerate(labels):
    tk.Label(frame_student_details, text=label).grid(row=i, column=0, sticky='w')
    entry = tk.Entry(frame_student_details)
    entry.grid(row=i, column=1, sticky='ew')
    entries[label] = entry

frame_nav = tk.Frame(root)
frame_nav.grid(row=1, column=0, sticky="ew")
nav_buttons = {
    '<<': first_record,
    '<': previous_record,
    '>': next_record,
    '>>': last_record,
    'New': create_record,
    'Save': save_record
}
for i, (text, command) in enumerate(nav_buttons.items()):
    button = tk.Button(frame_nav, text=text, command=command)
    button.grid(row=0, column=i)

create_student_table()
load_students()
if students_list:
    refresh_student_details(current_record_index)

root.mainloop()
