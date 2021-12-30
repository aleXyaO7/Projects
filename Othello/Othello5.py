import sys; args = sys.argv[1:]
puzzle = args[0]
token1 = args[1]
token2 = ['x', 'o'][token1 == 'x']

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

def output(board, t1, t2):
    possible = findpossible(board, t1, t2)
    temp = list(board)
    for i in possible:
        temp[i] = '*'
    result = ''.join(temp)
    for i in range(8):
        print(result[i * 8:i * 8 + 8])
    
    print()
    
    print(board, str(board.count('x')) +  '/' + str(board.count('o')))
    if possible: print('Possible moves for ' + t1 + ':', possible)
    else:
        possible = findpossible(board, t2, t1)
        if possible: print('Possible moves for ' + t2 + ':', possible)
    
    print()

    score, path = negamax(puzzle, token1, token2, '')
    path = ' '.join(path.split(' ')[::-1])
    print('score:', score,', path', path)

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

def findpossible(board, t1, t2):
    possible = []
    for i in range(64):
        if board[i] == '.' and valid(board, i, t1, t2):
            possible.append(i)
    return possible

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

def negamax(board, token1, token2, path):
    p1 = findpossible(board, token1, token2)
    if not p1:
        p2 = findpossible(board, token2, token1)
        if not p2:
            return board.count(token1) - board.count(token2), path
    
    totalmoves = {}
    k = ''
    if p1:
        for i in p1:
            newpath = path + ' ' + str(i)
            score, newpath = negamax(move(board, i, token1, token2), token2, token1, newpath)
            totalmoves[newpath] = -1 * score
    else:
        maxi, k = negamax(board, token2, token1, path + ' -1')
        return -maxi, k

    maxi = -64
    moves = 0
    for i in totalmoves:
        if maxi < totalmoves[i]:
            maxi = totalmoves[i]
            moves = i
    return maxi, moves

output(puzzle, token1, token2)
#Alexander Yao, Period 4, 2023