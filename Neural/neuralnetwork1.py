import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
weights = [[int(i) for i in j.split(' ')] for j in myList]
tranf = args[1]
inputs = args[2:]

layers = []
nn = []

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

nn[0] = [int(i) for i in inputs]

for i in range(1, len(layers)):
    lenprev = layers[i-1]
    lencur = layers[i]
    for j in range(lencur):
        for k in range(lenprev):
            print(i,j, k)
            print(nn[i])
            print(nn[i-1])
            print(weights[i-1])
            nn[i][j] += nn[i-1][k] * weights[i-1][j*lenprev+k]

print(nn)