import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import math, sys, time

(x_train, y_train), (x_test, y_test) = tfds.load('mnist', split = ['train', 'test'], batch_size = -1, as_supervised=True)

x_train = tf.reshape(x_train, shape=(x_train.shape[0], 784))
x_test  = tf.reshape(x_test, shape=(x_test.shape[0], 784))

nshape = x_train.shape[0]
epochs = 15
batchsize = 60
testcases = 10000
step = nshape//batchsize

ds_train = tf.data.Dataset.from_tensor_slices((x_train, y_train)).map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y)).repeat().shuffle(nshape).batch(batchsize).prefetch(batchsize)

def randnum(): 
    return tf.initializers.glorot_uniform(seed=42)

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

def divsigmoid(x):
    return x*(1-x)

def partial(x, err):
    return x * err

def dot(lst1, lst2):
    return sum([lst1[i] * lst2[i] for i in range(len(lst1))])

def error(preds, actual):
    return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = actual, logits = preds))

class neuralnetwork:
    def __init__(self, layers, lrate, device='None'):
        self.layers = layers
        self.lrate = .001
        self.device = device
        self.weights = []
        self.bias = []
        self.randomizer = tf.initializers.glorot_uniform(seed=42)

        for i in range(len(layers)-1):
            self.weights.append(tf.Variable(self.randomizer((self.layers[i], self.layers[i+1]))))

        for i in range(len(layers)-1):
            self.bias.append(tf.Variable(self.randomizer((self.layers[i+1],))))
        
        self.variables = []
        for i in range(len(self.weights)):
            self.variables.append(self.weights[i])
            self.variables.append(self.bias[i])
    
    def feedforward(self, x):
        if self.device is not None:
            with tf.device('gpu:0' if self.device == 'gpu' else 'cpu'):
                self.nn = []
                for i in range(len(self.layers)-2):
                    x = tf.nn.sigmoid(tf.add(tf.matmul(x, self.weights[i]), self.bias[i]))
                    self.nn.append(x)
                self.output = tf.nn.softmax(tf.add(tf.matmul(x, self.weights[-1]), self.bias[-1]))
                self.nn.append(self.output)
        return self.output

    def error(self, preds, actual):
        self.loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels = actual, logits = preds)
        return tf.reduce_mean(self.loss)

    def backprop(self, x, y):
        opt = tf.keras.optimizers.Adam(learning_rate=self.lrate)
        with tf.GradientTape() as tp:
            preds = self.feedforward(x)
            loss = self.error(preds, y)
        gradients = tp.gradient(loss, self.variables)
        opt.apply_gradients(zip(gradients, self.variables))

    def accuracy(self, preds, actual):
        preds = tf.cast(tf.argmax(preds, axis=1), tf.int32)
        actual = tf.cast(actual, tf.int32)
        predictions = tf.cast(tf.equal(actual, preds), tf.float32)
        return tf.reduce_mean(predictions)

nn1 = neuralnetwork([784,512,256,10], .001, 'gpu')

for i in range(epochs):
    acc = 0.
    total = 0
    for (x, y) in ds_train.take(step):
        print(x, y)
        input()
        pred = nn1.feedforward(x)
        acc += float(nn1.accuracy(pred,y))/step
        nn1.backprop(x,y)
        total += 1
    print('Epoch:', i)
    print('Accuracy:', acc)
    print('Testcases:', total)

print(time.process_time())
acc = 0
for (x, y) in ds_train.take(testcases):
    pred = nn1.feedforward(x)
    acc += float(nn1.accuracy(pred,y))/testcases
print('Final Accuracy:', acc)
print(time.process_time())

sys.stdout = open("weights.txt", "w")  
for i in nn1.weights:
    for j in i:
        print(np.array(j), end=' ')
    print()
    print()
sys.stdout.close()