import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math, random

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
    print(partials)
    for k in range(len(weights)):
        for j in range(len(partials[k])):
            weights[k][j] += partials[k][j]
    return weights

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

inputs, outputs, layers, weights = creation(myList)
weights = [[0.858171535007186,0.8027746946128934,0.14684213529535542,0.785995693143207,0.265286153369877,0.17605756095363478,0.4441568461208929,0.647774901037866], [0.8071563090227641,0.6524314223361646], [0.688845601173394]]
nn = simulate(inputs[0], weights, layers)
weights = backprop(nn, weights, outputs[0])
input()
for i in range(30000):
    nn = simulate(inputs[i%len(inputs)], weights, layers)
    weights = backprop(nn, weights, outputs[i%len(inputs)])
printnn(layers, weights)
for i in range(len(inputs)):
    nn = simulate(inputs[i], weights, layers)
    print(nn)
    print(nn[-1])
#Alexander Yao, Period 4, 2023