import sys; args = sys.argv[1:]
import math, random

val, symbol = 0, ''

def cleaninput():
    global symbol, val
    exp = args[0][7:]
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
    layers = [3, 4, 3, 1, 1]
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

def backprop(nn, weights, output, alpha):
    errs = error(nn, weights, output)[::-1]
    partials = update(nn, errs)
    for k in range(len(weights)):
        for j in range(len(partials[k])):
            weights[k][j] += partials[k][j] * alpha
    return weights

def printnn(layers, weights):
    print('Layer counts', ' '.join([str(i) for i in layers]))
    for i in weights:
        print(' '.join([str(j) for j in i]))

def randcords():
    return random.randint(-15, 15)/10, random.randint(-15, 15)/10

def specialcords(val):
    total = random.random() * .4 + val-.2
    split = random.random() * total
    x = math.sqrt(split) * (random.randint(0,1) * 2 - 1) -.1
    y = math.sqrt(total - split) * (random.randint(0,1) * 2 - 1)-.1
    return x, y

def testcase(x, y):
    output = .5
    total = (x*x + y*y - val)
    if symbol == '>':
        output += total
    else:
        output -= total
    return [output]

def epoch(weights, layers, n):
    for i in range(n):
        x, y = randcords()
        if i % 2 == 0:
            x, y = specialcords(val)
        for inputs in [[x,y,1],[x+.1,y,1],[x-.1,y,1],[x,y+.1,1],[x,y-.1,1],[x+.1,y+.1,1],[x-.1,y-.1,1],[x-.1,y+.1,1],[x+.1,y-.1,1]]:
            outputs = testcase(inputs[0],inputs[1])
            nn = simulate(inputs, weights, layers)
            weights = backprop(nn, weights, outputs, (n-i)/n)
    return weights

def main():
    cleaninput()
    layers, weights = creation()
    weights = epoch(weights, layers, 10000)
    printnn(layers, weights)
    total = 0
    for i in range(100000):
        x, y = randcords()
        nn = simulate([x,y,1], weights, layers)
        if (testcase(x,y)[0] > val and nn[-1][0] > .5) or (testcase(x,y)[0] < val and nn[-1][0] < .5):
            total += 1
    print(total)

main()
#Alexander Yao, Period 4, 2023