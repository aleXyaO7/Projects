import sys; args = sys.argv[1:]
#Alexander Yao, 2023, pd 4
import math
leng, w, h = 0, 0, 0
dr, dpr = 12, -1
g = 1
nbrs = {}
acts = {}
rewards = {}
policy = {}
comp, rwds = [], []
qk = {}
legend = {
    'UR': 'V',
    'URD': 'W',
    'DR': 'S',
    'RDL': 'T',
    'DL': 'E',
    'DLU': 'F',
    'LU': 'M',
    'LUR': 'N',
    'UD': '|',
    'LR': '-',
    'URLD': '+',
}

def cleaninput(lst):
    global leng, w, h, dr, dpr, nbrs, acts, rewards, policy
    pointer = 0
    leng = int(lst[pointer])
    pointer += 1
    if lst[pointer][0] in 'BRGbrg':
        for i in range(1, int(math.sqrt(leng)) + 1):
            if leng % i == 0: h = i
        w = leng // h
    else:
        w = int(lst[pointer])
        h = leng // w
        pointer += 1
    
    for i in range(leng):
        nbr = set()
        if i >= w: nbr.add(i-w)
        if i + w < leng: nbr.add(i+w)
        if i % w != 0: nbr.add(i-1)
        if i % w != w - 1: nbr.add(i+1)
        nbrs[i] = nbr
        acts[i] = set(nbr)
        policy[i] = ('', leng)
    
    while pointer < len(lst):
        if lst[pointer][0] in 'Bb':
            if lst[pointer][-1] not in 'NSEW':
                ind = int(lst[pointer][1:])
                newn = set()
                for i in nbrs[ind]:
                    if i not in acts[ind]:
                        newn.add(i)
                        acts[i].add(ind)
                    else:
                        acts[i].remove(ind)
                acts[ind] = newn
            else:
                p = 1
                while lst[pointer][p] in '0123456789':
                    p += 1
                ind = int(lst[pointer][1:p])
                dirs = lst[pointer][p:]
                for i in dirs:
                    if i == 'N' and ind - w in acts:
                        if ind - w in acts[ind]:
                            acts[ind].remove(ind - w)
                            acts[ind - w].remove(ind)
                        else:
                            acts[ind].add(ind - w)
                            acts[ind - w].add(ind)
                    elif i == 'W' and ind - 1 in acts:
                        if ind - 1 in acts[ind]:
                            acts[ind].remove(ind - 1)
                            acts[ind - 1].remove(ind)
                        else:
                            acts[ind].add(ind - 1)
                            acts[ind - 1].add(ind)
                    elif i == 'S' and ind + w in acts:
                        if ind + w in acts[ind]:
                            acts[ind].remove(ind + w)
                            acts[ind + w].remove(ind)
                        else:
                            acts[ind].add(ind + w)
                            acts[ind + w].add(ind)
                    elif i == 'E' and ind + 1 in acts:
                        if ind + 1 in acts[ind]:
                            acts[ind].remove(ind + 1)
                            acts[ind + 1].remove(ind)
                        else:
                            acts[ind].add(ind + 1)
                            acts[ind + 1].add(ind)
        elif lst[pointer][0] in 'Gg':
            g = int(lst[pointer][1])
        else:
            if lst[pointer].count(':') == 2:
                if len(lst[pointer]) == 3:
                    dpr = -1
                else:
                    dpr = int(lst[pointer][3:])
            else:
                if ':' in lst[pointer]:
                    temp = lst[pointer][1:].split(':')
                    if temp[0]:
                        if temp[1]:
                            rewards[int(temp[0])] = int(temp[1])
                        else:
                            rewards[int(temp[0])] = dr
                    else:
                        if temp[1]:
                            dr = int(temp[1])
                        else:
                            dr = 10
                else:
                    rewards[int(lst[pointer][1:])] = dr
            
        pointer += 1
    qk[-w] = 'D'
    qk[w] = 'U'
    qk[-1] = 'R'
    qk[1] = 'L'

def comps(acts):
    unseen = {*range(leng)}
    for i in rewards:
        unseen.remove(i)
    global comp, rwds
    while unseen:
        start = unseen.pop()
        stk = [start]
        c = {start}
        r = set()
        while stk:
            node = stk.pop()
            for i in acts[node]:
                if i in unseen and i not in rewards:
                    stk.append(i)
                    c.add(i)
                    unseen.remove(i)
                if i in rewards:
                    r.add(i)
        comp.append(c)
        rwds.append(r)

def bfs0(r):
    q = [(r, 0)]
    print('----------')
    while q:
        node, k = q.pop(0)
        for i in acts[node]:
            if i not in rewards:
                if policy[i][1] == k + 1 and qk[i-node] not in policy[i][0]:
                    policy[i] = (policy[i][0] + qk[i-node], policy[i][1])
                elif policy[i][1] > k + 1:
                    policy[i] = (qk[i-node], k + 1)
                    q.append((i, k+1))

def solve0(c, r):
    if not c:
        for i in r:
            policy[i] = '.'
    elif not r:
        for i in c:
            policy[i] = '.'
    else:
        maxr = []
        maxv = 0
        for i in r:
            if rewards[i] > maxv:
                maxv = rewards[i]
                maxr = []
                maxr.append(i)
            elif rewards[i] == maxv:
                maxr.append(i)
        for i in maxr:
            bfs0(i)

def g0():
    for i in rewards:
        policy[i] = '*'
    for i in range(len(rwds)):
        solve0(comp[i], rwds[i])

def output():
    for i in range(h):
        for j in range(w):
            ind = i * w + j
            p = set(policy[ind][0])
            if len(p) == 1: print(policy[ind][0], end = ' ')
            else:
                for k in legend:
                    if not (p - set(k) or set(k) - p):
                        print(legend[k], end = ' ')
                        break
        print()

cleaninput(args)
comps(acts)
g0()
print(comp, rwds)
print(policy)
output()

#Alexander Yao, 2023, pd 4
