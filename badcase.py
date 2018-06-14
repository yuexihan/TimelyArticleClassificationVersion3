import tensorflow as tf
import itertools

flags = tf.app.flags

flags.DEFINE_string('predictions', 'data/predictions', 'file to save predictions')
flags.DEFINE_string('badcase', 'data/badcase', 'file to save badcases')

FLAGS = flags.FLAGS

f = open(FLAGS.badcase, 'w', encoding='utf-8')
i = 0
for a, b in zip(itertools.chain(open('data/20180612.positve', encoding='utf-8'), open('data/20180612.negative', encoding='utf-8')), open(FLAGS.predictions, encoding='utf-8')):
    if i < 34431 and float(b) < 0 or i >= 34431 and float(b) > 0:
        f.write(a)
        f.write(b)

f.close()