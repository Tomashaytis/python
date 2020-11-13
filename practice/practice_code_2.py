import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext


class DirectoryEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


def start_observer(path):
    global observer, event_handler
    print(f"{datetime.datetime.now()}: Started watching {path}")
    callback(f"{datetime.datetime.now()}: Started watching {path}")
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


def stop_observer():
    global observer
    observer.stop()
    observer.join()


def callback(message): # функция обратного вызова
                       # на самом деле это никакая непередача исполняемого кода
                       # в качестве одного из параметров другого кода,
                       # просто пропихиваем результат работы обработчика в текстовое поле гуйни
    global sctext_log
    sctext_log.configure(state='normal')
    sctext_log.insert('end', message+'\n')
    sctext_log.configure(state='disabled')
    return True


def exit():
    global root
    stop_observer()
    root.destroy()


def choose_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        start_observer(dir_path)


if __name__ == "__main__":
    event_handler = DirectoryEventHandler()
    observer = Observer()
    path = None
    # объявление элементов интерфейса
    root = tk.Tk()  # главное окно
    root.title("Folder watcher")  # его заголовок
    sv = tk.StringVar()  # текст для  текстбокса
    button_choose_dir = ttk.Button(root, text='Choose a folder', command=choose_dir)  # кнопка выбора директории
    button_exit = ttk.Button(root, text='Exit', command=exit)  # кнопка выхода
    sctext_log = scrolledtext.ScrolledText(root, height=20, width=40, font=("Times New Roman", 12))  # окно журнала
    sctext_log.configure(state='disabled')  # нередактируемое
    # позиционирование элементов
    root.grid()
    root.grid_rowconfigure(0, weight=1)  # включаем реагирование столбцов/строк окна на его масштабирование
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    button_choose_dir.grid(row=1, column=0, pady=10, padx=10, sticky='ws')  # размещаем элементы
    button_exit.grid(row=1, column=1, pady=10, padx=10, sticky='es')
    sctext_log.grid(row=0, columnspan=2, pady=10, padx=10, sticky='nesw')

    root.mainloop()  # запускаем работу основного потока программы - костыльный цикл боьше не нужен
