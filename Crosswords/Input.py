import sys; args = sys.argv[1:]

h, w = args[0].split('x')
h, w = int(h), int(w)

numBlocks = int(args[1])

myList = open(args[2], 'r').read().splitlines()
myDict = set(myList)

conds = args[3:]

puzzle = '-' * w * h

def intscan(str):
    digits = '0123456789'
    pointer = 0
    for i in str:
        if i not in digits:
            break
        pointer += 1
    return int(str[:pointer]), str[pointer:]

def hcond(puzzle, r, c, word, w):
    pointer = c
    lst = list(puzzle)
    for i in word:
        lst[r * w + pointer] = i
        pointer += 1
    return ''.join(lst)

def vcond(puzzle, r, c, word, w):
    pointer = r
    lst = list(puzzle)
    for i in word:
        lst[pointer * w + c] = i
        pointer += 1
    return ''.join(lst)

def prep(puzzle, conds, w):
    for cond in conds:
        one, two = cond.split('x')
        r = int(one[1:])
        c, word = intscan(two)
        if one[0] == 'H': puzzle = hcond(puzzle, r, c, word, w)
        else: puzzle = vcond(puzzle, r, c, word, w)
    return puzzle

def output(puzzle, w, h):
    for i in range(h):
        print(puzzle[i * w: i * w + w])
    
output(prep(puzzle, conds, w), w, h)