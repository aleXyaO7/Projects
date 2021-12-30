def win(pzl):
    for i in nbrs:
        x = True
        o = True
        for j in i:
            if j == 'x':
                o = False
            elif j == 'o':
                x = False
            else:
                o = x = False
        if x == True:
            return 0
        elif o == True:
            return 1
    return -1

def move(pzl, char):
    lst = list(pzl)
    allpzl = []
    for i in range(len(pzl)):
        if pzl[i] == '.':
            lst[i] = char
            allpzl.append(''.join(lst))
            lst[i] = '.'
    return allpzl

def nextmove(pzl, char1, char2):
    t = win(pzl)
    if t == 0:
        return 1, 0
    elif t == 1:
        return 0, 1
    if pzl.find('.') == -1:
        return 0, 0
    xwins = 0
    owins = 0
    for subpzl in move(pzl, char1):
        x, o = nextmove(subpzl, char2, char1)
        xwins += x
        owins += o
    return xwins, owins

def findbestmove(pzl, char1, char2):
    f=1

char1, char2 = 'x', 'o'
r, c = 3, 3
nbrs = [{c * i + j for j in range(c)} for i in range(r)] + [{c * j + i for j in range(r)} for i in range(c)] + [{0, 4, 8}] + [{2, 4, 6}]
