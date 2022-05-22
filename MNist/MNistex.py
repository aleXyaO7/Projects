import numpy as np
import os
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)
import tensorflow as tf
import tensorflow_datasets as tfds

(x_train, y_train), (x_test, y_test) = tfds.load('mnist', split=['train', 'test'], 
                                                  batch_size=-1, as_supervised=True)

# reshaping
x_train = tf.reshape(x_train, shape=(x_train.shape[0], 784))
x_test  = tf.reshape(x_test, shape=(x_test.shape[0], 784))

ds_train = tf.data.Dataset.from_tensor_slices((x_train, y_train))
# rescaling
ds_train = ds_train.map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y))

class Model(object):
    def __init__(self, hidden1_size, hidden2_size, device=None):
        # layer sizes along with input and output
        self.input_size, self.output_size, self.device = 784, 10, device
        self.hidden1_size, self.hidden2_size = hidden1_size, hidden2_size
        self.lr_rate = 1e-03

        # weights initializationg
        self.glorot_init = tf.initializers.glorot_uniform(seed=42)
        # weights b/w input to hidden1 --> 1
        self.w_h1 = tf.Variable(self.glorot_init((self.input_size, self.hidden1_size)))
        # weights b/w hidden1 to hidden2 ---> 2
        self.w_h2 = tf.Variable(self.glorot_init((self.hidden1_size, self.hidden2_size)))
        # weights b/w hidden2 to output ---> 3
        self.w_out = tf.Variable(self.glorot_init((self.hidden2_size, self.output_size)))

        # bias initialization
        self.b1 = tf.Variable(self.glorot_init((self.hidden1_size,)))
        self.b2 = tf.Variable(self.glorot_init((self.hidden2_size,)))
        self.b_out = tf.Variable(self.glorot_init((self.output_size,)))

        self.variables = [self.w_h1, self.b1, self.w_h2, self.b2, self.w_out, self.b_out]


    def feed_forward(self, x):
        if self.device is not None:
            with tf.device('gpu:0' if self.device=='gpu' else 'cpu'):
                # layer1
                self.layer1 = tf.nn.sigmoid(tf.add(tf.matmul(x, self.w_h1), self.b1))
                # layer2
                self.layer2 = tf.nn.sigmoid(tf.add(tf.matmul(self.layer1,
                                                             self.w_h2), self.b2))
                # output layer
                self.output = tf.nn.softmax(tf.add(tf.matmul(self.layer2,
                                                             self.w_out), self.b_out))
        return self.output

    def loss_fn(self, y_pred, y_true):
        self.loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_true, 
                                                                  logits=y_pred)
        return tf.reduce_mean(self.loss)

    def acc_fn(self, y_pred, y_true):
        y_pred = tf.cast(tf.argmax(y_pred, axis=1), tf.int32)
        y_true = tf.cast(y_true, tf.int32)
        predictions = tf.cast(tf.equal(y_true, y_pred), tf.float32)
        return tf.reduce_mean(predictions)

    def backward_prop(self, batch_xs, batch_ys):
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr_rate)
        with tf.GradientTape() as tape:
            predicted = self.feed_forward(batch_xs)
            step_loss = self.loss_fn(predicted, batch_ys)
        grads = tape.gradient(step_loss, self.variables)
        print(grads)
        input()
        optimizer.apply_gradients(zip(grads, self.variables))

n_shape = x_train.shape[0]
epochs = 20
batch_size = 128

ds_train = ds_train.repeat().shuffle(n_shape).batch(batch_size).prefetch(batch_size)

neural_net = Model(512, 256, 'gpu')

for epoch in range(epochs):
    no_steps = n_shape//batch_size
    avg_loss = 0.
    avg_acc = 0.
    for (batch_xs, batch_ys) in ds_train.take(no_steps):
        preds = neural_net.feed_forward(batch_xs)
        avg_loss += float(neural_net.loss_fn(preds, batch_ys)/no_steps) 
        avg_acc += float(neural_net.acc_fn(preds, batch_ys) /no_steps)
        neural_net.backward_prop(batch_xs, batch_ys)
    print(f'Epoch: {epoch}, Training Loss: {avg_loss}, Training ACC: {avg_acc}')
