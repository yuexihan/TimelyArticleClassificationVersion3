from rule_based_classifier import CGeneralProc, Article
from common import channel_name_to_id
from tqdm import tqdm
import os
from datetime import date
import re

article_id_to_info = {}
folder = 'article_info'
for file_name in tqdm(os.listdir(folder)):
    if file_name.startswith('.'):
        continue
    for line in tqdm(open(os.path.join(folder, file_name), encoding='utf-8')):
        line = line.strip()
        try:
            push_time, inner_unique_id, teg_channel, pub_site_name = line.split('\t')
            if push_time and inner_unique_id and teg_channel and pub_site_name:
                push_time = date.fromtimestamp(int(push_time))
                article_id_to_info[inner_unique_id] = Article('', channel_name_to_id[teg_channel], push_time, pub_site_name)
        except:
            continue

f_positive = open('positive.txt', 'w', encoding='utf-8')
f_negative = open('negative.txt', 'w', encoding='utf-8')
general_proc = CGeneralProc('kd_content_mining.xml')
blank = re.compile(r'\s')
folder = 'article_tokens'
for file_name in tqdm(os.listdir(folder)):
    if file_name.startswith('.'):
        continue
    for line in tqdm(open(os.path.join(folder, file_name), encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        rest = rest.strip()
        if inner_id in article_id_to_info and rest:
            rest = blank.sub('', rest)
            article = article_id_to_info[inner_id]
            article.text = rest
            if general_proc.is_timely(article):
                f_positive.write(line)
            else:
                f_negative.write(line)
