import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

def lowest(pzl):
    min = r
    minidx = []
    for i in range(len(pzl)):   
        if pzl[i] == '.':
            c = choices(pzl, i)
            if len(c) < min:
                min = len(c)
                minidx = c
    return minidx

def choices(pzl, idx):
    pzls = []
    pz = list(pzl)
    idxs = {*chars}
    for i in checks[idx]:
        if pzl[i] in idxs:
            idxs.remove(pzl[i])
    for i in idxs:
        pz[idx] = str(i)
        pzls.append(''.join(pz))
    return pzls

def main(pzl):
    if pzl.find('.') == -1:
        return pzl
    for i in lowest(pzl):
        ar = main(i)
        if ar != '':
            return ar
    return ''

r, c = 9, 9
br, bc = 3, 3
chars = [*"123456789"]

checks = {}
for i in range(r * c):
    checks[i] = set()
for i in range(r):
    lst = []
    for j in range(c):
        lst.append(i * c + j)
    for j in range(len(lst)):
        for k in range(len(lst)):
            checks[lst[j]].add(lst[k])
for i in range(c):
    lst = []
    for j in range(r):
        lst.append(j * r + i)
    for j in range(len(lst)):
        for k in range(len(lst)):
            checks[lst[j]].add(lst[k])
for i in range(r // br):
    for j in range(c // bc):
        lst = []
        for k in range(br):
            for l in range(bc):
                lst.append(i * br * c + j * bc + k * c + l)
        for j in range(len(lst)):
            for k in range(len(lst)):
                checks[lst[j]].add(lst[k])
for k in checks:
    checks[k].remove(k)

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
    final = main(myList[i])
    total = 0
    for j in final:
        total += ord(j)
    total = total - r * c * ord('1')
    print(i + 1)
    print(myList[i])
    print(final)
    print(total)

#Alexander Yao, Period 4, 2023