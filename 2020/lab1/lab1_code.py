from collections import Counter
import re
import os

print('Прикладное программирование. Лабораторная работа №1')
print('Введите путь к входному текстовому файлу:')
input_path = input('>>')
if not os.path.isfile(input_path):  # 1.проверка существования файла
    input_path = 'input.txt'
print('Введите путь к выходному текстовому файлу:')
output_path = input('>>')                   # 1.проверка возможности создания файла
if not os.path.exists(output_path) and not os.access(os.path.dirname(output_path), os.W_OK):
    output_path = 'output.txt'
print('Введите количество слов для вывода:')
words_count = input('>>')
if re.match(r'^\d+$',words_count) is not None:  # 2.регекс проверка на положительное целое
    words_count = int(words_count)
else:
    words_count = 4

print('====================================================')
print(f'Входной файл: {input_path}\nВыходной файл: {output_path}\nЧисло слов: {words_count}')  # 3.форматный вывод
print('====================================================')

file_input = open('input.txt', 'r', encoding="utf8")  # 4.работа с файлами - чтение из файла с указанием кодировки
lines = file_input.readlines()
all_text = ''.join(lines).lower()  # 5.работа со строками
words = re.findall(r'\b\w+\b', all_text)  # 2.регекс отдельных слов
word_counts = Counter(words)  # 6.подсчет слов и отбор самых частых
top_words = word_counts.most_common(words_count)

top_four_text= []
for i in range(0, len(top_words)): # 5.работа со строками и кортежами
    top_four_text.append(''.join(top_words[i][0] + ' - ' + str(top_words[i][1])) + '\n')
file_output = open('output.txt', 'w')  # 4.работа с файлами - запись в файл
file_output.writelines(top_four_text)

# итог - 6 навыков:
# 1. работа с фс - проверка валидности путей,
# 2. регекс,
# 3. консольный ввод-вывод - считывание параметров, форматный вывод,
# 4. работа с файлами - открытие, создание, запись, кодировка,
# 5. работа со структурами языка - массивами/строками/кортежами,
# 6. collections - поиск наиболее популярных выражений
