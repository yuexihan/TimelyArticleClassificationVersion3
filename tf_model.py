import tensorflow as tf
from tf_data_loader import Loader
import time

flags = tf.app.flags
flags.DEFINE_integer('window', 2, 'cnn1d word window size')
flags.DEFINE_integer('channel', 256, 'channel dimension')
flags.DEFINE_integer('word_dimension', 100, 'word dimension')
flags.DEFINE_integer('pos_weight', 1, 'positive sample weight in LR')
flags.DEFINE_integer('epoch', 5, 'train epoch')
flags.DEFINE_float('learning_rate', 1e-3, 'learning rate')
flags.DEFINE_bool('sanity', False, 'sanity check')
flags.DEFINE_string('save', 'data/model', 'file to save model')

FLAGS = flags.FLAGS


class CnnMaxPool(object):
    def __init__(self):
        self.loader = Loader(sanity_check=FLAGS.sanity)
        self.sess = tf.Session()
        self.embedding = tf.constant(self.loader.id2v, dtype=tf.float32)
        self.build_graph()

    def forward(self, inputs):
        # embedding_lookup
        inputs = tf.nn.embedding_lookup(self.embedding, inputs)

        # 一维卷积网络
        with tf.variable_scope('cnn') as scope:
            try:
                conv_W = tf.get_variable(name='conv_W', shape=(FLAGS.window, FLAGS.word_dimension, FLAGS.channel))
                conv_b = tf.get_variable(name='conv_b', shape=FLAGS.channel, initializer=tf.zeros_initializer())
            except ValueError:
                scope.reuse_variables()
                conv_W = tf.get_variable(name='conv_W', shape=(FLAGS.window, FLAGS.word_dimension, FLAGS.channel))
                conv_b = tf.get_variable(name='conv_b', shape=FLAGS.channel, initializer=tf.zeros_initializer())

            conv = tf.sigmoid(tf.nn.conv1d(inputs, conv_W, 1, 'SAME') + conv_b)

        pool = tf.reduce_max(conv, 1)

        # 全连接分类
        with tf.variable_scope('full') as scope:
            try:
                W = tf.get_variable(name='W', shape=(FLAGS.channel, ))
                b = tf.get_variable(name='b', shape=(), initializer=tf.zeros_initializer())
            except ValueError:
                scope.reuse_variables()
                W = tf.get_variable(name='W', shape=(FLAGS.channel, ))
                b = tf.get_variable(name='b', shape=(), initializer=tf.zeros_initializer())
            logits = tf.reduce_sum(tf.multiply(pool, W), 1) + b

        return logits

    def build_graph(self):
        self.inputs = tf.placeholder(tf.int32, (None, None))
        self.lens = tf.placeholder(tf.int32, [None])
        self.labels = tf.placeholder(tf.float32, [None])

        self.logits = self.forward(self.inputs)
        self.loss = tf.reduce_mean(tf.nn.weighted_cross_entropy_with_logits(self.labels, self.logits, FLAGS.pos_weight))
        losses = tf.get_collection('losses')
        if losses:
            self.loss += tf.add_n(losses)

        optimizer = tf.train.AdamOptimizer(FLAGS.learning_rate)
        self.train_step = optimizer.minimize(self.loss)
        self.predictions = tf.cast(tf.greater(self.logits, 0), tf.float32)

    def train(self):
        sess = self.sess
        sess.run(tf.global_variables_initializer())
        last_time = time.time()
        for i in range(FLAGS.epoch):
            for step in range(79304 // 32):
                inputs, lens, labels = self.loader.next_batch()
                feed_dict = {
                    self.inputs: inputs,
                    self.lens: lens,
                    self.labels: labels,
                }
                loss, _ = sess.run([self.loss, self.train_step], feed_dict=feed_dict)
                if step % 50 == 0:
                    print(i, step, loss)
        tf.train.Saver().save(sess, FLAGS.save)

    def test(self, data_set):
        sess = self.sess
        all_1 = 0       # 正样本总数
        get_1 = 0       # 判定为正样本的数目
        right_1 = 0     # 判定为正样本且正确的数目

        inputs = []
        lens = []
        labels = []
        for input, label in data_set:
            inputs.append(input)
            lens.append(len(input))
            labels.append(label)
            if len(inputs) >= 128:
                max_len = max(lens)
                self.loader.padding(inputs, max_len)
                feed_dict = {
                    self.inputs: inputs,
                    self.lens: lens,
                    self.labels: labels,
                }
                predictions = sess.run(self.predictions, feed_dict=feed_dict)
                for p, l in zip(predictions, labels):
                    if p == 1:
                        get_1 += 1
                        if l == 1:
                            right_1 += 1
                    if l == 1:
                        all_1 += 1
                inputs = []
                lens = []
                labels = []
        if len(inputs) > 0:
            max_len = max(lens)
            self.loader.padding(inputs, max_len)
            feed_dict = {
                self.inputs: inputs,
                self.lens: lens,
                self.labels: labels,
            }
            predictions = sess.run(self.predictions, feed_dict=feed_dict)
            for p, l in zip(predictions, labels):
                if p == 1:
                    get_1 += 1
                    if l == 1:
                        right_1 += 1
                if l == 1:
                    all_1 += 1
        if get_1 == 0:
            accuracy = right_1 / (get_1 + 0.1)
        else:
            accuracy = right_1 / get_1
        recall = right_1 / all_1
        if accuracy + recall == 0:
            f1 = 2 * accuracy * recall / (accuracy + recall + 0.1)
        else:
            f1 = 2 * accuracy * recall / (accuracy + recall)
        return accuracy, recall, f1


def main(_):
    model = CnnMaxPool()
    model.train()


if __name__ == '__main__':
    tf.app.run()
