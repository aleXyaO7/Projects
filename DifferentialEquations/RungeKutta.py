import math
def deriv(x, y):
    return 10/3 * math.pow(x,7/3)
def rungekutta(x, y, stepsize):
    k1 = deriv(x,y)
    k2 = deriv(x + stepsize/2, y + stepsize/2 * k1)
    k3 = deriv(x + stepsize/2, y + stepsize/2 * k2)
    k4 = deriv(x + stepsize/2, y + stepsize * k3)
    return y + stepsize / 6 * (k1 + k2 + k3 + k4)
def calc(x, y, stepsize, iteration):
    x1, y1 = x, y
    for i in range(iteration):
        y1 = rungekutta(x1, y1, stepsize)
        x1 = x1 + stepsize
        print(x1, y1)

calc(0, 2, 0.05, 20)