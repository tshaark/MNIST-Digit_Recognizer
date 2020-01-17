import tensorflow as tf
import numpy as np
from PIL import Image
import os

# On my machine, I have to use the CPU
# because occured some problem when i using the GPU,
# so you can comment the code below for better speed
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

img = np.invert(Image.open("1.png").convert('L')).ravel().reshape((1, 784))


def test_regression():
    tf.reset_default_graph()
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(
            os.path.join(os.path.dirname(__file__), "model/regression/regression-1000.meta"))
        saver.restore(sess, tf.train.latest_checkpoint('./model/regression/'))

        graph = tf.get_default_graph()

        # print all tensor name
        print([n.name for n in graph.as_graph_def().node])

        x = graph.get_tensor_by_name("regression/x:0")
        feed_dict = {x: img}

        regression = graph.get_tensor_by_name("y:0")

        print(sess.run(regression, feed_dict).flatten().tolist())


def test_cnn():
    tf.reset_default_graph()
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(os.path.join(os.path.dirname(__file__), "model/cnn/cnn-1000.meta"))
        saver.restore(sess, tf.train.latest_checkpoint('./model/cnn/'))

        graph = tf.get_default_graph()

        # print all tensor name
        print([n.name for n in graph.as_graph_def().node])

        x = graph.get_tensor_by_name("cnn/x:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")
        feed_dict = {x: img, keep_prob: 1.0}

        cnn = graph.get_tensor_by_name("y_conv:0")
        print(sess.run(cnn, feed_dict).flatten().tolist())


if __name__ == '__main__':
    test_cnn()
    test_regression()
