import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

import time

def lowest(pos):
    min = r
    minidx = 0
    for i in pos:
        if len(pos[i]) < 2:
            return i
        if len(pos[i]) < min:
            min = len(pos[i])
            minidx = i
    return minidx

def choices(pzl, pos, idx):
    allpos = []
    lst = list(pzl)
    if len(pos[idx]) == 0:
        return []
    if len(pos[idx]) == 1:
        lst[idx] = pos[idx].pop()
        pos[idx].add(lst[idx])
        return [''.join(lst)]
    for i, j in charfind(idx, pos):
        lst[idx] = j
        allpos.append(''.join(lst))
    return allpos

def charfind(idx, pos):
    dct = {}
    for i in pos[idx]:
        dct[i] = 0
    for i in checks[idx]:
        if i in pos:
            for j in pos[i]:
                if j in dct:
                    dct[j] += 1
    lst = []
    for i in dct:
        lst.append((dct[i], i))
    lst.sort()
    return lst

def increment(n, temp, idx):
    for k in checks[idx]:
        if k in temp:
            temp[k] = temp[k] - {n[idx]}

def dictcopy(pos):
    return {k:pos[k] for k in pos}

def main(pzl, pos):
    global called
    called += 1
    if pzl.find('.') == -1:
        return pzl
    idx = lowest(pos)
    nbrs = choices(pzl, pos, idx)
    pos.pop(idx)
    for n in nbrs:
        temp = dictcopy(pos)
        increment(n, temp, idx)
        ar = main(n, temp)
        if ar:
            return ar
    return ''

def definepos(pzl):
    pos = {}
    for j in range(len(pzl)):
        if pzl[j] == '.':
            nbrs = set([pzl[i] for i in checks[j]])
            pos[j] = set(chars) - nbrs
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

called = 0
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
print(called)
print(time.process_time())

#Alexander Yao, Period 4, 2023