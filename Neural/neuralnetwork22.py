import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math, random

def randweights(x):
    return [random.randint(1, 1000)/1000 for i in range(x)]

def simulate(inputs, weights, layers):
    nn = []
    y = []
    for i in layers:
        nn.append([0 for j in range(i)])
        y.append([])
    y.pop()
    for i in range(len(inputs)):
        nn[0][i] += inputs[i]
    for i in range(1, len(layers) - 1):
        lenprev = layers[i-1]
        lencur = layers[i]
        for j in range(lencur):
            for k in range(lenprev):
                nn[i][j] += nn[i-1][k] * weights[i-1][j*lenprev+k]
            y[i].append(nn[i][j])
            nn[i][j] = sigmoid(nn[i][j])
    for i in range(len(nn[-1])):
        nn[-1][i] += nn[-2][i] * weights[-1][i]
    return nn, nn[-1], y

def creation(myList):
    inputs = []
    outputs = []

    for i in myList:
        insize = i.split(' ')
        flag = False
        tempin = []
        tempout = []
        for j in insize:
            if j == '=>':
                flag = True
            else:
                if not flag: tempin.append(int(j))
                else: tempout.append(int(j))
        tempin.append(1)
        inputs.append(tempin)
        outputs.append(tempout)

    layers = [len(inputs[0]), 2, 1, 1]
    weights = []
    for i in range(len(layers)-1):
        weights.append([])
        for j in range(layers[i] * layers[i+1]):
            weights[i].append(0)
    return inputs, outputs, layers, weights

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

def divsigmoid(x):
    return sigmoid(x)/(1-sigmoid(x))

def partial(x, err):
    return -x * err

def error(nn, ys, weights, preverr, layer, output):
    errs = []
    if layer == len(nn) - 1:
        for i in range(len(nn[layer])):
            errs.append((output[i] - ys[layer][i]) * weights[layer][i] * divsigmoid(ys[layer][i]))
    else:
        for i in range(len(nn[layer])):
            errs.append(sum([preverr[j] * weights[layer + 1][i + j * len(nn[layer])] for j in range(len(nn[layer+1]))]) * divsigmoid(ys[layer][i]))
    return errs

def backprop(nn, ys, weights, output):
    back, errs = [[] for i in range(len(nn) - 1)], []
    errs.append([output[i] - ys[-1][i] for i in range(len(output))])
    for i in range(len(output)):
        back[-1].append(partial(nn[-2][i], errs[-1][i]))
    