import math
def choose(n,k):
    return math.factorial(n) / math.factorial(k) / math.factorial(n-k)
def permute(n,k):
    return math.factorial(n) / math.factorial(n-k)
def pascal(n,k,p):
    return choose(n-1,k-1) * math.pow(p,k) * math.pow(1-p,n-k)
def calculate_prob(d,N,k,p):
    prob = 0
    if d == 5:
        for n in N:
            prob += pascal(n,k,p)
    return prob

print(calculate_prob(5,[2,3,4,5],2,0.516815))