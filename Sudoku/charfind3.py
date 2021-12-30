import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

import time

def lowest(pos):                #Finds dot position with lowest possibilities
    min = r
    minidx = 0
    for i in pos:
        if len(pos[i]) < 2:
            return i
        if len(pos[i]) < min:
            min = len(pos[i])
            minidx = i
    return minidx

def choices(pzl, pos):          #Finds best subpuzzles
    idx = lowest(pos)
    if len(pos[idx]) == 0:
        return []
    allpos = []
    lst = list(pzl)
    if len(pos[idx]) == 1:
        lst[idx] = pos[idx].pop()
        pos[idx].add(lst[idx])
        return [(''.join(lst), idx)]
    if len(pos[idx]) == 2:
        for i in pos[idx]:
            lst[idx] = i
            allpos.append((''.join(lst), idx))
        return allpos
    else:
        ch, choices = charfind(pos)
        if len(choices) < len(pos[idx]):
            for i in choices:
                lst[i] = ch
                allpos.append((''.join(lst), i))
                lst[i] = '.'
        else:
            for i in pos[idx]:
                lst[idx] = i
                allpos.append((''.join(lst), idx))
    return allpos

def charfind(pos):              #Finds best char
    lst = []
    for i in checks:
        positions = {j:[] for j in chars}
        for j in checks[i]:
            if j in pos:
                for k in pos[j]:
                    positions[k].append(j)
        if i in pos:
            for k in pos[i]:
                positions[k].append(i)
        for j in positions:
            if positions[j]:
                lst.append((len(positions[j]), j, positions[j]))
    a, ch, choice = min(lst)
    return ch, choice

def increment(n, pos, idx):     #Increments possible chars for dots
    temp = dictcopy(pos)
    for k in checks[idx]:
        if k in pos:
            temp[k] = pos[k] - {n[idx]}
    temp.pop(idx)
    return temp

def dictcopy(pos):              #Deepcopy dicts
    return {k:pos[k] for k in pos}

def main(pzl, pos):             #Main bruteforce method
    global called
    called += 1
    if pzl.find('.') == -1: return pzl
    nbrs = choices(pzl, pos)
    for n, idx in nbrs:
        temp = increment(n, pos, idx)
        ar = main(n, temp)
        if ar: return ar
    return ''

def definepos(pzl):             #Defines dot positions and possible chars
    pos = {}
    for j in range(len(pzl)):
        if pzl[j] == '.':
            nbrs = set([pzl[i] for i in checks[j]])
            pos[j] = set(chars) - nbrs
    return pos

def format(pzl):                #Formats into sudoku form  
    for i in range(bc):
        for k in range(bc):
            for j in range(br):
                print(pzl[(i * bc + k) * r + br * j:(i * bc + k) * r + br * j + br], end = ' ')
            print()
        print()

r, c = 9, 9
br, bc = 3, 3
chars = [*"123456789"]

checks = {}             #Defines all neighbors
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
    pos = definepos(pzl)            #Defines all dot positions and their possible characters
    final = main(pzl, pos)
    total = 0
    for j in final:                 #Ascii chekcking
        total += ord(j)
    total = total - r * c * ord('1')
    print(i + 1)
    print(myList[i])
    print(final)
    print(total)
print('brute force called:', called)
print('total time:', time.process_time(), 's')

#Alexander Yao, Period 4, 2023