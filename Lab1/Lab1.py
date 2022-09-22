import os
import requests
import re

URL = 'https://yandex.ru/images/'
html_page = requests.get(URL+'search?text=' + 'tiger')
a = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', html_page.text)
print(a)
