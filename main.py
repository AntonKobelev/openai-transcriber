import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from threading import Thread

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)

def transcribe():
    input_file = entry_path.get()
    if input_file:
        # Создаем отдельный поток для выполнения процесса с расшифровкой
        thread = Thread(target=transcribe_audio, args=(input_file,))
        thread.start()
        # Показываем индикатор загрузки
        progressbar.start()
        # Ожидаем завершения потока и останавливаем индикатор загрузки
        root.after(100, check_thread, thread)

def transcribe_audio(input_file):
    try:
        command = f"whisper {input_file}"
        subprocess.run(command, shell=True)
        messagebox.showinfo("Конвертация завершена", "Конвертация аудио в текст завершена.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        # Останавливаем индикатор загрузки после завершения процесса
        progressbar.stop()

def check_thread(thread):
    if thread.is_alive():
        # Если поток выполняется, повторяем проверку через 100 миллисекунд
        root.after(100, check_thread, thread)
    else:
        # Если поток завершился, останавливаем индикатор загрузки
        progressbar.stop()

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("OpenAI transcriber")


label_path = tk.Label(root, text="Выберите аудиофайл:")
label_path.pack()

entry_path = tk.Entry(root, width=50)
entry_path.pack()

button_browse = tk.Button(root, text="Обзор", command=choose_file, compound=tk.LEFT, width=40)
button_browse.pack()

button_start = tk.Button(root, text="Старт", command=transcribe, compound=tk.LEFT, width=40)
button_start.pack()

# Добавляем кнопку "Выход из программы"
button_exit = tk.Button(root, text="Выход из программы", command=exit_program, compound=tk.LEFT, width=40)
button_exit.pack()

# Добавляем индикатор загрузки
progressbar = ttk.Progressbar(root, mode="indeterminate")
progressbar.pack(fill="x", padx=7, pady=7)


root.mainloop()
