import random


class Loader(object):
    def __init__(self, sanity_check=False):
        self.sanity_check = sanity_check
        self.default_vec = [0] * 100
        self.w2id, self.id2v = self.load_word_vector()
        self.p_train = self.load_data('data/positive.train', 1)
        self.n_train = self.load_data('data/negative.train', 0)
        self.test = self.load_data('data/positive.test', 1) + self.load_data('data/negative.test', 0)
        self.p_i = 0
        self.n_i = 0
        self.w2id = [([i], w) for w, i in self.w2id.items()]
        print('finish initialize data loader')

    def load_word_vector(self):
        f = open('data/words_100.vec', encoding='utf-8')
        w2id = {'<UNKNOWN>': 0}
        id2v = [[0.] * 100]
        f.readline()
        for line in f:
            line = line.rstrip().split(' ')
            assert len(line) == 101
            w = line[0]
            v = [float(x) for x in line[1:]]
            w2id[w] = len(w2id)
            id2v.append(v)
            if self.sanity_check:
                if len(w2id) > 10000:
                    break
        return w2id, id2v

    def load_data(self, file_name, label):
        f = open(file_name, encoding='utf-8')
        data = []
        for line in f:
            _, rest = line.split('\t', 1)
            words = rest.split()[:500]
            vectors = []
            for w in words:
                if w in self.w2id:
                    vectors.append(self.w2id[w])
                else:
                    vectors.append(0)
            data.append((vectors, label))
        return data

    def next_batch(self):
        inputs = []
        lens = []
        labels = []

        for _ in range(32):
            if self.p_i == 0:
                random.shuffle(self.p_train)
            input, label = self.p_train[self.p_i]
            self.p_i = (self.p_i + 1) % len(self.p_train)
            inputs.append(input)
            lens.append(len(input))
            labels.append(label)

        for _ in range(32):
            if self.n_i == 0:
                random.shuffle(self.n_train)
            input, label = self.n_train[self.n_i]
            self.n_i = (self.n_i + 1) % len(self.n_train)
            inputs.append(input)
            lens.append(len(input))
            labels.append(label)

        max_len = max(lens)
        self.padding(inputs, max_len)

        return inputs, lens, labels

    def padding(self, inputs, max_len):
        for input in inputs:
            input.extend([0] * (max_len - len(input)))
