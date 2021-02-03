import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

                            # отнаследовали
class DirectoryEventHandler(FileSystemEventHandler): # поскольку в питоне все объекты, запилим собственные
    """докстринги пишутся так, но студенты и так должны быть в курсе"""
    def __init__(self): # через __ указывается приватность методов и переменных
                        # только их все равно можно вызывать, лол ->оффтоп
        super().__init__() #вызвали родительский конструктор - он и так вызывается, так что init можно было не писать
    def on_created(self, event): #
        print(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self,event):
        print(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self,event):
        print(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self,event):
        print(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")


def start_observer(path):
    global observer, event_handler # все назначения выполняются в локальной области по умолчанию. При помощи global
                                   # можно объявить переменную доступной для блока кода, следующим за оператором
    observer.schedule(event_handler, path, recursive=True)
    observer.start()


def stop_observer():
    global observer
    observer.stop()
    observer.join()


if __name__ == "__main__":
    event_handler = DirectoryEventHandler()
    observer = Observer()

    path = "dir_to_watch"
    start_observer(path)
    print(f"{datetime.datetime.now()}: is watching {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_observer()
