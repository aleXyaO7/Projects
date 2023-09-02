import math
def deriv(x, y):
    return 100 - 100 * y
def step(x, y, stepsize):
    return y + deriv(x, y) * stepsize
def calc(x, y, stepsize, iteration):
    x1, y1 = x, y
    for i in range(iteration):
        y1 = step(x1, y1, stepsize)
        x1 = x1 + stepsize
        print(x1, y1)

calc(0, 2, 0.021, 50)