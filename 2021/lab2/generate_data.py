import json
import codecs

from mimesis import Person
from mimesis.enums import Gender
import random
from tqdm import trange
import os
import argparse
from pathlib import Path
from os.path import join
from mimesis.schema import Field, Schema
from mimesis import Person
from mimesis import builtins

custom_providers = (builtins.RussiaSpecProvider,)

field = Field('ru', seed=0, providers=custom_providers)

d = [[("email", 'email'),
     ('telephone', 'telephone')],
     [('weight', 'weight'),
      ('height', 'height'), ],
     [('snils', 'snils'),
     ('inn', 'inn'), ],
     [('passport_series', 'passport_series'),
     ('passport_number', 'passport_number')],
     [('university', 'university'),
     ('occupation', 'occupation')],
     [('age', 'age'),
     ('work_experience', 'work_experience')],
     [('academic_degree', 'academic_degree'),
     ('political_views', 'political_views')],
     [('worldview', 'worldview'),
     ('blood_type', 'blood_type')],
     [('address', 'address'),
     ('id', 'uuid')]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--opt", help="количество вариантов",
                        type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument(
        "--count", help="количество записей в файле", type=int, required=True)
    parser.add_argument(
        "--output", help="выходная директория", type=str, required=True)
    args = parser.parse_args()

    path = Path(args.output)
    if path.is_dir():
        random.seed(args.seed)
        for option in trange(1, args.opt+1):
            count = 0
            opt = format(option-1, '010b')
            with open(join(path, str(option)+'.txt'), 'w+', encoding='windows-1251') as f:
                f.write("[")
                for i in trange(args.count):
                    description = (
                        lambda: {
                            d[0][int(opt[-1])][0]: field(d[0][int(opt[-1])][1]),
                            d[1][int(opt[-2])][0]: field(d[1][int(opt[-2])][1]),
                            d[2][int(opt[-3])][0]: field(d[2][int(opt[-3])][1]),
                            d[3][int(opt[-4])][0]: field(d[3][int(opt[-4])][1]),
                            d[4][int(opt[-5])][0]: field(d[4][int(opt[-5])][1]),
                            d[5][int(opt[-6])][0]: field(d[5][int(opt[-6])][1]),
                            d[6][int(opt[-7])][0]: field(d[6][int(opt[-7])][1]),
                            d[7][int(opt[-8])][0]: field(d[7][int(opt[-8])][1]),
                            d[8][int(opt[-9])][0]: field(d[8][int(opt[-9])][1]),
                        }
                    )
                    schema = Schema(schema=description)
                    res = schema.create(iterations=1)
                    json.dump(res[0],f, ensure_ascii=False)
                    if i < args.count-1 :
                        f.write(",\n")
                    else:
                        f.write("\n")
                f.write("]")
    else:
        print("Выходной каталог не существует.")
