from scipy.stats import poisson
for k in range(1500, 2000):
    print(k, poisson.pmf(k,1500)/poisson.pmf(k,2000))

print(poisson.pmf(1732,1500))