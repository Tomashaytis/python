import os
from tkinter import filedialog, Label, Button, Tk
from PIL import Image, ImageTk
from skimage import io, feature


def open_image():
    global panel_original, panel_processed, btn_save, path, img_processed  # работа с референсами
    path = filedialog.askopenfilename()  # работа с диалогами
    if len(path) > 0:
        img_original = io.imread(path)  # обработка изображений
        img_processed = feature.canny(img_original)  # потенциальное место для создания вариантов - разные фильтры

        img_original_pil = Image.fromarray(img_original)  # преобразование изображений в формат для демонстрации
        img_processed_pil = Image.fromarray(img_processed)
        img_original_tk = ImageTk.PhotoImage(img_original_pil)
        img_processed_tk = ImageTk.PhotoImage(img_processed_pil)

        if panel_original is None or panel_processed is None:
            panel_original = Label(image=img_original_tk)  # работа с созданием гуйни
            panel_original.image = img_original_tk
            panel_original.grid(row=0, column=0, padx=10, pady=10)  # размещение элементов гуйни

            panel_processed = Label(image=img_processed_tk)
            panel_processed.image = img_processed_tk
            panel_processed.grid(row=0, column=1, padx=10, pady=10)

            btn_save = Button(root, text="Сохранить результат", command=save_result)
            btn_save.grid(row=1, column=1, padx=10, pady=10)
            btn_open.grid(row=1, column=0, padx=10, pady=10)
        else:
            panel_original.configure(image=img_original_tk)
            panel_original.image = img_original_tk
            panel_processed.configure(image=img_processed_tk)
            panel_processed.image = img_processed_tk


def save_result():
    global img_processed, path
    if img_processed is not None:
        file = filedialog.asksaveasfile(mode='w', defaultextension=os.path.splitext(path)[1])  # парсинг пути к файлу
        if file:
            io.imsave(file.name, img_processed)


root = Tk()
root.winfo_toplevel().title("Прикладное программирование")
btn_save = None
img_processed = None
path = None
panel_original = None
panel_processed = None

btn_open = Button(root, text="Открыть изображение", command=open_image)
btn_open.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()
# итог - 7 мест, где студент может обосраться