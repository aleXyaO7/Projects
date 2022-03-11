w, h = 13, 13
leng = w * h
numBlocks = 32

myList = open('dct20k.txt', 'r').read().splitlines()
myWords = set(myList)

rows, cols = [], []
for i in range(h): rows.append([*range(i*w, i*w+w)])
for i in range(w): cols.append([*range(i, i+h*w, w)])

puzzle = '----#cafe#-------#----#-------#--------###----#-----------#orb###-----#-w-#-------#ten#-------#-w-#-----###moo#-----------#----###--------#-------#----#-------#----#----'

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

letter = 'abcdefghijklmnopqrstuvwxyz'
spword = {}
awords = {}

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
    for i in lengths:
        awords[i] = set()
        for j in letter:
            for k in range(i):
                spword[(i, k, j)] = set()
    for i in myWords:
        leng = len(i)
        if leng in lengths and az(i): 
            awords[leng].add(i) 
            for j in range(leng): spword[(leng, j, i[j])].add(i)

def az(word):
    for i in word:
        if i not in letter: return False
    return True

def findwords(word):
    leng = len(word)
    allwords = awords[leng]
    for i in range(leng):
        if word[i] != openchar: allwords = allwords & spword[(leng, i, word[i])]
    return allwords

def matchingword(puzzle, pos, dr, leng):
    word = ''
    if dr == 'H':
        word = puzzle[pos:pos+leng]
    else:
        word = ''.join([puzzle[i] for i in range(pos, pos + leng * w, w)])
    print(word)
    return findwords(word)

def output(puzzle):
    for i in range(h):
        print(puzzle[i * w: i * w + w])

output(puzzle)
wordpos = extract(puzzle)
lengths = [c for a, b, c in wordpos]
extractwords(lengths)
print(matchingword(puzzle, 107, 'H', 3))