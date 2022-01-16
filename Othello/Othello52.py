import sys; args = sys.argv[1:]
import time
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

    score, path, k = negamax(puzzle, token1, token2, '')
    path += k
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

cache = {}
def negamax(board, token1, token2, path):
    if (board, token1) in cache:
        score, path2 = cache[(board, token1)]
        return score, path, path2
    p1 = findpossible(board, token1, token2)
    if not p1:
        p2 = findpossible(board, token2, token1)
        if not p2:
            k = board.count(token1) - board.count(token2)
            cache[(board, token1)] = k, ''
            return k, path, ''
    
    totalmoves = {}
    if p1:
        for i in p1:
            score, oldpath, newpath = negamax(move(board, i, token1, token2), token2, token1, path + ' ' + str(i))
            totalmoves[str(i) + ' ' + newpath] = -1 * score
    else:
        maxi, old, new = negamax(board, token2, token1, path + ' -1')
        return -maxi, path, '-1 ' + new

    maxi = -64
    nextmoves = 0
    for i in totalmoves:
        if maxi < totalmoves[i]:
            maxi = totalmoves[i]
            nextmoves = i
    cache[(board, token1)] = maxi, nextmoves
    return maxi, path, nextmoves

output(puzzle, token1, token2)
print(time.process_time())
#Alexander Yao, Period 4, 2023