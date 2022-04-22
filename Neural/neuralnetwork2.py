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

def partialfinal(output, x, weight):
    return (output - x * weight) * x

def gradientfinal(outputs, xs, weights):
    return [partialfinal(outputs[i], xs[i], weights[i]) for i in range(len(outputs))]

def errorfinal(output, y, weight):
    return (output - y) * weight * divsigmoid(y)

def partialpenult(x, error):
    return x * error

def gradientpenult(xs, ers, i, j):
    return [partialpenult(xs[x], ers[y]) for x in range(i) for y in range(j)]

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

inputs, outputs, layers, weights = creation(myList)
weights = [randweights(len(i)) for i in weights]

def learn(inputs, weights, layers, output):
    nn, outputs, y = simulate(inputs, weights, layers)
    gra = gradientfinal(output, nn[-2], weights[-1])
    for j in range(len(gra)): weights[-1][j] += .01 * gra[j]
    er = []
    for j in range(len(outputs[0])): er.append(errorfinal())
    printnn(layers, weights)

learn(inputs[0], weights, layers, outputs[0])
#Alexander Yao, Period 4, 2023
