import os
import re
from os.path import join
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)  # 1.flask - создание экземпляра и конфига к нему
app.config['LAB_DIR'] = 'lab3'
app.config['UPLOAD_DIR'] = 'upload'  # 6.работа со словарями
app.config['ALLOWED_EXTENSION'] = '.png'  # потенциальное место для разных вариантов - .jpeg, .tiff, .bmp и т.д.


@app.route("/")
def index():
    return render_template('index.html')  # 1.flask - работа с рендерингом шаблонов


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        if re.search(app.config['ALLOWED_EXTENSION'] + '$',
                     uploaded_file.filename) is not None:  # 4.регекс
            uploaded_file.save(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR'], uploaded_file.filename))
        else:
            return redirect(url_for('extension_err',  # 1.flask - роутинг с параметрами
                                    allowed=app.config['ALLOWED_EXTENSION'],
                                    forbidden=os.path.splitext(uploaded_file.filename)[1]))  # 3.работа с экстеншенами
    return redirect(url_for('index'))  # 1.flask - работа с роутингом


@app.route('/extension_err?<string:allowed>&<string:forbidden>')  # 1.flask - работа с url rules
def extension_err(allowed, forbidden):
    return render_template('extension_err.html',  # 1.flask - рендеринг шаблона с передачей параметров
                           allowed=allowed,
                           forbidden=forbidden)


@app.route('/display')
def display():
    files = [join(app.config['UPLOAD_DIR'], f)  # 5.работа с файлами/директориями
             for f in os.listdir(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR']))
             if os.path.isfile(join(app.config['LAB_DIR'], app.config['UPLOAD_DIR'], f))]
    return render_template('display.html', images=files)


if __name__ == "__main__":
    app.run()

# итог - 6 навыков:
# 1. flask - запуск, конфиги, роутинг, рендеринг, передача параметров, url rules, post-запросы,
# 2. html - верстка страниц, работа с тегами,
# 3. jinja - работа с шаблонами, синтаксис для передачи параметров в них,
# 4. регекс,
# 5. работа с фс - работа с путями к файлам/директориям/экстеншенами,
# 6. работа со структурами языка - словарями/строками
