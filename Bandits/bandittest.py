from numpy.random import normal; from bandit1 import *

total = 0
def tester():
    global total
    res = []
    for i in range(1000):
        bandits = [k for k in normal(0, 1, 10)]
        reward = 0
        armpl = bandit(0, 10, None)
        for k in range(1, 1001):
            reward += (val:=normal(bandits[armpl], 1))
            armpl = bandit(k, armpl, val)
        res.append(reward/k)
        if not (i+1) % 10: print(round(sum(res[i-9:i+1])/10, 2), end=" ")
        if not (i+1) % 100: print()
    print(f"SCORE: {sum(res)/(len(res)/1000)}") 
    total += sum(res)/(len(res)/1000)

if __name__ == "__main__": 
    for i in range(10): tester()
    print(total/10)