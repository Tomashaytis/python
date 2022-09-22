import requests
import re

URL = 'https://yandex.ru/images/'
html_page = requests.get(URL+'search?text=' + 'tiger', headers={"User-Agent": "Mozilla/5.0"})
# print(html_page.text)
a = re.findall(r'"origin":\{"w":\w+,"h":\w+,"url":"([^"]+)"\}', html_page.text)
print(a)
