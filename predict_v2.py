from rule_based_classifier import Article
from common import channel_name_to_id
from tqdm import tqdm
from datetime import date
import itertools
import csv

article_id_to_info = {}

for line in tqdm(open('data/article_info/20180612', encoding='utf-8')):
    if len(line.split('\t')) != 5:
        print(line)
        continue
    push_time, inner_unique_id, teg_channel, pub_site_name, quality_score = line.split('\t')
    quality_score = quality_score.strip()
    if push_time and inner_unique_id and teg_channel and pub_site_name and quality_score and float(quality_score) >= 3:
        push_time = date.fromtimestamp(int(push_time))
        article_id_to_info[inner_unique_id] = Article('', channel_name_to_id[teg_channel], push_time, pub_site_name)


f_output = open('predict.txt', 'w', encoding='utf-8')
writer = csv.writer(f_output, delimiter='\t')
writer.writerow(['docid', 'cid', 'author', 'time', 'positive', 'score'])

i = 0
for a, b in zip(itertools.chain(open('data/20180612.positive', encoding='utf-8'), open('data/20180612.negative', encoding='utf-8')), open('data/prediction_3_64_trunc', encoding='utf-8')):
    inner_id, rest = a.split('\t', 1)
    positive = 1 if i < 34431 else -1
    i += 1
    if inner_id in article_id_to_info:
        article = article_id_to_info[inner_id]
        score = float(b)
        writer.writerow([inner_id, article.channel_id, article.author, article.push_time, positive, score])

f_output.close()
