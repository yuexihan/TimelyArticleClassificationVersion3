from tf_model import CnnMaxPool, FLAGS
import tensorflow as tf
model = CnnMaxPool()
tf.train.Saver().restore(model.sess, FLAGS.save)

result = []
inputs = []
lens = []
labels = []
for input, label in model.loader.w2id:
    inputs.append(input)
    lens.append(len(input))
    labels.append(label)
    if len(inputs) >= 128:
        max_len = max(lens)
        model.loader.padding(inputs, max_len)
        feed_dict = {
            model.inputs: inputs,
            model.lens: lens,
        }
        predictions = model.sess.run(model.logits, feed_dict=feed_dict)
        result.extend(zip(labels, predictions))
        inputs = []
        lens = []
        labels = []
if len(inputs) > 0:
    max_len = max(lens)
    model.loader.padding(inputs, max_len)
    feed_dict = {
        model.inputs: inputs,
        model.lens: lens,
    }
    predictions = model.sess.run(model.logits, feed_dict=feed_dict)
    result.extend(zip(labels, predictions))

result.sort(key=(lambda x: x[1]), reverse=True)

with open('words-score-sigmoid.txt', 'wb') as f:
    for w, i in result:
        if isinstance(w, str):
            w = w.encode('utf-8')
        f.write(w)
        f.write(b'\n')
        f.write(str(i).encode('utf-8'))
        f.write(b'\n')
