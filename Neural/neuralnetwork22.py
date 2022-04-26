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
        y[-1].append(nn[-2][i] * weights[-1][i])
    nn.pop()
    y.pop(0)
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

    layers = [len(inputs[0]), 2, len(outputs[0]), len(outputs[0])]
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
    return x * err

def dot(lst1, lst2):
    return sum([lst1[i] * lst2[i] for i in range(len(lst1))])

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
    print(nn)
    print(ys)
    print(weights)
    input()
    back, errs = [[] for i in range(len(nn))], []
    errs.append([output[i] - ys[-1][i] for i in range(len(output))])
    for i in range(len(output)):
        back[-1].append(partial(nn[-1][i], errs[-1][i]))
    errs.append([weights[-1][i] * errs[-1][i] * divsigmoid(ys[-1][i]) for i in range(len(nn[-1]))])
    print(back)
    print(errs)
    input()
    for k in range(len(weights) - 2, 0, -1):
        n1 = len(nn[k])
        n0 = len(ys[k])
        for j in range(n0):
            for i in range(n1):
                back[k].append(partial(nn[k][i], errs[-1][j]))
        temp = []
        for i in range(n1):
            total = 0
            for j in range(n0):
                total += weights[k][j * len(nn[j]) + i] * errs[-1][j]
            temp.append(total * divsigmoid(y[k-1][i]))
        errs.append(temp)
        print(back)
        print(errs)
        input()
    n1 = len(nn[0])
    n0 = len(ys[0])
    for j in range(n0):
        for i in range(n1):
            back[0].append(partial(nn[0][i], errs[-1][j]))
    print(back)
    print(errs)
    input()
    for i in range(len(back)):
        s = math.sqrt(dot(back[i], back[i]))
        if s != 0:
            k = [j/s * .01 for j in back[i]]
            for j in range(len(back[i])):
                weights[i][j] += k[j]
    print(back)
    print(errs)
    input()
    return weights

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

inputs, outputs, layers, weights = creation(myList)
weights = [randweights(len(i)) for i in weights]
for i in range(30000):
    nn, outputs, y = simulate(inputs[i%len(inputs)], weights, layers)
    weights = backprop(nn, y, weights, outputs)
printnn(layers, weights)
for i in range(len(inputs)):
    nn, outputs, y = simulate(inputs[i], weights, layers)
    print(nn[-1])
#Alexander Yao, Period 4, 2023