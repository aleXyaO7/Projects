import sys; args = sys.argv[1:]

h, w = args[0].split('x')
h, w = int(h), int(w)
leng = h * w

rows, cols = [], []
for i in range(h): rows.append([*range(i*w, i*w+w)])
for i in range(w): cols.append([*range(i, i+h*w, w)])
numBlocks = int(args[1])

nbrs = {}
for i in range(leng):
    nbr = {}
    if i >= w: nbr[i-w] = [i+w, i+2*w]
    if i < leng - w: nbr[i+w] = [i-w, i-2*w]
    if i % w != 0: nbr[i-1] = [i+1, i+2]
    if i % w != w - 1: nbr[i+1] = [i-1, i-2]
    nbrs[i] = nbr

edges = {}
for i in range(w): edges[i] = set()
for i in range(leng-w, leng): edges[i] = set()
for i in range(0, leng-w, w): edges[i] = set()
for i in range(w - 1, leng, w): edges[i] = set()
for i in range(w):
    edges[i].add(i+w)
    edges[i].add(i+2*w)
for i in range(leng-w, leng): 
    edges[i].add(i-w)
    edges[i].add(i-2*w)
for i in range(0, leng-w, w): 
    edges[i].add(i+1)
    edges[i].add(i+2)
for i in range(w - 1, leng, w): 
    edges[i].add(i-1)
    edges[i].add(i-2)

conds = args[2:]

openchar = '-'
blockchar = '#'
tempchar = '$'

blocknbrs = {}
for i in range(leng):
    nbr = {}
    if i >= w: nbr[i-w] = [i-2*w, i-3*w]
    if i < leng - w: nbr[i+w] = [i+w, i+2*w]
    if i % w != 0: nbr[i-1] = [i-2, i-3]
    if i % w != w - 1: nbr[i+1] = [i+2, i+3]
    blocknbrs[i] = nbr

puzzle = openchar * leng

def intscan(str):
    digits = '0123456789'
    pointer = 0
    for i in str:
        if i not in digits:
            break
        pointer += 1
    return int(str[:pointer]), str[pointer:]

def hcond(puzzle, r, c, word):
    pointer = c
    lst = list(puzzle)
    for i in word:
        lst[r * w + pointer] = i
        pointer += 1
    return ''.join(lst)

def vcond(puzzle, r, c, word):
    pointer = r
    lst = list(puzzle)
    for i in word:
        lst[pointer * w + c] = i
        pointer += 1
    return ''.join(lst)

def htcond(puzzle, r, c, word, n):
    pointer = c
    for i in word:
        if i == blockchar: puzzle, n, t = addtemp(puzzle, r * w + pointer, n, blockchar)
        else: puzzle, n, t = addtemp(puzzle, r * w + pointer, n, tempchar)
        pointer += 1
    return puzzle, n

def vtcond(puzzle, r, c, word, n):
    pointer = r
    for i in word:
        if i == blockchar: puzzle, n, t = addtemp(puzzle, pointer * w + c, n, blockchar)
        else: puzzle, n, t = addtemp(puzzle, pointer * w + c, n, tempchar)
        pointer += 1
    return puzzle, n

def prep(puzzle, numBlocks, conds):
    for cond in conds:
        one, two = cond[:cond.find('x')], cond[cond.find('x') + 1:]
        r = int(one[1:])
        c, word = intscan(two)
        if one[0] == 'H': puzzle, numBlocks = htcond(puzzle, r, c, word, numBlocks)
        else: puzzle, numBlocks = vtcond(puzzle, r, c, word, numBlocks)
    puzzle = blocks(puzzle, numBlocks)
    if not puzzle: return puzzle
    for cond in conds:
        one, two = cond[:cond.find('x')], cond[cond.find('x') + 1:]
        r = int(one[1:])
        c, word = intscan(two)
        if one[0] == 'H': puzzle = hcond(puzzle, r, c, word)
        else: puzzle = vcond(puzzle, r, c, word)
    return puzzle

def output(puzzle):
    for i in range(h):
        print(puzzle[i * w: i * w + w])

def addtemp(puzzle, ind, n, ch):
    lst = list(puzzle)
    lst[ind] = ch
    rev = leng - ind - 1
    if ch == blockchar:
        n -= 1
        if ind != leng // 2:
            lst[rev] = ch
            n -= 1
        for i in blocknbrs[ind]:
            if puzzle[i] == tempchar:
                for j in blocknbrs[ind][i]:
                    if j < 0 or j >= leng or puzzle[j] == blockchar: return puzzle, n, -1
                    lst[j] = tempchar
        for i in blocknbrs[rev]:
            if puzzle[i] == tempchar:
                for j in blocknbrs[rev][i]:
                    lst[j] = tempchar
    else:
        if ind != leng // 2:
            lst[rev] = ch   
        if ind in edges: 
            for i in edges[ind]:
                if lst[i] == blockchar:
                    return puzzle, n, -1
                lst[i] = tempchar
            for i in edges[rev]:
                lst[i] = tempchar
        for i in nbrs[ind]:
            if puzzle[i] == blockchar:
                for j in nbrs[ind][i]:
                    if j < 0 or j >= leng or puzzle[j] == blockchar: return puzzle, n, -1
                    lst[j] = tempchar
        for i in nbrs[rev]:
            if puzzle[i] == blockchar:
                for j in nbrs[rev][i]: lst[j] = tempchar
    return ''.join(lst), n, 0

def blocks(puzzle, numBlocks):
    if puzzle.find(openchar) == -1: return puzzle.replace(tempchar, openchar)
    n = numBlocks
    if n == puzzle.count(openchar):
        return puzzle.replace(openchar, blockchar)
    if n % 2 == 1: puzzle, n, t = addtemp(puzzle, leng//2, n, blockchar)
    puzzle = bf(puzzle, n)
    puzzle = puzzle.replace(tempchar, openchar)
    return puzzle

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
    stk = [p.find(tempchar)]
    while stk:
        node = stk.pop()
        total += 1
        g[node] = '*'
        for i in nbrs[node]:
            if i not in seen and g[i] == tempchar or g[i] == openchar:
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

def bf(puzzle, numBlocks):
    if not valid([*puzzle]): return ''
    if numBlocks <= 0:
        if not valid([*puzzle.replace(openchar, tempchar)]): return ''
        return puzzle
    idx = puzzle.find(openchar)
    if idx == -1: return ''
    npuzzle, n, t = addtemp(puzzle, idx, numBlocks, blockchar)
    npuzzle = bf(npuzzle, n)
    if npuzzle: return npuzzle
    npuzzle, n, t = addtemp(puzzle, idx, numBlocks, tempchar)
    if t == 0:
        npuzzle = bf(npuzzle, numBlocks)
        if npuzzle: return npuzzle
    return ''

output(prep(puzzle, numBlocks, conds))

#Alexander Yao, Period 4, 2023
