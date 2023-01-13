import math
def prime_factor(n):
    f = {}
    for i in range(2, int(math.sqrt(n))):
        while n % i == 0:
            n /= i
            if i not in f:
                f[i] = 0
            f[i] += 1
    if n != 1:
        f[int(n)] = 1
    return f

print(prime_factor(12))

def gcd(a, b):
    if b == 0: return a
    return gcd(b, a % b)

def lcm(a, b):
    return a * b // gcd(a, b)

print(gcd(5, 10))
print(lcm(5, 12))