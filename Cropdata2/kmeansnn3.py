import pandas as pd
import numpy as np
from pandas import read_csv
import tensorflow as tf
import tensorflow_datasets as tfds
import math, sys, time, random
from PIL import Image as im

size = 15

dataset = pd.read_csv('imlist.csv', header = None)
pre2020 = [[j for j in i] for i in dataset.iloc[:,19-size:19].values]
tar2020 = [int(i) for i in dataset.iloc[:, 19].values]
leng = len(tar2020)

# Create and use a method to convert arrays to images
def toImage(array, s):
    w,h = 1329, 1320
    t=(w,h,3)
    array = np.reshape(array, (1329, 1320))
    result = np.zeros(t, dtype=np.uint8)
    for i in range(1329):
        for j in range(1320):
            if(array[i,j] == 0):
                result[i,j] = [255, 0, 0]
            elif(array[i,j] == 1):
                result[i, j] = [100, 100, 0]
            elif(array[i,j] == 2):
                result[i, j] = [38, 122, 0]
            elif(array[i,j] == 3):
                result[i,j] = [232, 255, 191]
            elif(array[i,j] == 4):
                result[i, j] = [0, 0, 255]
            elif(array[i,j] == 5):
                result[i, j] = [0, 0, 0]
            elif(array[i,j] == 6):
                result[i,j] = [0, 255, 0]
            elif(array[i,j] == 7):
                result[i, j] = [255, 255, 0]
            elif(array[i,j] == 8):
                result[i, j] = [0, 255, 255]
            elif(array[i,j] == 9):
                result[i,j] = [255, 0, 255]
    data = im.fromarray(result, "RGB")
    data.save(s)

# Kmeans

k = 10
vector_dict = {}
means = {}

def cleaninput():
    for i in range(len(pre2020)):
        temp = tuple(pre2020[i])
        if temp not in vector_dict: vector_dict[temp] = set()
        vector_dict[temp].add(i)

def definemeans():
    for i in range(k):
        node = tuple(pre2020[random.randint(0, leng - 1)])
        while node in means:
            node = tuple(pre2020[random.randint(0, leng - 1)])
        means[node] = set()

def dist(p1, p2):
    total = 0
    for i in range(len(p1)):
        total += pow(p1[i]-p2[i], 2)
    return math.sqrt(total)

def closestmean(p1, means):
    s,t = min([(dist(p1, m), m) for m in means])
    return t

def findmean(v, o):
    if not v: return o
    total = [0] * size
    t = 0
    for i in v:
        s = len(vector_dict[i])
        for j in range(size):
            total[j] += i[j] * s
        t += s
    return tuple([total[j]/t for j in range(size)])

def sort(points, means):
    for i in points:
        means[closestmean(i, means)].append(i)
    return means

def kepoch():
    global means
    newmeans = {}
    for i in means: newmeans[i] = set()
    for v in vector_dict:
        nv = closestmean(v, means)
        newmeans[nv].add(v)
    means = {}
    for i in newmeans:
        mean = findmean(newmeans[i], i)
        means[mean] = newmeans[i]
    print([len(means[i]) for i in means])

def train():
    pointer = 0
    while True:
        pointer += 1
        tempmeans = dict(means)
        kepoch()
        if means == tempmeans: break
        print('Round', pointer)

cleaninput()
definemeans()
train()
for i in means:
    if means[i]:
        print([round(j) for j in i])

kmeansdict = {}
kmeansarray = [0] * leng
pointer = 0
for i in means:
    kmeansdict[i] = pointer
    pointer += 1
for i in means:
    for j in means[i]:
        for z in vector_dict[j]:
            kmeansarray[z] = kmeansdict[i]
toImage(kmeansarray, 'kmeansarray.png')

kmeanslegend = [5] * leng
for i in range(10):
    for j in range(50):
        for z in range(50):
            kmeanslegend[z + j * 1320 + i * 66000] = i
toImage(kmeanslegend, 'kmeanslegend.png')

# Neural Network
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

array = [0] * leng
epochs = 2
batchsize = 60
allp = []
for i in means:
    print(i)
    ind, x_train, y_train = [], [], []
    for j in means[i]:
        for z in vector_dict[j]:
            temp = pre2020[z]
            temp.append(z)
            x_train.append(temp)
            y_train.append(tar2020[z])
            
            nshape = len(x_train)
    print('training')
    ds_train = tf.data.Dataset.from_tensor_slices((x_train, y_train)).map(lambda x, y: (tf.cast(x, tf.float32)/255.0, y)).repeat().shuffle(nshape).batch(batchsize).prefetch(batchsize)
    nn1 = neuralnetwork([size,12,7,4], .001, 'gpu')
    step = len(y_train)//batchsize
    for i in range(epochs):
        print('epoch', i)
        acc = 0.
        total = 0
        for (nx,y) in ds_train.take(step):
            x = []
            for j in nx:
                x.append(j[:-1])
            pred = nn1.feedforward(x)
            acc += float(nn1.accuracy(pred,y))/step
            nn1.backprop(x,y)
            total += 1
        print('Epoch:', i)
        print('Accuracy:', acc)
        print('Testcases:', total)
    print(time.process_time())
    acc = 0
    for (nx, y) in ds_train.take(step):
        x = []
        for j in nx:
            x.append(j[:-1])
        pred = nn1.feedforward(x)
        acc += float(nn1.accuracy(pred,y))/step
        for i in range(len(pred)):
            array[int(list(nx[i])[-1])] = int(tf.argmax(pred[i]))
    print('Final Accuracy:', acc)
    print(time.process_time())
    allp.append((x_train[0], acc))
    print('------------------------------')
print(allp)

toImage(array, 'kmeansnn.png')