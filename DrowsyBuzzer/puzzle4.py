def digits(n):
    return sum([int(i) for i in str(n)])

def div(n, fac, min, max):
    for i in range(min, max):
        print(i)
        print(n % pow(fac, i))

num = int('118851645561296000376034785198164494688414456705831172376262219200112792088277969541071768990787363873003127014286365940947784044775942705077240951386463035565828869014109611169381330429612810758611514370371882372778777971240170557817389364281344')
print(num)
print(num % pow(3,234) * pow(2,80) * pow(11, 105))
num //= pow(2,80) * pow(3,234) * pow(11, 105)
print(num)
print(digits(num))