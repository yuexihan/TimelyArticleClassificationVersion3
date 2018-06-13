from tf_model import CnnMaxPool, FLAGS, flags
import tensorflow as tf

flags.DEFINE_string('predictions', 'data/predictions', 'file to save predictions')

model = CnnMaxPool()
tf.train.Saver().restore(model.sess, FLAGS.save)

result = []
inputs = []
lens = []
labels = []
for input, label in model.loader.test:
    inputs.append(input)
    lens.append(len(input))
    labels.append(label)
    if len(inputs) >= 128:
        max_len = max(lens)
        model.loader.padding(inputs, max_len)
        feed_dict = {
            model.inputs: inputs,
            model.lens: lens,
            model.labels: labels,
        }
        predictions = model.sess.run(model.logits, feed_dict=feed_dict)
        result.extend(predictions)
        inputs = []
        lens = []
        labels = []
if len(inputs) > 0:
    max_len = max(lens)
    model.loader.padding(inputs, max_len)
    feed_dict = {
        model.inputs: inputs,
        model.lens: lens,
        model.labels: labels,
    }
    predictions = model.sess.run(model.logits, feed_dict=feed_dict)
    result.extend(predictions)

with open(FLAGS.predictions, 'w', encoding='utf-8') as f:
    for r in result:
        f.write(str(r) + '\n')
