import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import ntpath

# covid_06.10.20.xlsx
print('Прикладное программирование. Лабораторная работа №2')  # 1.консольный вывод
print('Введите путь к входному файлу:')
file_name = input('>>')  # 1.считывание параметров
if not os.path.exists(file_name):  # 2.проверка существования файла
    sys.exit('Ошибка! Файла не существует')  # 3.терминация программы с выводом ошибки
if not file_name.endswith(('xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt')):  # 4.проверка расширения
    sys.exit('Ошибка! Неверный формат файла')
print('Введите индекс листа, с которого необходимо считать данные, начиная с 0:')
ind = int(input('>>'))
if ind < 0:
    sys.exit('Ошибка! Введено не целое чило')

dataframe = pd.read_excel(file_name, index_col=ind)  # 5.чтение из таблицы
print('====================================================')
print('Файл: ' + ntpath.basename(file_name))  # 4.выделение имени файла из пути
print('Столбцов: ' + str(len(dataframe.columns)))  # 5.вывод информации о столбцах
for col in dataframe.columns:
    print('   ' + col)
print('Строк: ' + str(len(dataframe.index)))  # 5.вывод информации о строках
print('====================================================')
top_sick = dataframe.nlargest(5, dataframe.columns[1]).iloc[:, [0, 1]]  # 5.поиск по датафрейму
top_heal = dataframe.nlargest(5, dataframe.columns[2]).iloc[:, [0, 2]]
top_dead = dataframe.nlargest(5, dataframe.columns[3]).iloc[:, [0, 3]]
bottom_sick = dataframe.nsmallest(5, dataframe.columns[1]).iloc[:, [0, 1]]
bottom_heal = dataframe.nsmallest(5, dataframe.columns[2]).iloc[:, [0, 2]]
bottom_dead = dataframe.nsmallest(5, dataframe.columns[3]).iloc[:, [0, 3]]

fig, axes = plt.subplots(6, 1, figsize=(12, 6))  # 6.визуализация - несколько диаграмм в одном окне
top_sick.plot.barh(x=0, y=1, color='red', ax=axes[0])  # 6.визуализация - отрисовка столбчатой диаграммы
top_heal.plot.barh(x=0, y=1, color='green', ax=axes[1])
top_dead.plot.barh(x=0, y=1, color='black', ax=axes[2])
bottom_sick.plot.barh(x=0, y=1, color='green', ax=axes[3])
bottom_heal.plot.barh(x=0, y=1, color='red', ax=axes[4])
bottom_dead.plot.barh(x=0, y=1, color='black', ax=axes[5])
for ax in axes:  # 6.визуализация - сокрытие элементов даграммы
    ax.get_legend().set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('')
fig.tight_layout()
plt.show()

# итог - 5 навыков:
# 1. консольный ввод-вывод - считываение параметров, ввод/вывод данных
# 2. работа с фс - проверка валидности путей,
# 3. работа со средствами системы - терминация программы при невыполнении условия,
# 4. работа с ntpath - выделение расширения файла
# 5. работа с pandas - чтение из excel файла, получение информации о составе датафрейма, селект данных в датафрейме
# 6. работа с matplotlib - отрисовка диаграммы, вывод нескольких диаграмм в одном окне, сокрытие элементов диаграммы