import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math

def simulate(inputs, weights, layers):
    nn = [inputs, [0,0], [0], [0]]
    for i in range(1, len(layers) - 1):
        lenprev = layers[i-1]
        lencur = layers[i]
        for j in range(lencur):
            for k in range(lenprev):
                nn[i][j] += nn[i-1][k] * weights[i-1][j*lenprev+k]
            nn[i][j] = trans(nn[i][j], tranf)

def creation(myList):
    inputs = []
    outputs = []

    for i in myList:
        insize = myList.split(' ')
        flag = False
        for j in insize:
            if j == '=>':
                flag = True
            else:
                if not flag: inputs.append(int(j))
                else: outputs.append(int(j))

    layers = [len(inputs), 2, 1, 1]
    weights = [[]]
    for i in range(len(layers)-1):
        weights.append([])
        for j in range(layers[i] * layers[i+1]):
            weights[i+1].append(0)

    return inputs, outputs, layers, weights

def hadamard(v1, v2):
    return [v1[i]*v2[i] for i in range(len(v1))]

def dot(v1, v2):
    return sum(hadamard(v1, v2))

def sigmoid(x):
    return 1/(1+pow(math.e, -x))

def divsigmoid(x):
    return sigmoid(x)/(1-sigmoid(x))

def finalpartial(output, inp, weight):
    return (output - inp * weight) * inp

def partial(inp, weight):
    return -inp*weight

def efinal(output, inp, weight):
    return (output - inp * weight) * weight * divsigmoid(output)

def elayer(inp, weights, e):
    return sum([weights[i]*e[i] for i in range(len(e))]) * sigmoid(inp)

def gradient(layer, nn, weights, t):
    return [finalpartial(t, nn[layer][i], weights[layer][i]) for i in range(len(nn[layer]))]

#Alexander Yao, Period 4, 2023