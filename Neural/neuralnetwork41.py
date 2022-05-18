import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math, random

weights = []

def cleaninput(myList):
    result = []
    for l in myList:
        lay = []
        newl = l.split(' ')
        for j in newl:
            if j and j[-1] == ',':
                j = j[:-1]
            if j and j.replace('.', '', 1).replace('-', '', 1).isdigit(): lay.append(float(j))
        if lay: result.append(lay)
    return result

def randnum():
    return random.randint(1, 1000)/1000

def genweights(weight, layer1, layer2):
    w = []
    for i in range(layer2):
        for j in range(layer1):
            w.append(weight[i * layer1 + j])
        for j in range(layer1):
            w.append(0)
    for i in range(layer2):
        for j in range(layer1):
            w.append(0)
        for j in range(layer1):
            w.append(weight[i * layer1 + j])
    return w

def init(weights, layers, square):
    start = []
    for i in range(layers[1]):
        a, b = square[0][2*i],square[0][2*i+1]
        start.append(a)
        start.append(0)
        start.append(b)
    for i in range(layers[1]):
        a, b = square[0][2*i],square[0][2*i+1]
        start.append(0)
        start.append(a)
        start.append(b)
    weights.append(start)
    for i in range(1,len(layers)-2):
        weights.append(genweights(square[i], layers[i], layers[i+1]))
    weights.append([square[-1][0],square[-1][0]])
    weights.append([(1+math.e)/2/math.e])
    return weights

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

square = cleaninput(myList)
layers = []
prevlayercount = 1
for i in square[::-1]:
    prevlayercount = len(i) // prevlayercount
    layers.append(prevlayercount)
layers = layers[::-1]
outputdim = layers[-1]
layers.append(outputdim)
init(weights, layers, square)
layers = []
prevlayercount = 1
for i in weights[::-1]:
    prevlayercount = len(i) // prevlayercount
    layers.append(prevlayercount)
layers = layers[::-1]
outputdim = layers[-1]
layers.append(outputdim)
printnn(layers, weights)
#Alexander Yao, Period 4, 2023