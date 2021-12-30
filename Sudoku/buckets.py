import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

def lowest(pointer):
    while not buckets[pointer]:
        pointer += 1
    while buckets[pointer][0] in seen:
        buckets[pointer].pop(0)
    return buckets[pointer].pop(0)

def choices(pzl, pos, pointer):
    idx = lowest(pointer)
    allpos = []
    lst = list(pzl)
    for i in pos[idx]:
        lst[idx] = i
        allpos.append(''.join(lst))
    return allpos, idx

def increment(n, temp, idx):
    for k in checks[idx]:
            if k in temp:
                temp[k] = temp[k] - {n[idx]}
                buckets[len(temp[k])].append(k)

def dictcopy(pos):
    temp = {}
    for k in pos:
        temp[k] = pos[k]
    return temp

def main(pzl, pos, pointer):
    print(buckets)
    input()
    if pzl.find('.') == -1:
        return pzl
    nbrs, idx = choices(pzl, pos, pointer)
    pos.pop(idx)
    seen.add(idx)
    for n in nbrs:
        temp = dictcopy(pos)
        increment(n, temp, idx)
        ar = main(n, temp, pointer - 1)
        if ar:
            return ar
    return ''

def definepos(pzl):
    pos = {}
    for j in range(len(pzl)):
        if pzl[j] == '.':
            pos[j] = set(chars)
            for k in checks[j]:
                if pzl[k] in pos[j]:
                    pos[j].remove(pzl[k])
            buckets[len(pos[j])].append(j)
    return pos

def format(pzl):
    for i in range(bc):
        for k in range(bc):
            for j in range(br):
                print(pzl[(i * bc + k) * r + br * j:(i * bc + k) * r + br * j + br], end = ' ')
            print()
        print()

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

seen = set()

for i in range(len(myList)):
    pzl = myList[i]
    buckets = [[] for i in range(10)]
    pos = definepos(pzl)
    seen = set()
    final = main(pzl, pos, 1)
    total = 0
    for j in final:
        total += ord(j)
    total = total - r * c * ord('1')
    print(i + 1)
    print(myList[i])
    print(final)
    print(total)


#Alexander Yao, Period 4, 2023