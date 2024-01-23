import math
def poisson(x,alpha):
    return math.pow(math.e, -1*alpha) * math.pow(alpha, x) / math.factorial(x)
def expectedvalue(X,alpha):
    e = 0
    for x in X:
        e += x * poisson(x,alpha)
    return e

z = [i for i in range(0,50)]
print(expectedvalue(z, 480/175))