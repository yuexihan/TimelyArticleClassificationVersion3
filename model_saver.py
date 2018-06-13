import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_string('load', 'data/model_2_64', 'file to load model')
flags.DEFINE_string('save', 'data/online_2_64', 'file to save model')

FLAGS = flags.FLAGS

with tf.Session() as sess:
    saver = tf.train.import_meta_graph(FLAGS.load + '.meta')
    saver.restore(sess, FLAGS.load)
    builder = tf.saved_model.builder.SavedModelBuilder(FLAGS.save)

    builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING])