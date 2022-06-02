import sys; args = sys.argv[1:]
#Alexander Yao, 2023, pd 4
import math
leng, w, h = 0, 0, 0
dr, dpr = 10, -1
g = 0
nbrs = {}
acts = {}
rewards = {}
policy = {}
comp, rwds = [], []

def cleaninput(lst):
    global leng, w, h, dr, dpr, nbrs, acts, rewards
    pointer = 0
    leng = int(lst[pointer])
    pointer += 1
    if lst[pointer][0] in 'BRG':
        for i in range(1, int(math.sqrt(leng)) + 1):
            if leng % i == 0: h = i
        w = leng // h
    else:
        w = int(lst[pointer])
        h = leng // w
        pointer += 1
    
    if lst[pointer][0] in 'G':
        g = int(lst[pointer][1])
        pointer += 1
    else:
        g = 0
    
    for i in range(leng):
        nbr = set()
        if i >= w: nbr.add(i-w)
        if i + w < leng: nbr.add(i+w)
        if i % w != 0: nbr.add(i-1)
        if i % w != w - 1: nbr.add(i+1)
        nbrs[i] = nbr
        acts[i] = set(nbr)
    
    while pointer < len(lst):
        if lst[pointer][0] in 'B':
            if len(lst[pointer]) == 2:
                ind = int(lst[pointer][1])
                newn = set()
                for i in nbrs[ind]:
                    if i not in acts[ind]:
                        newn.add(i)
                        acts[i].add(ind)
                    else:
                        acts[i].remove(ind)
                acts[ind] = newn
            else:
                ind = int(lst[pointer][1])
                dirs = lst[pointer][2:]
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
    
    print(acts)
    print()
    print(rewards)

<<<<<<< Updated upstream
def comps(acts):
    unseen = {*range(leng)}
    for i in rewards:
        unseen.remove(i)
    seen = set()
    global comp, rwds
    while unseen:
        start = unseen.pop()
        unseen.add(start)
        stk = [start]
        c = [start]
        r = []
        while stk:
            node = stk.pop()
            unseen.remove(node)
            seen.add(node)
            for i in acts[node]:
                if i not in seen and i not in rewards:
                    stk.append(i)
                    c.append(i)
                if i in rewards:
                    r.append(i)
        comp.append(c)
        rwds.append(r)

def g0(acts):
    for i in rewards:
        policy[i] = '*'
    for i in range(len(rwds)):
        maxrwd = []
        
=======

>>>>>>> Stashed changes

cleaninput(args)
comps(acts)
print(comp, rwds)
#Alexander Yao, 2023, pd 4
