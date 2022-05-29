import math
#Alexander Yao, 2023, pd 4
totals = [0,0,0,0,0,0,0,0,0,0]
n = [0,0,0,0,0,0,0,0,0,0]
arms = [0,1,2,3,4,5,6,7,8,9]
learning = .8

def maxind():
    maxi = 0
    maxv = -100000000
    for i in arms:
        if maxv < totals[i]/n[i] + learning * math.sqrt(math.log(sum(n), math.e)/n[i]):
            maxv = totals[i]/n[i] + learning * math.sqrt(math.log(sum(n), math.e)/n[i])
            maxi = i
    return maxi

def bandit(k, armpl, val):
    global totals, n, arms
    if k == 0:
        totals = [0,0,0,0,0,0,0,0,0,0]
        n = [0,0,0,0,0,0,0,0,0,0]
        arms = [0,1,2,3,4,5,6,7,8,9]
        return 0
    if k != 0:
        totals[armpl] += val
        n[armpl] += 1
    if k < 10:
        return arms[k % len(arms)]
    else:
        return maxind()

#Alexander Yao, 2023, pd 4