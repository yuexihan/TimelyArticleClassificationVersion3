import random

f_p = open('data/positive.txt', 'r', encoding='utf-8')
f_p_train = open('data/positive.train', 'w', encoding='utf-8')
f_p_test = open('data/positive.test', 'w', encoding='utf-8')

lines = []
for line in f_p:
    if len(line.split()) < 50:
        continue
    lines.append(line)
    if len(lines) == 63:
        random.shuffle(lines)
        for x in lines[:8]:
            f_p_train.write(x)
        for x in lines[8:10]:
            f_p_test.write(x)
        lines = []
random.shuffle(lines)
for x in lines[:8]:
    f_p_train.write(x)
for x in lines[8:]:
    f_p_test.write(x)
lines = []
f_p.close()
f_p_train.close()
f_p_test.close()

f_n = open('data/negative.txt', 'r', encoding='utf-8')
f_n_train = open('data/negative.train', 'w', encoding='utf-8')
f_n_test = open('data/negative.test', 'w', encoding='utf-8')

for line in f_n:
    if len(line.split()) < 50:
        continue
    lines.append(line)
    if len(lines) == 144:
        random.shuffle(lines)
        for x in lines[:8]:
            f_n_train.write(x)
        for x in lines[8:10]:
            f_n_test.write(x)
        lines = []
random.shuffle(lines)
for x in lines[:8]:
    f_n_train.write(x)
for x in lines[8:]:
    f_n_test.write(x)
lines = []
f_n.close()
f_n_train.close()
f_n_test.close()
