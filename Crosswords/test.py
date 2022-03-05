w, h = 16, 10
leng = w * h
numBlocks = 32

rows, cols = [], []
for i in range(h): rows.append([*range(i*w, i*w+w)])
for i in range(w): cols.append([*range(i, i+h*w, w)])

original = '-----$$$$---------$$$$#-------#$$$$------#----#-----------#$$$#-------#-$---------#$$$#---------$-#-------#$$$#-----------#----#------$$$$#-------#$$$$---------$$$$-----'
puzzle = '------------####------------####------------####------------####--------------------------------####------------####------------####------------####------------'

mononbrs = {}
for i in range(leng):
    nbr = []
    if i >= w: nbr.append(i-w)
    if i < leng - w: nbr.append(i+w)
    if i % w != 0: nbr.append(i-1)
    if i % w != w - 1: nbr.append(i+1)
    mononbrs[i] = nbr

openchar = '-'
blockchar = '#'
tempchar = '$'

def rowcheck(puzzle, lst):
    flag = 0
    empty = False
    for i in lst:
        if puzzle[i] == blockchar:
            if flag != 0 and flag < 3 and empty == False:
                return False
            flag = 0
            empty = False
        elif puzzle[i] == openchar:
            empty = True
        else: flag += 1
    if empty == True or (flag > 2 or flag == 0):
        return True
    return False

def floodfill(puzzle, n):
    p = ''.join(puzzle)
    g = puzzle[:]
    seen = set()
    total = 0
    start = p.find(tempchar)
    if start == -1:
        start = p.find(openchar)
        if start == -1: return n == 0
    stk = [start]
    while stk:
        output(''.join(g))
        print(stk)
        input()
        node = stk.pop()
        total += 1
        g[node] = '*'
        for i in mononbrs[node]:
            if i not in seen and (g[i] == tempchar or g[i] == openchar):
                seen.add(i)
                stk.append(i)

    return total >= (leng - n)

def valid(puzzle):
    for i in range(h): 
        if not rowcheck(puzzle, rows[i]): return False
    for i in range(w): 
        if not rowcheck(puzzle, cols[i]): return False
    if not floodfill(puzzle, numBlocks): return False
    return True

def output(puzzle):
    for i in range(h):
        print(puzzle[i * w: i * w + w])

output(puzzle)
floodfill([*puzzle], 0)