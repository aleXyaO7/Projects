import sys; args = sys.argv[1:]
myList = open(args[2], 'r').read().splitlines()
myWords = set(myList)

h, w = args[0].split('x')
h, w = int(h), int(w)
leng = h * w
pospuzzles = []
conpuzzles = []

rows, cols = [], []
for i in range(h): rows.append([*range(i*w, i*w+w)])
for i in range(w): cols.append([*range(i, i+h*w, w)])
numBlocks = int(args[1])
finaln = numBlocks

nbrs = {}
for i in range(leng):
    nbr = {}
    if i >= w: nbr[i-w] = [i+w, i+2*w, leng-i-w-1, leng-i-2*w-1]
    if i < leng - w: nbr[i+w] = [i-w, i-2*w, leng-i+w-1, leng-i+2*w-1]
    if i % w != 0: nbr[i-1] = [i+1, i+2, leng-i-2, leng-i-3]
    if i % w != w - 1: nbr[i+1] = [i-1, i-2, leng-i, leng-i+1]
    nbrs[i] = nbr

edges = {}
for i in range(w): edges[i] = set()
for i in range(leng-w, leng): edges[i] = set()
for i in range(0, leng-w, w): edges[i] = set()
for i in range(w - 1, leng, w): edges[i] = set()
for i in range(w):
    edges[i].add(i+w)
    edges[i].add(leng-i-w-1)
    edges[i].add(i+2*w)
    edges[i].add(leng-i-2*w-1)
for i in range(leng-w, leng): 
    edges[i].add(i-w)
    edges[i].add(leng-i+w-1)
    edges[i].add(i-2*w)
    edges[i].add(leng-i+2*w-1)
for i in range(0, leng-w, w): 
    edges[i].add(i+1)
    edges[i].add(leng-i-2)
    edges[i].add(i+2)
    edges[i].add(leng-i-3)
for i in range(w - 1, leng, w): 
    edges[i].add(i-1)
    edges[i].add(leng-i)
    edges[i].add(i-2)
    edges[i].add(leng-i+1)

mononbrs = {}
for i in range(leng):
    nbr = []
    if i >= w: nbr.append(i-w)
    if i < leng - w: nbr.append(i+w)
    if i % w != 0: nbr.append(i-1)
    if i % w != w - 1: nbr.append(i+1)
    mononbrs[i] = nbr

blocknbrs = {}
for i in range(leng):
    nbr = {}
    if i+3*w < leng: nbr[i+3*w] = [i+2*w, i+w, leng-i-2*w-1, leng-i-w-1]
    if i-3*w >= 0: nbr[i-3*w] = [i-2*w, i-w, leng-i+2*w-1, leng-i+w-1]
    if i % w > 2: nbr[i-3] = [i-1, i-2, leng-i, leng-i+1]
    if i % w < w - 3: nbr[i+3] = [i+1, i+2, leng-i-3, leng-i-2]
    blocknbrs[i] = nbr

conds = args[3:]

openchar = '-'
blockchar = '#'
tempchar = '$'

puzzle = openchar * leng

#-----------------Structure-----------------

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
        if one[0] == 'H' or one[0] == 'h': puzzle, numBlocks = htcond(puzzle, r, c, word, numBlocks)
        else: puzzle, numBlocks = vtcond(puzzle, r, c, word, numBlocks)
    numBlocks = finaln - puzzle.count(blockchar)
    blocks(puzzle, numBlocks)
    for puz in pospuzzles:
        newp = puz
        for cond in conds:
            one, two = cond[:cond.find('x')], cond[cond.find('x') + 1:]
            r = int(one[1:])
            c, word = intscan(two)
            if one[0] == 'H' or one[0] == 'h': newp = hcond(newp, r, c, word)
            else: newp = vcond(newp, r, c, word)
        conpuzzles.append(newp)

def output(puzzle):
    print()
    for i in range(h):
        print(puzzle[i * w: i * w + w])

def addtemp(puzzle, ind, n, ch):
    lst = list(puzzle)
    lst[ind] = ch
    rev = leng - ind - 1
    newn = n
    if ch == blockchar:
        newn -= 1
        if ind != leng // 2:
            lst[rev] = ch
            newn -= 1
        for i in blocknbrs[ind]:
            if lst[i] == blockchar:
                for j in blocknbrs[ind][i]:
                    if lst[j] == tempchar: return puzzle, n, -1
                    if lst[j] == openchar:
                        lst[j] = blockchar
                        newn -= 1 
        
    else:
        if ind != leng // 2:
            lst[rev] = ch   
        if ind in edges: 
            for i in edges[ind]:
                if lst[i] == blockchar:
                    return puzzle, n, -1
                lst[i] = tempchar
        for i in nbrs[ind]:
            if puzzle[i] == blockchar:
                for j in nbrs[ind][i]:
                    if j < 0 or j >= leng or puzzle[j] == blockchar: return puzzle, n, -1
                    lst[j] = tempchar
    return ''.join(lst), newn, 0

def blocks(puzzle, numBlocks):
    if puzzle.find(openchar) == -1: return puzzle.replace(tempchar, openchar)
    n = numBlocks
    if n == puzzle.count(openchar):
        return puzzle.replace(openchar, blockchar)
    if n % 2 == 1: puzzle, n, t = addtemp(puzzle, leng//2, n, blockchar)
    bf(puzzle, n)

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

def bf(puzzle, numBlocks):
    if not valid([*puzzle]): return ''
    if numBlocks <= 0:
        if valid([*puzzle.replace(openchar, tempchar)]): pospuzzles.append(puzzle.replace(tempchar, openchar))
        return ''
    idx = puzzle.find(openchar)
    if idx == -1: return ''
    npuzzle, n, t = addtemp(puzzle, idx, numBlocks, blockchar)
    if t == 0:
        npuzzle = bf(npuzzle, n)
        if npuzzle: return npuzzle
    npuzzle, n, t = addtemp(puzzle, idx, numBlocks, tempchar)
    if t == 0:
        npuzzle = bf(npuzzle, numBlocks)
        if npuzzle: return npuzzle
    return ''

prep(puzzle, numBlocks, conds)

def quickextractrow(puzzle, r):
    return ''.join([puzzle[i] for i in rows[r]]).split(blockchar)

def quickextractcol(puzzle, r):
    return ''.join([puzzle[i] for i in cols[r]]).split(blockchar)

def quickextract(puzzle):
    allwords = []
    for i in range(h): 
        for j in quickextractrow(puzzle, i): allwords.append(len(j))
    for i in range(w): 
        for j in quickextractcol(puzzle, i): allwords.append(len(j))
    return allwords

def evaluate(wordlength):
    return pow(wordlength, 2)

puzzles = []
for i in conpuzzles: 
    total = 0
    temp = quickextract(i)
    for j in temp: total += evaluate(j)
    puzzles.append((total, i))
puzzles.sort()

#-----------------Creation-----------------

letter = 'abcdefghijklmnopqrstuvwxyz'

def extractrow(puzzle, r):
    words = []
    flag = False
    start = 0
    pointer = 0
    for i in rows[r]:
        if puzzle[i] != blockchar:
            if not flag: 
                start = i
                flag = True
                pointer = 1
            else: pointer += 1
        elif puzzle[i] == blockchar and flag:
            words.append((start, 'H', pointer))
            pointer = 0
            flag = False
    if flag:
        words.append((start, 'H', pointer))
        pointer = 0
        flag = False
    return words

def extractcol(puzzle, r):
    words = []
    flag = False
    start = 0
    pointer = 0
    for i in cols[r]:
        if puzzle[i] != blockchar:
            if not flag: 
                start = i
                flag = True
                pointer = 1
            else: pointer += 1
        elif puzzle[i] == blockchar and flag:
            words.append((start, 'V', pointer))
            pointer = 0
            flag = False
    if flag:
        words.append((start, 'V', pointer))
        pointer = 0
        flag = False
    return words

def extract(puzzle):
    allwords = []
    for i in range(h): 
        for a, b, j in extractrow(puzzle, i): allwords.append((a, b, j))
    for i in range(w): 
        for a, b, j in extractcol(puzzle, i): allwords.append((a, b, j))
    return allwords

def extractwords(lengths):
    words = {}
    for i in lengths:
        words[i] = findwords(i)
    return words

def az(word):
    for i in word:
        if i not in letter: return False
    return True

def findwords(length):
    wds = []
    for i in myWords:
        if len(i) == length and az(i): wds.append(i)
    return wds

def matchingword(puzzle, pos, dr, leng):
    word = ''
    if dr == 'H':
        word = puzzle[pos:pos+leng]
    else:
        word = ''.join([puzzle[i] for i in range(pos, pos + leng * w, w)])

def findmatching(word):
    i = 0

for t, puzzle in puzzles:
    output(puzzle)
    wordpos = extract(puzzle)
    lengths = [c for a, b, c in wordpos]
    words = extractwords(lengths)
    for a, b, c in wordpos: matchingword(puzzle, a, b, c)
    break

#Alexander Yao, Period 4, 2023
