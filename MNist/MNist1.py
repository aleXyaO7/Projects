import tensorflow as tf
import math, random, sys
from tensorflow import keras

sys.stdout = open("weights.txt", "w")
mnist = tf.keras.datasets.mnist
(x_train, y_train),(x_test, y_test) = mnist.load_data()

def randnum():
    return random.randint(1, 1000)/1000

def simulate(inputs, weights, layers):
    nn = []
    for i in layers:
        nn.append([0 for j in range(i)])
    for i in range(len(inputs)):
        nn[0][i] += inputs[i]
    for i in range(1, len(layers) - 1):
        lenprev = layers[i-1]
        lencur = layers[i]
        for j in range(lencur):
            nn[i][j] = sigmoid(dot(nn[i-1], weights[i-1][j*lenprev:(j+1)*lenprev]))
    for i in range(len(nn[-1])):
        nn[-1][i] += nn[-2][i] * weights[-1][i]
    
    return nn

def creation(x_train, y_train, x_test, y_test):
    inputs = []
    outputs = []
    testin = []
    for i in range(len(x_train)):
        t = []
        for j in x_train[i]: 
            for k in j:
                t.append(k)
        t.append(1)
        inputs.append(t)
        r = []
        for j in range(10):
            r.append(0)
        r[y_train[i]-1] += 1
        outputs.append(r)
    
    for i in range(len(x_test)):
        t = []
        for j in x_test[i]: 
            for k in j:
                t.append(k)
        t.append(1)
        testin.append(t)

    layers = [785, 10, 10, 10, 10, 10]
    weights = []
    for i in range(len(layers)-2):
        weights.append([])
        for j in range(layers[i] * layers[i+1]):
            weights[i].append(randnum())
    weights.append([])
    for j in range(layers[-1]):
        weights[-1].append(randnum())
    return inputs, outputs, testin, y_test, layers, weights

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

def divsigmoid(x):
    return x*(1-x)

def partial(x, err):
    return x * err

def dot(lst1, lst2):
    return sum([lst1[i] * lst2[i] for i in range(len(lst1))])

def error(nn, weights, output):
    errs = []
    errs.append([output[i] - nn[-1][i] for i in range(len(nn[-1]))])
    temp = []
    for i in range(len(nn[-1])):
        temp.append(errs[-1][i] * weights[-1][i] * divsigmoid(nn[-2][i]))
    errs.append(temp)
    temp = []
    for k in range(len(nn)-3, 0, -1):
        for i in range(len(nn[k])):
            temp.append(divsigmoid(nn[k][i]) * sum([weights[k][i+len(nn[k])*j]*errs[-1][j] for j in range(len(nn[k+1]))]))
        errs.append(temp)
        temp = []
    return errs

def update(nn, errs):
    partials = []
    for k in range(len(nn)-2):
        partials.append([nn[k][i] * errs[k][j] for j in range(len(errs[k])) for i in range(len(nn[k]))])
    partials.append([nn[-2][i] * errs[-1][i] for i in range(len(nn[-1]))])
    return partials

def backprop(nn, weights, output):
    errs = error(nn, weights, output)[::-1]
    partials = update(nn, errs)
    for k in range(len(weights)):
        for j in range(len(partials[k])):
            weights[k][j] += partials[k][j] * .1
    return weights

def printnn(weights):
    for i in weights:
        print(' '.join([str(j) for j in i]))

def maxpos(lst):
    maxp = 0
    maxval = 0
    for i in range(len(lst)):
        if lst[i] > maxval:
            maxval = lst[i]
            maxp = i
    return maxp

inputs, outputs, testin, testout, layers, weights = creation(x_train, y_train, x_test, y_test)
for i in range(len(inputs) * 10):
    nn = simulate(inputs[i%len(inputs)], weights, layers)
    weights = backprop(nn, weights, outputs[i%len(inputs)])
printnn(weights)
sys.stdout.close()
total = 0
for i in range(len(testin)):
    nn = simulate(testin[i], weights, layers)
    if maxpos(nn[-1]) == testout[i] - 1:
        total += 1
print(total)
#Alexander Yao, Period 4, 2023