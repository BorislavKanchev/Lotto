import sqlite3
import random
from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # За ttk стиловете
import subprocess
import re
import tkinter as tk
from tkinter import ttk

drawn_users = []

def main():
    def delete_item():
     selected_index = initial_listbox.curselection()
     if selected_index:

        # Извличане на името на изтрития потребител
        deleted_user = initial_listbox.get(selected_index)
        # Изтриване на елемента от листбокса
        initial_listbox.delete(selected_index)

        
        
        # Изтриване на потребителя и от базата данни (тук трябва да добавите кода за изтриване)
        delete_user_from_database(deleted_user)
        

    def on_right_click(event):
        # Създаване на контекстно меню
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Изтрий", command=delete_item)
        context_menu.post(event.x_root, event.y_root)
    # Създаване на прозорец
    root = Tk()

    # Получаване на размерите на екрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Задаване на размерите на прозореца на 90% от размерите на екрана
    window_width = int(screen_width)
    window_height = int(screen_height)
    root.geometry(f"{window_width}x{window_height}")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.title("Случаен избор на потребител")

    style = ttk.Style()
    style.configure("Red.TButton", foreground="red", padding=5, background="red", font=("Helvetica", 18))
    style.configure("Green.TButton", foreground="green", padding=5, background="green", font=("Helvetica", 18))
    style.configure("Grey.TButton", foreground="grey", padding=5, background="grey", font=("Helvetica", 18))
    style.configure("TListbox", font=("Helvetica", 18))

    button_group = ttk.LabelFrame(root)
    button_group.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Инициализиране на бутона за зареди
    btn_load = ttk.Button(button_group, text="Зареди", command=lambda: load(root, initial_listbox, drawn_listbox, shuffle_textbox, btn_load, btn_start, btn_stop, btn_clear_numbers), style="Green.TButton")
    btn_load.grid(row=0, column=0, padx=10, pady=10)

    # Инициализиране на бутона за старт
    btn_start = ttk.Button(button_group, text="Старт", command=lambda: start(root, initial_listbox, drawn_listbox, shuffle_textbox, btn_start, btn_load, btn_clear_numbers), style="Green.TButton")
    btn_start.grid(row=1, column=0, padx=10, pady=10)

    # Инициализиране на бутона за стоп
    btn_stop = ttk.Button(button_group, text="Избери", command=lambda: stop(root, initial_listbox, drawn_listbox, shuffle_textbox), style="Red.TButton")
    btn_stop.grid(row=2, column=0, padx=10, pady=10)

    btn_save = ttk.Button(button_group, text="Запис", command=save_users_to_file, style="Grey.TButton")
    btn_save.grid(row=3, column=0, padx=10, pady=10)

    # Инициализиране на бутона за изчистване на номерата
    btn_clear_numbers = ttk.Button(button_group, text="Изчисти", command=lambda: clear_number(drawn_listbox, shuffle_textbox), style="Red.TButton")
    btn_clear_numbers.grid(row=4, column=0, padx=10, pady=10)

    btn_close = ttk.Button(button_group, text="Затвори", command=root.quit, style="Grey.TButton")
    btn_close.grid(row=5, column=0, padx=10, pady=10)

    btn_add_user = ttk.Button(button_group, text="Добави потребител", command=lambda: add_user(root, initial_listbox, drawn_listbox, shuffle_textbox, entry_user_name, btn_load, btn_start, btn_stop, btn_clear_numbers), style="Grey.TButton")
    btn_add_user.grid(row=6, column=0, padx=10, pady=10)

    entry_user_name = Entry(button_group, width=40, font=("Helvetica", 12))
    entry_user_name.grid(row=7, column=0, padx=10, pady=10)

    initial_listbox = Listbox(root, height=50, width=25, selectmode=SINGLE, font=("Helvetica", 14))
    initial_listbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    initial_listbox.bind('<Double-1>', lambda event: double_click_handler(event, initial_listbox, drawn_listbox))
    initial_listbox.bind("<Button-3>", on_right_click)

    shuffle_textbox = Text(root, height=1, width=25, wrap=WORD)
    shuffle_textbox.grid(row=0, column=2, columnspan=4, padx=10, pady=10)
    shuffle_textbox.configure(foreground="red", font=("Helvetica", 24))

    drawn_listbox = Listbox(root, height=50, width=25, selectmode=SINGLE, font=("Helvetica", 16))
    drawn_listbox.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")
    drawn_listbox.bind('<Double-1>', lambda event: double_click_handler1(event, initial_listbox, drawn_listbox))

    clear_number(drawn_listbox, shuffle_textbox)

    # Стартиране на приложението
    root.mainloop()
    

def delete_user_from_database(user_name):
    # Свържете се с базата данни
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Изтрийте записа от базата данни по име
    cursor.execute("DELETE FROM users WHERE name=?", (user_name,))

    # Потвърдете транзакцията
    conn.commit()

    # Затворете връзката с базата данни
    conn.close() 
    messagebox.showerror("Изтриване", f"{user_name} е изтрит!")  

    
def add_user(root, initial_listbox, drawn_listbox, shuffle_textbox, entry_user_name, btn_load, btn_start, btn_stop, btn_clear_numbers):
    load(root, initial_listbox, drawn_listbox, shuffle_textbox, btn_load, btn_start, btn_stop, btn_clear_numbers)
    
    # Извличане на името на потребителя от текстовото поле
    user_name = entry_user_name.get()

    if user_name:
        # Отваряне на връзката към базата данни
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()

        # Проверка дали потребителят вече съществува в базата данни
        cursor.execute("SELECT * FROM users WHERE name = ?", (user_name,))
        existing_user = cursor.fetchone()

        if not existing_user:
            # Добавяне на новия потребител в базата данни
            cursor.execute("INSERT INTO users (name, number) VALUES (?, NULL)", (user_name,))
            connect.commit()

            # Добавяне на новия потребител в първия списък
            initial_listbox.insert(END, user_name)

            # Изчистване на текстовото поле след успешно добавяне
            entry_user_name.delete(0, END)
        else:
            messagebox.showerror("Грешка", "Този потребител вече съществува в базата данни!")

        # Затваряне на връзката към базата данни
        connect.close()
    else:
        messagebox.showerror("Грешка", "Моля, въведете име на потребител!")

    # Фокусирайте текстовото поле след добавянето
    entry_user_name.focus()

def double_click_handler1(event, initial_listbox, drawn_listbox):
    # Извличане на избрания потребител от втория списък
    selected_user_index = drawn_listbox.curselection()
    if selected_user_index:
        selected_user_index = selected_user_index[0]
        selected_user = drawn_listbox.get(selected_user_index)

        # Извличане на името на избрания потребител
        selected_user_name = selected_user.split(".")[1].strip()

        # Добавете името на потребителя към първия списък
        initial_listbox.insert(END, selected_user_name)
        items = list(initial_listbox.get(0, "end"))  # Вземете всички елементи от листбокса като списък
        items.sort()  # Сортирайте списъка по азбучен ред
        initial_listbox.delete(0, "end")  # Изчистете всички елементи от листбокса
        for item in items:
          initial_listbox.insert("end", item)  # Вмъкнете сортирания списък обратно в листбокса 

        # Изтрийте потребителя от втория списък
        drawn_listbox.delete(selected_user_index)

        # Изтрийте номера на потребителя от базата данни
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET number = NULL WHERE name = ?", (selected_user_name,))
        connect.commit()
        connect.close()


def remove_user(user_number, initial_listbox, drawn_listbox):
    global drawn_users

    # Изтриване на потребителя от втория листбокс
    selected_user_index = None
    for i in range(drawn_listbox.size()):
        user = drawn_listbox.get(i)
        user_num_match = re.match(r'^(\d+)\.', user)
        if user_num_match:
            user_num = int(user_num_match.group(1))
            if user_num == user_number:
                selected_user_index = i
                break

    if selected_user_index is not None:
        drawn_listbox.delete(selected_user_index)

    # Изтриване на номера на потребителя от базата данни
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE users SET number = NULL WHERE name = ?", (user.split(".")[1].strip(),))
    connect.commit()
    connect.close()

    # Добавяне на потребителя към списъка със свободни потребители
    user_name = None
    for i in range(initial_listbox.size()):
        user = initial_listbox.get(i)
        user_num_match = re.match(r'^(\d+)\.', user)
        if user_num_match:
            user_num = int(user_num_match.group(1))
            if user_num == user_number:
                user_name = user.split(".")[1].strip()
                break

    if user_name:
        initial_listbox.insert(END, f"{user_number}. {user_name}")
        drawn_users.remove(user_name)

def clear_number(drawn_listbox, shuffle_textbox):
    # Отваряне на връзката към базата данни
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    # Записване на NULL във всички записи от колоната "number" в таблицата
    cursor.execute("UPDATE users SET number = NULL")

    # Потвърждаване на промените и затваряне на връзката към базата данни
    connect.commit()
    connect.close()

    # Изчистване на втория листбокс и текстовото поле
    if drawn_listbox:
        drawn_listbox.delete(0, END)
    if shuffle_textbox:
        shuffle_textbox.delete(1.0, END)

    messagebox.showinfo("Изтриване на подреждането", "Подредбата е изтрита!")    

def double_click_handler(event, initial_listbox, drawn_listbox):
    global global_initial_listbox
    # Извличане на избрания потребител от първия списък
    selected_user_index = initial_listbox.curselection()
    if selected_user_index:
        selected_user_index = selected_user_index[0]
        selected_user = initial_listbox.get(selected_user_index)

        # Изчисляване на номера на изтегления потребител
        drawn_user_number = drawn_listbox.size() + 2

        # Добавяне на номер и потребителя във втория списък
        drawn_listbox.insert(END, f"{drawn_user_number}. {selected_user}")

        # Запис на номера на избрания потребител в базата данни
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET number = ? WHERE name = ?", (drawn_user_number, selected_user))
        connect.commit()
        connect.close()

        # Добавяне на потребителя към списъка с изтеглените
        drawn_users.append(selected_user)

        # Премахване на избрания потребител от първия списък
        initial_listbox.delete(selected_user_index)    

def save_users_to_file():
    # Отваряне на връзката към базата данни
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    # Извличане на данните за потребителите от таблицата, сортирани по номер
    cursor.execute("SELECT name, number FROM users ORDER BY number")
    user_data = cursor.fetchall()

    # Затваряне на връзката към базата данни
    connect.close()

    # Запис на данните в текстов файл
    with open("user_data.txt", "w") as file:
        for user in user_data:
            file.write(f"{user[1]}. {user[0]}\n")

    # Отваряне на текстовия файл с подходящата програма за преглед
    subprocess.Popen(["notepad.exe", "user_data.txt"])  # Заменете "notepad.exe" с желаната програма за преглед на текстови файлове

def load(root, initial_listbox, drawn_listbox, shuffle_textbox, btn_load, btn_start, btn_clear_numbers, btn_stop):
    global global_initial_listbox
    global_initial_listbox = initial_listbox
    # Инициализиране на списъка с изтеглените потребители
    global drawn_users
    if 'drawn_users' not in globals():
        drawn_users = []

    btn_load.config(state=DISABLED)
    btn_start.config(state=DISABLED)
    btn_stop.config(state=DISABLED)
    btn_clear_numbers.config(state=DISABLED)

    # Получаване на всички потребители
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    users.sort()
     # Изчистване на списъка с изтеглени потребители
    initial_listbox.delete(0, END)

    # Изчистване на втория списък
    drawn_listbox.delete(0, END)

    # Изчистване на текстовото поле за разбъркване
    shuffle_textbox.delete(1.0, END)

    # Цикл за извличане на случайни потребители
    for user in users:
        # Проверка дали потребителят е бил изтеглен
        if user[0] not in drawn_users:
            # Добавяне на потребителя в първия списък
            initial_listbox.insert(END, user[0])
    connect.close()         

def start(root, initial_listbox, drawn_listbox, shuffle_textbox, btn_start, btn_load, btn_clear_numbers):
    # Инициализиране на списъка с изтеглените потребители
    global drawn_users
    if 'drawn_users' not in globals():
        drawn_users = []

    btn_start.config(state=DISABLED)
    btn_load.config(state=DISABLED)
    btn_clear_numbers.config(state=DISABLED)

    # Получаване на всички потребители
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Изчистване на списъка с изтеглени потребители
    initial_listbox.delete(0, END)

    # Изчистване на втория списък
    drawn_listbox.delete(0, END)

    # Изчистване на текстовото поле за разбъркване
    shuffle_textbox.delete(1.0, END)

    # Цикл за извличане на случайни потребители
    for user in users:
        # Проверка дали потребителят е бил изтеглен
        if user[0] not in drawn_users:
            # Добавяне на потребителя в първия списък
            initial_listbox.insert(END, user[0])

    # Запускане на таймер за автоматично разбъркване на имената
    shuffle_names(root, initial_listbox, drawn_listbox, shuffle_textbox)    

def shuffle_names(root, initial_listbox, drawn_listbox, shuffle_textbox):
    global drawn_users
    if initial_listbox.size() > 0:
        # Извличане на случайен потребител от първия списък
        random_user_index = random.randint(0, initial_listbox.size() - 1)
        random_user = initial_listbox.get(random_user_index)

        # Извеждане на случайния потребител в текстовото поле
        shuffle_textbox.delete(1.0, END)
        shuffle_textbox.insert(END, random_user)

        # Стартиране на таймер за следващо разбъркване
        root.after(20, lambda: shuffle_names(root, initial_listbox, drawn_listbox, shuffle_textbox))
    else:
        # Изчистване на текстовото поле
        shuffle_textbox.delete(1.0, END)

        # Извеждане на съобщение, че изборът е приключил
        messagebox.showinfo("Изборът приключи", "Всички потребители са изтеглени!")

def stop(root, initial_listbox, drawn_listbox, shuffle_textbox):
    global drawn_users
    if initial_listbox.size() > 0:
        # Извличане на случайен потребител от първия списък
        random_user_index = random.randint(0, initial_listbox.size() - 1)
        random_user = initial_listbox.get(random_user_index)

        # Изчисляване на номера на изтегления потребител
        drawn_user_number = drawn_listbox.size() + 2

        # Добавяне на номер и потребителя във втория списък
        drawn_listbox.insert(END, f"{drawn_user_number}. {random_user}")

        # Запишете номера на избрания потребител в базата данни
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()
        cursor.execute("UPDATE users SET number = ? WHERE name = ?", (drawn_user_number, random_user))
        connect.commit()
        connect.close()

        # Добавяне на потребителя към списъка с изтеглените
        drawn_users.append(random_user)

        # Премахване на случайния потребител от първия списък
        initial_listbox.delete(random_user_index)

if __name__ == "__main__":
    main()