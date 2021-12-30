import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
def invalid(pzl):
    pos = []
    for i in blocks:
        st = ''
        for j in i:
            st += pzl[j]
        pos.append(st)
    for i in pos:
        t = list(i)
        while '.' in t:
            t.remove('.')
        s = {*t}
        if len(s) != len(t):
            return False
    return True

def choices(pzl):
    pzls = []
    idx = pzl.find('.')
    pz = list(pzl)
    for i in range(1, 10):
        pz[idx] = str(i)
        pzls.append(''.join(pz))
    return pzls

def bruteforce(pzl):
    if not invalid(pzl):
        return ''
    if pzl.find('.') == -1:
        return pzl
    for i in choices(pzl):
        bf = bruteforce(i)
        if bf != '':
            return bf
    return ''

r, c = 9, 9
br, bc = 3, 3

blocks = []
for i in range(r):
    lst = []
    for j in range(c):
        lst.append(i * c + j)
    blocks.append(lst)
for i in range(c):
    lst = []
    for j in range(r):
        lst.append(j * r + i)
    blocks.append(lst)
for i in range(r // br):
    for j in range(c // bc):
        lst = []
        for k in range(br):
            for l in range(bc):
                lst.append(i * br * c + j * bc + k * c + l)
        blocks.append(lst)

for i in range(len(myList)):
    final = bruteforce(myList[i])
    total = 0
    for j in final:
        total += ord(j)
    total = total - r * c * ord('1')
    print(i + 1)
    print(myList[i])
    print(final)
    print(total)

#Alexander Yao, Period 4, 2023