from rule_based_classifier import CGeneralProc, Article
from common import channel_name_to_id
from tqdm import tqdm
import os
from datetime import date
import re
from tf_model import CnnMaxPool, FLAGS, flags
import tensorflow as tf
import csv

article_id_to_info = {}
folder = 'article_info_new'
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

model = CnnMaxPool()
tf.train.Saver().restore(model.sess, FLAGS.save)
loader = model.loader
general_proc = CGeneralProc('kd_content_mining.xml')

f_output = open('predict.txt', 'w', encoding='utf-8')
writer = csv.writer(f_output, delimiter='\t')
blank = re.compile(r'\s')
folder = 'article_tokens_new'
writer.writerow(['docid', 'cid', 'author', 'time', 'positive', 'score'])

articles = []
inputs = []
lens = []
positives = []
docids = []
for file_name in tqdm(os.listdir(folder)):
    if file_name.startswith('.'):
        continue
    for line in tqdm(open(os.path.join(folder, file_name), encoding='utf-8')):
        inner_id, rest = line.split('\t', 1)
        rest = rest.strip()
        if inner_id in article_id_to_info and rest:
            article = article_id_to_info[inner_id]
            article.text = blank.sub('', rest)
            if general_proc.is_timely(article):
                positives.append(1)
            else:
                positives.append(-1)
            words = rest.split()[:500]
            vector = []
            for w in words:
                if w in loader.w2id:
                    vector.append(loader.w2id[w])
                else:
                    vector.append(0)
            inputs.append(vector)
            lens.append(len(vector))
            articles.append(article)
            docids.append(inner_id)
            if len(inputs) >= 128:
                max_len = max(lens)
                loader.padding(inputs, max_len)
                feed_dict = {
                    model.inputs: inputs,
                    model.lens: lens,
                }
                predictions = model.sess.run(model.logits, feed_dict=feed_dict)
                for article, positive, score, inner_id in zip(articles, positives, predictions, docids):
                    writer.writerow([inner_id, article.channel_id, article.author, article.push_time, positive, score])
                articles = []
                positives = []
                inputs = []
                lens = []
                docids = []
    if len(inputs) > 0:
        max_len = max(lens)
        loader.padding(inputs, max_len)
        feed_dict = {
            model.inputs: inputs,
            model.lens: lens,
        }
        predictions = model.sess.run(model.logits, feed_dict=feed_dict)
        for article, positive, score, inner_id in zip(articles, positives, predictions, docids):
            writer.writerow([inner_id, article.channel_id, article.author, article.push_time, positive, score])
