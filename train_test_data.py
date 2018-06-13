import random
from datetime import date
from tqdm import tqdm

f_p = open('data/positive.train', 'w', encoding='utf-8')
f_n = open('data/negative.train', 'w', encoding='utf-8')

for day in range(2, 12):
    day = date(2018, 6, day)
    day = day.strftime('%Y%m%d')
    file = 'data/%s.positive' % day
    ids = []
    for line in tqdm(open(file, encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        if len(line.split()) < 50:
            continue
        ids.append(inner_id)
    random.shuffle(ids)
    ids = set(ids[:10000])
    for line in tqdm(open(file, encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        if inner_id in ids:
            ids.remove(inner_id)
            f_p.write(line)


for day in range(2, 12):
    day = date(2018, 6, day)
    day = day.strftime('%Y%m%d')
    file = 'data/%s.negative' % day
    ids = []
    for line in tqdm(open(file, encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        if len(line.split()) < 50:
            continue
        ids.append(inner_id)
    random.shuffle(ids)
    ids = set(ids[:10000])
    for line in tqdm(open(file, encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        if inner_id in ids:
            ids.remove(inner_id)
            f_n.write(line)
