import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import scrolledtext

conn = sqlite3.connect('./user_info.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                family TEXT,
                phone TEXT,
                course TEXT,
                status TEXT,
                national_id TEXT)''')
conn.commit()

def insert_user(name, family, phone, course, status, national_id):
    c.execute("INSERT INTO users (name, family, phone, course, status, national_id) VALUES (?, ?, ?, ?, ?, ?)",
              (name, family, phone, course, status, national_id))
    conn.commit()

def search_users(name):
    c.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
    return c.fetchall()

def list_users():
    c.execute("SELECT * FROM users")
    return c.fetchall()

def open_user_window(user_data):
    user_window = tk.Toplevel()
    user_window.title(f"مشخصات کاربر: {user_data[1]} {user_data[2]}")

    user_info = f"نام: {user_data[1]}\nنام خانوادگی: {user_data[2]}\nتلفن: {user_data[3]}\nدوره: {user_data[4]}\n"
    user_status = user_data[5]
    user_national_id = user_data[6]

    user_label = ttk.Label(user_window, text=user_info)
    user_label.pack()

    status_label = ttk.Label(user_window, text="وضعیت:")
    status_label.pack()

    status_text = scrolledtext.ScrolledText(user_window, wrap=tk.WORD, width=30, height=5)
    status_text.insert(tk.INSERT, user_status)
    status_text.pack()

    national_id_label = ttk.Label(user_window, text="کد ملی:")
    national_id_label.pack()

    national_id_entry = ttk.Entry(user_window)
    national_id_entry.insert(0, user_national_id)
    national_id_entry.pack()

def submit_form():
    name = name_entry.get()
    family = family_entry.get()
    phone = phone_entry.get()
    course = course_entry.get()
    status = status_text.get("1.0", tk.END)
    national_id = national_id_entry.get()
    insert_user(name, family, phone, course, status, national_id)
    name_entry.delete(0, tk.END)
    family_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    status_text.delete("1.0", tk.END)
    national_id_entry.delete(0, tk.END)

def search_button_click():
    name = search_entry.get()
    results = search_users(name)
    search_results.delete(0, tk.END)
    for result in results:
        search_results.insert(tk.END, result)

def list_button_click():
    results = list_users()
    list_results.delete(0, tk.END)
    for result in results:
        list_results.insert(tk.END, result)

root = tk.Tk()
root.title("اطلاعات کاربر")

# Set the RTL text direction
root.tk_setPalette(background="#e1e1e1")
style = ttk.Style()
style.configure("TLabel", font=("BNazanin", 14))
style.configure("TButton", font=("BNazanin", 12))

form_frame = ttk.Frame(root)
form_frame.pack(padx=10, pady=10)

name_label = ttk.Label(form_frame, text="نام:")
name_label.grid(row=0, column=0, sticky=tk.W)

name_entry = ttk.Entry(form_frame)
name_entry.grid(row=0, column=1)

family_label = ttk.Label(form_frame, text="نام خانوادگی:")
family_label.grid(row=1, column=0, sticky=tk.W)

family_entry = ttk.Entry(form_frame)
family_entry.grid(row=1, column=1)

phone_label = ttk.Label(form_frame, text="تلفن:")
phone_label.grid(row=2, column=0, sticky=tk.W)

phone_entry = ttk.Entry(form_frame)
phone_entry.grid(row=2, column=1)

course_label = ttk.Label(form_frame, text="دوره:")
course_label.grid(row=3, column=0, sticky=tk.W)

course_entry = ttk.Entry(form_frame)
course_entry.grid(row=3, column=1)

status_label = ttk.Label(form_frame, text="وضعیت:")
status_label.grid(row=4, column=0, sticky=tk.W)

status_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, width=30, height=5)
status_text.grid(row=4, column=1)

national_id_label = ttk.Label(form_frame, text="کد ملی:")
national_id_label.grid(row=5, column=0, sticky=tk.W)

national_id_entry = ttk.Entry(form_frame)
national_id_entry.grid(row=5, column=1)

submit_button = ttk.Button(form_frame, text="ثبت", command=submit_form)
submit_button.grid(row=6, column=1)

search_frame = ttk.Frame(root)
search_frame.pack(padx=10, pady=10)

search_label = ttk.Label(search_frame, text="جستجو:")
search_label.grid(row=0, column=0, sticky=tk.W)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(search_frame, text="جستجو", command=search_button_click)
search_button.grid(row=0, column=2)

search_results = tk.Listbox(search_frame)
search_results.grid(row=1, column=0, columnspan=3)

list_frame = ttk.Frame(root)
list_frame.pack(padx=10, pady=10)

list_button = ttk.Button(list_frame, text="لیست کاربران", command=list_button_click)
list_button.grid()

list_results = tk.Listbox(list_frame)
list_results.grid()

list_results.bind('<Double-Button-1>', lambda event: open_user_window(list_results.get(tk.ACTIVE)))

root.mainloop()
conn.close()
