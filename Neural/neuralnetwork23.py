from http.client import TEMPORARY_REDIRECT
import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math, random

def randnum():
    return random.randint(1, 1000)/1000

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
    print(y[-1])
    return nn, y

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
            weights[i].append(randnum())
    
    return inputs, outputs, layers, weights

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

def divsigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))

def partial(x, err):
    return x * err

def dot(lst1, lst2):
    return sum([lst1[i] * lst2[i] for i in range(len(lst1))])

def error(nn, ys, weights, output):
    errs = []
    errs.append([output[i] - ys[-1][i] for i in range(len(ys[-1]))])
    temp = []
    for i in range(len(ys[-1])):
        temp.append(errs[-1][i] * weights[-1][i] * divsigmoid(ys[-2][i]))
    errs.append(temp)
    temp = []
    sums = []
    for k in range(len(nn)-2, 0, -1):
        for i in range(len(nn[k])):
            for j in range(len(nn[k+1])):
<<<<<<< HEAD
                sums.append(weights[k][i*len(nn[k+1])+j] * errs[-1][j])
            temp.append(-divsigmoid(ys[k-1][i]) * sum(sums))
            sums = []
        errs.append(temp)
        temp = []
=======
                print(weights, errs)
                print(weights[k][i*len(nn[k+1])+j], errs[-1][j])
                input()
                sums.append(weights[k][i*len(nn[k+1])+j] * errs[-1][j])
            print(sums)
            print(divsigmoid(ys[k-1][i]))
            input()
            temp.append(divsigmoid(ys[k-1][i]) * sum(sums))
            sums = []
        errs.append(temp)
        temp = []
    print(errs)
    print(0, 0, 0)
    input()
>>>>>>> 826eccccabb7241a7bb883a4bb2cddc3f5d33d29
    return errs

def update(nn, errs):
    partials = []
    for k in range(len(nn)-1):
        partials.append([100*nn[k][i] * errs[k][j] for i in range(len(nn[k])) for j in range(len(nn[k + 1]))])
    partials.append([100*nn[-1][i] * errs[-1][i] for i in range(len(nn[-1]))])
    return partials

def backprop(nn, ys, weights, output):
    errs = error(nn, ys, weights, output)[::-1]
    partials = update(nn, errs)
    for k in range(len(weights)):
        s = math.sqrt(dot(partials[k], partials[k]))
        for j in range(len(partials[k])):
            weights[k][j] += (partials[k][j]/s)*.001
    return weights

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

inputs, outputs, layers, weights = creation(myList)
for i in range(30000):
    nn, y = simulate(inputs[i%len(inputs)], weights, layers)
    weights = backprop(nn, y, weights, outputs[i%len(inputs)])
printnn(layers, weights)
for i in range(len(inputs)):
    nn, y = simulate(inputs[i], weights, layers)
<<<<<<< HEAD
    print(inputs[i])
    print(y[-1])
#Alexander Yao, Period 4, 2023
=======
    print(nn[-1])
#Alexander Yao, Period 4, 2023
>>>>>>> 826eccccabb7241a7bb883a4bb2cddc3f5d33d29
