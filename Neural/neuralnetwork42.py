import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math, random
val, symbol = 0, ''

def clean():
    global symbol, val
    exp = args[1][7:]
    if '>=' in exp:
        symbol = '>'
        val = float(exp[2:])
    elif '<=' in exp:
        symbol = '<'
        val = float(exp[2:])
    elif '>' in exp:
        symbol = '>'
        val = float(exp[1:])
    elif '<' in exp:
        symbol = '<'
        val = float(exp[1:])
    val = math.sqrt(val)
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
        start.append(a/val)
        start.append(0)
        start.append(b/val)
    for i in range(layers[1]):
        a, b = square[0][2*i],square[0][2*i+1]
        start.append(0)
        start.append(a/val)
        start.append(b/val)
    weights.append(start)
    for i in range(1,len(layers)-2):
        weights.append(genweights(square[i], layers[i], layers[i+1]))
    if symbol == '>':
        weights.append([square[-1][0],square[-1][0]])
        weights.append([(1+math.e)/2/math.e])
    else:
        weights.append([-square[-1][0],-square[-1][0]])
        weights.append([1.85914])
    return weights

def dot(lst1, lst2):
    return sum([lst1[i] * lst2[i] for i in range(len(lst1))])

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

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

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

def specialcords(val):
    split = random.random() * val
    x = math.sqrt(split) * (random.randint(0,1) * 2 - 1)
    y = math.sqrt(val - split) * (random.randint(0,1) * 2 - 1)
    return x, y

clean()
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