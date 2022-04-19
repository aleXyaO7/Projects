import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import math
weights = [[float(i) for i in j.split(' ')] for j in myList]
tranf = args[1]
inputs = args[2:]

layers = []
nn = []
def trans(val, tranf):
    if tranf == 'T1':
        return val
    if tranf == 'T2':
        return val * (val >= 0)
    if tranf == 'T3':
        return 1/(1+pow(math.e, -val))
    if tranf == 'T4':
        return 2/(1+pow(math.e, -val)) - 1

prevlayercount = 1
for i in weights[::-1]:
    prevlayercount = len(i) // prevlayercount
    layers.append(prevlayercount)
layers = layers[::-1]
outputdim = layers[-1]
layers.append(outputdim)

for i in layers:
    newlayer = []
    for j in range(i): newlayer.append(0)
    nn.append(newlayer)

nn[0] = [float(i) for i in inputs]

for i in range(1, len(layers) - 1):
    lenprev = layers[i-1]
    lencur = layers[i]
    for j in range(lencur):
        for k in range(lenprev):
            nn[i][j] += nn[i-1][k] * weights[i-1][j*lenprev+k]
        nn[i][j] = trans(nn[i][j], tranf)
for i in range(len(nn[-1])):
    nn[-1][i] += nn[-2][i] * weights[-1][i]
for i in nn[-1]: print(i, end = ' ')

#Alexander Yao, Period 4, 2023
