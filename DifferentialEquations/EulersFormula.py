import math
def deriv(x, y):
    return 10/3 * math.pow(x,7/3)
def euler(x, y, stepsize):
    return y + deriv(x, y) * stepsize
def calc(x, y, stepsize, iteration):
    x1, y1 = x, y
    for i in range(iteration):
        y1 = euler(x1, y1, stepsize)
        x1 = x1 + stepsize
        print(x1, y1)

calc(0, 2, 0.05, 20)