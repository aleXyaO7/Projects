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
    nbr = []
    if i >= w: nbr.append(i-w)
    if i < leng - w: nbr.append(i+w)
    if i % w != 0: nbr.append(i-1)
    if i % w != w - 1: nbr.append(i+1)
    nbrs[i] = nbr

conds = args[2:]

openchar = '-'
blockchar = '#'
tempchar = '$'

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

def prep(puzzle, numBlocks, conds):
    for cond in conds:
        one, two = cond[:cond.find('x')], cond[cond.find('x') + 1:]
        r = int(one[1:])
        c, word = intscan(two)
        if one[0] == 'H': puzzle = hcond(puzzle, r, c, word)
        else: puzzle = vcond(puzzle, r, c, word)
    puzzle = blocks(puzzle, numBlocks - puzzle.count(blockchar))
    return puzzle

def output(puzzle, w, h):
    for i in range(h):
        print(puzzle[i * w: i * w + w])

def addtemp(puzzle, ind, n, ch):
    lst = list(puzzle)
    lst[ind] = ch
    n -= 1
    if ind != leng // 2:
        lst[leng - ind] = ch
        n -= 1
    return ''.join(lst), n

def blocks(puzzle, numBlocks):
    n = numBlocks
    if n == puzzle.count(openchar):
        return puzzle.replace(openchar, blockchar)
    
    lst = list(puzzle)
    for i in range(leng):
        if lst[i] == blockchar:
            lst[leng - i - 1] = blockchar
            n -= 1
        elif lst[i] != openchar and lst[leng - i - 1] == openchar and i != leng//2:
            lst[leng - i - 1] = tempchar
    
    puzzle = bf(''.join(lst), n)
    
    puzzle = puzzle.replace(tempchar, openchar)
    return puzzle

def rowcheck(puzzle, lst):
    flag = 0
    for i in lst:
        if puzzle[i] == blockchar:
            if flag != 0 and flag < 3:
                return False
            flag = 0
        else: flag += 1
    if flag > 2 or flag == 0:
        return True
    return False

def floodfill(puzzle, n):
    p = ''.join(puzzle)
    seen = set()
    total = 0
    stk = [p.find(tempchar)]
    while stk:
        node = stk.pop()
        total += 1
        for i in nbrs[node]:
            if i not in seen and i == blockchar:
                seen.add(i)
                stk.append(i)
    return total == n

def valid(puzzle):
    for i in range(h): 
        if not rowcheck(puzzle, rows[i]): return False
    for i in range(w): 
        if not rowcheck(puzzle, cols[i]): return False
    if not floodfill(puzzle, numBlocks): return False
    return True

def bf(puzzle, numBlocks):
    if numBlocks == 0:
        temp = [*puzzle.replace(openchar, tempchar)]
        if valid(temp):
            return ''.join(temp)
        return ''
    idx = puzzle.find(openchar)
    npuzzle, n = addtemp(puzzle, idx, numBlocks, blockchar)
    npuzzle = bf(puzzle, numBlocks)
    if npuzzle: return npuzzle
    npuzzle, n = addtemp(puzzle, idx, numBlocks, tempchar)
    npuzzle = bf(puzzle, numBlocks)
    if npuzzle: return npuzzle
    return ''

output(prep(puzzle, numBlocks, conds), w, h)

#Alexander Yao, Period 4, 2023