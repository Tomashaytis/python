import random
import string
import argparse
import os
import json
import numpy as np
from tqdm import trange


#     'email' - добавлено
#     'telephone' - добавлено
#     'weight' - добавлено
#     'height' - добавлено
#     'snils' - добавлено
#     'inn' - добавлено
#     'passport_series' - добавлено
#     'passport_number' - добавлено
#     'university' - добавлено
#     'occupation' - добавлено
#     'age' - добавлено
#     'work_experience' - добавлено
#     'academic_degree' - добавлено
#     'political_views' - добавлено
#     'worldview' - добавлено
#     'blood_type' - тут меня уже задушило
#     'address' - добавлено

def degrade_email(dictlist):
    for i in range(0, int(len(dictlist) / 4)):
        dictlist[i]["email"] = dictlist[i]["email"].replace("@", " @ ")
    for i in range(int(len(dictlist) / 4), int(len(dictlist) / 2)):
        dictlist[i]["email"] = dictlist[i]["email"].replace(".", "..")
    for i in range(int(len(dictlist) / 2), int(len(dictlist) / 4) * 3):
        dictlist[i]["email"] = dictlist[i]["email"].replace(".", ",")
    for i in range(int(len(dictlist) / 4) * 3, len(dictlist)):
        dictlist[i]["email"] = dictlist[i]["email"].replace(".com", "")
    return dictlist


def degrade_telephone(dictlist):
    for i in range(0, int(len(dictlist) / 4)):
        dictlist[i]["telephone"] = dictlist[i]["telephone"].replace("-", "")
    for i in range(int(len(dictlist) / 4), int(len(dictlist) / 2)):
        dictlist[i]["telephone"] = dictlist[i]["telephone"].replace("(", "").replace(")", "")
    for i in range(int(len(dictlist) / 2), int(len(dictlist) / 4) * 3):
        dictlist[i]["telephone"] = dictlist[i]["telephone"].replace("+", "")
    for i in range(int(len(dictlist) / 4) * 3, len(dictlist)):
        dictlist[i]["telephone"] = dictlist[i]["telephone"].replace("9", "a")
    return dictlist


def degrade_weight(dictlist):
    for i in range(0, int(len(dictlist) / 4)):
        dictlist[i]["weight"] = random.randint(0, 20)
    for i in range(int(len(dictlist) / 4), int(len(dictlist) / 2)):
        dictlist[i]["weight"] = random.randint(300, 600)
    for i in range(int(len(dictlist) / 2), int(len(dictlist) / 4) * 3):
        dictlist[i]["weight"] = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    for i in range(int(len(dictlist) / 4) * 3, len(dictlist)):
        dictlist[i]["weight"] = random.randint(-600, 0)
    return dictlist


def degrade_height(dictlist):
    for i in range(0, int(len(dictlist) / 4)):
        dictlist[i]["height"] = round(random.uniform(0.0, 1.0), 2)
    for i in range(int(len(dictlist) / 4), int(len(dictlist) / 2)):
        dictlist[i]["height"] = round(random.uniform(2.5, 4.0), 2)
    for i in range(int(len(dictlist) / 2), int(len(dictlist) / 4) * 3):
        dictlist[i]["height"] = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    for i in range(int(len(dictlist) / 4) * 3, len(dictlist)):
        dictlist[i]["height"] = dictlist[i]["height"].replace(".", ",")
    return dictlist


def degrade_snils_inn(dictlist, key):
    for i in range(0, int(len(dictlist) / 2)):
        ind = random.randint(0, len(dictlist[i][key]))
        dictlist[i][key] = dictlist[i][key][:ind] + random.choice(string.ascii_letters) + dictlist[i][key][ind + 1:]
    for i in range(int(len(dictlist) / 2), len(dictlist)):
        dictlist[i][key] = dictlist[i][key][:-1]
    return dictlist


def degrade_passportnumber(dictlist):
    for i in range(0, int(len(dictlist) / 2)):
        ind = random.randint(0, len(str(dictlist[i]['passport_number'])))
        dictlist[i]['passport_number'] = str(dictlist[i]['passport_number'])[:ind] + random.choice(
            string.ascii_letters) + str(dictlist[i]['passport_number'])[ind + 1:]
    for i in range(int(len(dictlist) / 2), len(dictlist)):
        dictlist[i]['passport_number'] = int(dictlist[i]['passport_number'] / 10)
    return dictlist


def degrade_passportseries(dictlist):
    for i in range(0, int(len(dictlist) / 3)):
        dictlist[i]["passport_series"] = dictlist[i]["passport_series"].replace(" ", "")
    for i in range(int(len(dictlist) / 3), 2 * int(len(dictlist) / 3)):
        ind = random.randint(0, len(dictlist[i]["passport_series"]) - 1)
        dictlist[i]["passport_series"] = dictlist[i]["passport_series"][:ind] + random.choice(string.ascii_letters) + \
                                         dictlist[i]["passport_series"][ind + 1:]
    for i in range(2 * int(len(dictlist) / 3), len(dictlist)):
        dictlist[i]["passport_series"] = dictlist[i]["passport_series"][:-1]
    return dictlist


def degrade_age(dictlist):
    for i in range(0, int(len(dictlist) / 4)):
        dictlist[i]["age"] = random.randint(0, 5)
    for i in range(int(len(dictlist) / 4), int(len(dictlist) / 2)):
        dictlist[i]["age"] = random.randint(100, 200)
    for i in range(int(len(dictlist) / 2), int(len(dictlist) / 4) * 3):
        dictlist[i]["age"] = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    for i in range(int(len(dictlist) / 4) * 3, len(dictlist)):
        dictlist[i]["age"] = random.randint(-200, 0)
    return dictlist


def degrade_workexperience(dictlist):
    for i in range(0, int(len(dictlist) / 3)):
        dictlist[i]["work_experience"] = random.randint(100, 200)
    for i in range(int(len(dictlist) / 3), int(len(dictlist) / 3) * 2):
        dictlist[i]["work_experience"] = random.choice(string.ascii_letters)
    for i in range(int(len(dictlist) / 3) * 2, len(dictlist)):
        dictlist[i]["work_experience"] = random.randint(-200, -1)
    return dictlist


def degrade_occupation(dictlist):
    occupations = ["Воин", "Маг", "Охотник", "Шаман", "Друид", "Разбойник", "Паладин", "Чернокнижник", "Жрец", "Монах",
                   "Рыцарь смерти", "Охотник на демонов"]
    for i in range(0, len(dictlist)):
        dictlist[i]["occupation"] = random.choice(occupations)
    return dictlist


def degrade_university(dictlist):
    universities = ["Хогвартс", "Дурмстранг", "Шармбатон", "Кирин-Тор", "Каражан", "Аретуза", "Бан Ард",
                    "Гвейсон Хайль"]
    for i in range(0, len(dictlist)):
        dictlist[i]["university"] = random.choice(universities)
    return dictlist


def degrade_worldview(dictlist):
    worldviews = ["Культ проклятых", "Храм Трибунала", "Девять божеств", "Культ Механикус", "Культ Вечного Огня",
                  "Культ богини Мелитэле", "Культ пророка Лебеды", "Светское гачимученничество"]
    for i in range(0, len(dictlist)):
        dictlist[i]["worldview"] = random.choice(worldviews)
    return dictlist


def degrade_academicdegree(dictlist):
    degrees = ["Великий волшебник", "Великий волхв", "Великий дракон", "Великий казначей", "Великий турок",
               "Великий циклоп", "Великий тиран"]
    for i in range(0, len(dictlist)):
        dictlist[i]["academic_degree"] = random.choice(degrees)
    return dictlist


def degrade_address(dictlist):
    for i in range(0, int(len(dictlist) / 3)):
        dictlist[i]["address"] = dictlist[i]["address"].replace(" ", "")
    for i in range(int(len(dictlist) / 3), 2 * int(len(dictlist) / 3)):
        dictlist[i]["address"] = dictlist[i]["address"].replace(" ", "_")
    for i in range(2 * int(len(dictlist) / 3), len(dictlist)):
        dictlist[i]["address"] = dictlist[i]["address"].replace(" ", ",")
    return dictlist


def degrade_politicalviews(dictlist):
    politicalviews = ["поддерживает Братьев Бури", "поддерживает Имперский легион", "патриот независимой Темерии",
                      "согласен с действиями Гарроша Адского Крика на посту вождя Орды"]
    for i in range(0, len(dictlist)):
        dictlist[i]["political_views"] = random.choice(politicalviews)
    return dictlist


def degrade_file(filename, inpath, outpath):
    data = np.array(json.load(open(os.path.join(inpath, filename), encoding='windows-1251')))
    keys = data[0].keys()
    if 'email' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_email(data[inds])
    if 'telephone' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_telephone(data[inds])
    if 'weight' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_weight(data[inds])
    if 'height' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_height(data[inds])
    if 'snils' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_snils_inn(data[inds], 'snils')
    if 'inn' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_snils_inn(data[inds], 'inn')
    if 'passport_series' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_passportseries(data[inds])
    if 'passport_number' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_passportnumber(data[inds])
    if 'university' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_university(data[inds])
    if 'occupation' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_occupation(data[inds])
    if 'age' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_age(data[inds])
    if 'work_experience' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_workexperience(data[inds])
    if 'academic_degree' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_academicdegree(data[inds])
    if 'political_views' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_politicalviews(data[inds])
    if 'worldview' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_worldview(data[inds])
    if 'address' in keys:
        inds = random.sample(range(len(data)), int(len(data) / 100))
        data[inds] = degrade_address(data[inds])
    with open(os.path.join(outpath, filename), 'w', encoding='windows-1251') as f:
        json.dump(data.tolist(), f, ensure_ascii=False, indent=4, )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", help="входная директория", type=str, required=True)
    parser.add_argument(
        "--output", help="выходная директория", type=str, required=True)
    args = parser.parse_args()
    inpath = args.input
    outpath = args.output
    if os.path.isdir(inpath) and os.path.isdir(outpath):
        files = [f for f in os.listdir(inpath) if os.path.isfile(os.path.join(inpath, f))]
        for j in trange(0, len(files)):
            degrade_file(files[j], inpath, outpath)
    else:
        print("С аргументами беда")
