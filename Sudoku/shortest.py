import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

def choices(pzl, idx):
    vals = set(chars)
    for i in checks[idx]:
        if pzl[i] in vals:
            vals.remove(pzl[i])
    allpos = []
    lst = list(pzl)
    for i in vals:
        lst[idx] = i
        allpos.append(''.join(lst))
    return allpos

def main(pzl, pos):
    if pzl.find('.') == -1:
        return pzl
    val, idx = pos[0]
    for i in choices(pzl, idx):
        pos1 = pos[:]
        pos1.pop(0)
        ar = main(i, pos1)
        if ar != '':
            return ar
    return ''

def definepos(pzl):
    lst = []
    for j in range(len(pzl)):
        if pzl[j] == '.':
            a = set(chars)
            for k in checks[j]:
                if pzl[k] in a:
                    a.remove(pzl[k])
            lst.append((a, j))
    return(sorted(lst))

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

for i in range(len(myList)):
    pzl = myList[i]
    pos = definepos(pzl)
    final = main(pzl, pos)
    total = 0
    for j in final:
        total += ord(j)
    total = total - r * c * ord('1')
    print(i + 1)
    print(myList[i])
    print(final)
    print(total)

#Alexander Yao, Period 4, 2023