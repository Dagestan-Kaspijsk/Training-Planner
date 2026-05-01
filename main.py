import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

DATA_FILE = 'trainings.json'

# --- Загрузка данных из JSON ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            trainings = json.load(f)
        except json.JSONDecodeError:
            trainings = []
else:
    trainings = []

# --- Создание главного окна ---
root = tk.Tk()
root.title("Training Planner")

# --- Функция добавления тренировки ---
def add_training():
    date = date_entry.get().strip()
    tr_type = type_entry.get().strip()
    duration = duration_entry.get().strip()

    if not date or not tr_type or not duration:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
        return

    # Валидация даты (ГГГГ-ММ-ДД)
    if not re.match(r"\d{4}-\d{2}-\d{2}", date):
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД (например: 2024-05-01).")
        return

    # Валидация длительности (положительное число)
    try:
        dur_num = int(duration)
        if dur_num <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным целым числом.")
        return

    # Добавление записи в список и сохранение в JSON
    new_training = {"date": date, "type": tr_type, "duration": dur_num}
    trainings.append(new_training)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(trainings, f, ensure_ascii=False, indent=4)

    # Обновление таблицы и очистка полей ввода
    update_table()
    date_entry.delete(0, 'end')
    type_entry.delete(0, 'end')
    duration_entry.delete(0, 'end')

# --- Функция фильтрации ---
def apply_filter():
    filter_date = filter_date_entry.get().strip()
    filter_type = filter_type_entry.get().strip().lower()

    filtered = []
    for tr in trainings:
        match_date = True if not filter_date else (tr['date'] == filter_date)
        match_type = True if not filter_type else (filter_type in tr['type'].lower())
        if match_date and match_type:
            filtered.append(tr)
    display_trainings(filtered)

# --- Функция обновления таблицы ---
def update_table():
    display_trainings(trainings)

def display_trainings(trainings_list):
    for i in tree.get_children():
        tree.delete(i)
    for tr in trainings_list:
        tree.insert('', 'end', values=(tr['date'], tr['type'], tr['duration']))

# --- Создание виджетов интерфейса ---
frame = ttk.Frame(root, padding="10")
frame.pack(fill='x')

ttk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky='w', pady=2)
date_entry = ttk.Entry(frame)
date_entry.grid(row=0, column=1, sticky='ew', pady=2)

ttk.Label(frame, text="Тип тренировки:").grid(row=1, column=0, sticky='w', pady=2)
type_entry = ttk.Entry(frame)
type_entry.grid(row=1, column=1, sticky='ew', pady=2)

ttk.Label(frame, text="Длительность (мин):").grid(row=2, column=0, sticky='w', pady=2)
duration_entry = ttk.Entry(frame)
duration_entry.grid(row=2, column=1, sticky='ew', pady=2)

btn_frame = ttk.Frame(frame)
btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
ttk.Button(btn_frame, text="Добавить тренировку", command=add_training).pack(side='left', padx=5)

# --- Блок фильтрации ---
filter_frame = ttk.LabelFrame(root, text="Фильтр", padding="5")
filter_frame.pack(fill='x', pady=5)

ttk.Label(filter_frame, text="Дата:").grid(row=0, column=0, sticky='w')
filter_date_entry = ttk.Entry(filter_frame)
filter_date_entry.grid(row=0, column=1, sticky='ew')

ttk.Label(filter_frame, text="Тип:").grid(row=0, column=2, sticky='w', padx=(10,0))
filter_type_entry = ttk.Entry(filter_frame)
filter_type_entry.grid(row=0, column=3, sticky='ew')

ttk.Button(filter_frame, text="Применить фильтр", command=apply_filter).grid(row=0, column=4, padx=5)

# --- Таблица для отображения данных ---
tree = ttk.Treeview(root, columns=("date", "type", "duration"), show='headings')
tree.heading("date", text="Дата")
tree.heading("type", text="Тип")
tree.heading("duration", text="Длительность (мин)")
tree.column("date", anchor='center', width=120)
tree.column("type", anchor='center', width=150)
tree.column("duration", anchor='center', width=120)
tree.pack(fill='both', expand=True, padx=10, pady=5)

# --- Запуск приложения ---
update_table()  # Загрузка данных при старте
root.mainloop()