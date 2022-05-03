import sys; args = sys.argv[1:]
import math, random

val, symbol = 0, ''

def cleaninput():
    global symbol, val
    exp = args[0][7:]
    if '=>' in exp:
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

def creation():
    layers = [2, 5, 3, 1, 1]
    weights = []
    for i in range(len(layers)-2):
        weights.append([])
        for j in range(layers[i] * layers[i+1]):
            weights[i].append(randnum())
    weights.append([])
    for j in range(layers[-1]):
        weights[-1].append(randnum())
    return layers, weights

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

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

def testcase(num):
    x, y = random.randint(-15, 15)/10, random.randint(-15, 15)/10
    inputs = [x,y]
    output = .5
    total = x*x + y*y - val
    if symbol == '>':
        output += total
    else:
        output -= total
    return inputs, [output]

def epoch(weights, layers, n):
    for i in range(n):
        if n % 10 == 5: inputs, outputs = testcase(-1)
        elif n % 10 == 6: inputs, outputs = testcase(1)
        else: inputs, outputs = testcase(0)
        nn = simulate(inputs, weights, layers)
        weights = backprop(nn, weights, outputs)
    return weights

def main():
    cleaninput()
    layers, weights = creation()
    weights = epoch(weights, layers, 100000)
    printnn(layers, weights)
    nn = simulate([.9, 0], weights, layers)
    print(nn[-1])

main()
#Alexander Yao, Period 4, 2023