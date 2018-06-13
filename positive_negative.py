from rule_based_classifier import CGeneralProc, Article
from common import channel_name_to_id
from tqdm import tqdm
import os
from datetime import date
import re

general_proc = CGeneralProc('kd_content_mining.xml')

for day in range(1, 13):
    day = date(2018, 6, day)
    day = day.strftime('%Y%m%d')

    article_id_to_info = {}
    folder = 'data/article_info'
    for line in open(os.path.join(folder, day), encoding='utf-8'):
        if len(line.split('\t')) != 5:
            print(line)
            continue
        push_time, inner_unique_id, teg_channel, pub_site_name, quality_score = line.split('\t')
        if push_time and inner_unique_id and teg_channel and pub_site_name and teg_channel in channel_name_to_id:
            push_time = date.fromtimestamp(int(push_time))
            article_id_to_info[inner_unique_id] = Article('', channel_name_to_id[teg_channel], push_time, pub_site_name)
        else:
            print(line)
            continue

    f_positive = open('data/' + day + '.positive', 'w', encoding='utf-8')
    f_negative = open('data/' + day + '.negative', 'w', encoding='utf-8')
    blank = re.compile(r'\s')
    folder = 'data/article_tokens'
    for line in tqdm(open(os.path.join(folder, day), encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        rest = rest.strip()
        # truncate to 20%
        rest = rest[:(len(rest) // 5)]
        if inner_id in article_id_to_info and rest:
            rest = blank.sub('', rest)
            article = article_id_to_info[inner_id]
            article.text = rest
            if general_proc.is_timely(article):
                f_positive.write(line)
            else:
                f_negative.write(line)
    f_positive.close()
    f_negative.close()