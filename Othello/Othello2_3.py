import sys; args = sys.argv[1:]

default = '.' * 27 + 'ox' + '.' * 6 + 'xo' + '.' * 27
puzzle, token1, token2, moves = default, 'x', 'o', []
letters = {'A':0,'a':0,'B':1,'b':1,'C':2,'c':2,'D':3,'d':3,'E':4,'e':4,'F':5,'f':5,'G':6,'g':6,'H':7,'h':7}

#Iterates through the input and cleans it
pointer = 0
if pointer < len(args):
    if len(args[pointer]) == 64:
        t = list(args[0])
        for i in range(64):
            if t[i] in 'XO':
                t[i] = t[i].lower()
        puzzle = ''.join(t)
        pointer += 1
    elif len(args[pointer]) == 0:
        puzzle = default
        pointer += 1
if pointer < len(args):
    if pointer < len(args) and args[pointer] in 'XOxo':
        token1 = args[pointer].lower()
        if token1 == 'o':
            token2 = 'x'
        pointer += 1
    else:
        x = puzzle.count('x')
        o = puzzle.count('o')
        if x > o:
            token1 = 'o'
            token2 = 'x'
if pointer < len(args):
    moves = args[pointer:]

#Finds all directions associated with each index
constraints = {}
for i in range(64):
    constraints[i] = []
    n = [i - j * 8 for j in range(1, i//8 + 1)]
    s = [i + j * 8 for j in range(1, (63 - i)//8 + 1)]
    w = [i - j for j in range(1, i % 8 + 1)]
    e = [i + j for j in range(1, 8 - i % 8)]
    nw = [i - j * 9 for j in range(1, min(i % 8, i//8) + 1)]
    ne = [i - j * 7 for j in range(1, min(8 - i % 8, i//8 + 1))]
    sw = [i + j * 7 for j in range(1, min((63 - i)//8, i % 8) + 1)]
    se = [i + j * 9 for j in range(1, min((63 - i)//8 + 1, 8 - i % 8))]
    lst = [n, s, w, e, nw, ne, sw, se]
    for j in lst:
        if len(j) > 1:
            constraints[i].append(j)

#Cleans the moves into integers
def movescleaner(moves):
    result = []
    for i in moves:
        if i[0] in letters:
            result.append(letters[i[0]] + int(i[1]) * 8 - 8) 
        else:
            if int(i) >= 0:
                result.append(int(i))
    return result

#Checks if a move with the token is valid
def valid(board, pos, t1, t2):
    for i in constraints[pos]:
        flag = False
        for j in i:
            if board[j] == t2:
                flag = True
            elif board[j] == t1 and flag:
                return True
            else:
                break
    return False

#Formats the output (snapshot)
def output(board, pos, possible, t1, t2):
    if pos != '': print(t1, 'moves to', pos)
    temp = list(board)
    for i in possible:
        temp[i] = '*'
    result = ''.join(temp)
    for i in range(8):
        print(result[i * 8:i * 8 + 8])
    print()
    print(board, str(board.count('x')) +  '/' + str(board.count('o')))
    if possible: print('Possible moves for ' + t2 + ':', possible)
    else:
        possible = findpossible(board, t1, t2)
        if possible: print('Possible moves for ' + t1 + ':', possible)
    print()

#Finds all possible moves for next token
def findpossible(board, t1, t2):
    possible = []
    for i in range(64):
        if board[i] == '.' and valid(board, i, t1, t2):
            possible.append(i)
    return possible

#Moves the token and adjusts other tokens accordingly
def move(board, pos, token1, token2):
    result = list(board)
    result[pos] = token1
    for i in constraints[pos]:
        flag = False
        change = []
        for j in i:
            if board[j] == token2:
                flag = True
                change.append(j)
            elif board[j] == token1 and flag:
                for k in change:
                    result[k] = token1
                break
            else:
                break
    return ''.join(result)

#Makes the legal move for either player, finds possible moves and outputs snapshot
def makemove(board, pos, t1, t2):
    if valid(board, pos, t1, t2):
        newboard = move(board, pos, t1, t2)
        possible = findpossible(newboard, t2, t1)
        output(newboard, pos, possible, t1, t2)
        return newboard, t2, t1
    else:
        newboard = move(board, pos, t2, t1)
        possible = findpossible(newboard, t1, t2)
        output(newboard, pos, possible, t2, t1)
        return newboard, t1, t2

#Loops through the moves and moves accordingly
moves = movescleaner(moves)
t1, t2 = token1, token2
output(puzzle, '', findpossible(puzzle, t1, t2), t2, t1)
for i in moves:
    puzzle, t1, t2 = makemove(puzzle, i, t1, t2)

#Alexander Yao, Period 4, 2023