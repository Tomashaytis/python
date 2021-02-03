import time
import datetime
from watchdog.observers import Observer #Python API library and shell utilities to monitor file system events.
from watchdog.events import FileSystemEventHandler


def on_created(event):
    print(f"{datetime.datetime.now()}: {event.src_path} has been created") # форматированные строковые литералы
                                                                           # Выражения оцениваются по мере выполнения
                                                                           # и затем форматируются при помощи протокола
                                                                           # __format__


def on_deleted(event):
    print(f"{datetime.datetime.now()}: {event.src_path} has been deleted")


def on_modified(event):
    print(f"{datetime.datetime.now()}: {event.src_path} has been modified")


def on_moved(event):
    print(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


if __name__ == "__main__": # указываем, какая область кода не будет выполняться,
                           # если наш модуль импортирован в другой скрипт
    # patterns = "*"
    # ignore_patterns = ""
    # ignore_directories = False
    # case_sensitive = True
    # event_handler = PatternMatchingEventHandler
    event_handler = FileSystemEventHandler() #создаем обработчик, который реагирует на поступление определенного события
    # только он ничего не умеет, так что придется его научить теми процедурами, которые мы написали ранее:
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    path = "dir_to_watch"
    go_recursively = True
    observer = Observer() # создаем наблюдатель, определяет зависимость "один-ко-многим"
                          # между объектами так, что при изменении состояния одного объекта
                          # все зависящие от него объекты уведомляются и обновляются автоматически
    observer.schedule(event_handler, path, recursive=go_recursively)
    # Observer является относительно далеким потомком threading.Thread,
    # соотвественно после вызова start() мы получаем фоновый поток,
    # следящий за изменениями.
    # Так что если скрипт сразу завершится, то ничего толкового мы не получим.
    observer.start()
    print(f"{datetime.datetime.now()}: started watching {path}")
    try:
        while True:
            time.sleep(1)# поддерживаем основной поток приложения в живом состоянии
    except KeyboardInterrupt:
        observer.stop()
        observer.join()# сказать про корректное завершение потока, в котором обитает обсервер
