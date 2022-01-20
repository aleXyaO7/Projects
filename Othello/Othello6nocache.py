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

cx = {0:{1,8,9},7:{6,14,15},56:{48,49,57},63:{54,55,62}}
corner = {0,7,56,63}
weights = {
    0:99,7:99,56:99,63:99,
    1:-8,6:-8,8:-8,15:-8,48:-8,55:-8,57:-8,62:-8,
    2:8,5:8,16:8,23:8,40:8,47:8,58:8,61:8,
    3:6,4:6,24:6,31:6,32:6,39:6,59:6,60:6,
    9:-24,14:-24,49:-24,54:-24,
    10:-4,13:-4,17:-4,22:-4,41:-4,46:-4,50:-4,53:-4,
    11:-3,12:-3,25:-3,30:-3,33:-3,38:-3,51:-3,52:-3,
    18:7,21:7,42:7,45:7,
    19:4,20:4,26:4,29:4,34:4,37:4,43:4,44:4,
    27:0,28:0,35:0,36:0
}
edge = [[0,1,2,3,4,5,6,7],[0,8,16,24,32,40,48,56],[56,57,58,59,60,61,62,63],[7,15,23,31,39,47,55,63]]
edgenums = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
edgedict = {}
for i in edgenums:
    edgedict[i] = []
    for j in edge:
        if i in j:
            edgedict[i].append({*j} - {i})

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

    score, path = alphabeta(puzzle, token1, token2, -64, 64)
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

def safeedgemove(board, pos):
    for i in edgedict[pos]:
        for j in i:
            if board[j] == '.':
                return False
    return True

def evaluate(board, token1, token2):
    total = sum([weights[i] for i in range(64) if board[i] == token1])
    cxtotal = {*findpossible(board, token2, token1)}
    for i in cx:
        if board[i] == '.':
            cxtotal -= cx[i]
    total1 = len(cxtotal)
    for i in corner:
        if i in cxtotal:
            total1 += 9
    
    return total - total1 * 100

def weightedpos(board, pos, token1, token2):
    result = []
    for i in corner:
        if i in pos:
            pos.remove(i)
            result.append(i)
    for i in edgenums:
        if i in pos and safeedgemove(board, i):
            pos.remove(i)
            result.append(i)
    temp = []
    for k in pos:
        newboard = move(board, k, token1, token2)
        newval = evaluate(newboard, token1, token2)
        temp.append((newval, k))
    temp.sort()
    temp2 = [i for j,i in temp[::-1]]
    result = result + temp2
    return result

def alphabeta(board, token1, token2, alpha, beta):
    p1 = findpossible(board, token1, token2)
    if not p1:
        p2 = findpossible(board, token2, token1)
        if not p2:
            k = board.count(token1) - board.count(token2)
            return k, ''
    
    value = -64
    newalpha = alpha
    returnpath = ''
    if p1:
        p1 = weightedpos(board, p1, token1, token2)
        for i in p1:
            score, npath = alphabeta(move(board, i, token1, token2), token2, token1, -1 * beta, -1 * alpha)
            value = max(value, -score)
            if newalpha < value:
                newalpha = value
                returnpath = str(i) + ' ' + npath
            if newalpha >= beta:
                returnpath = ''
                break
    else:
        maxi, new = alphabeta(board, token2, token1, -1 * beta, -1 * alpha)
        return -maxi, '-1 ' + new

    return newalpha, returnpath

output(puzzle, token1, token2)
print(time.process_time())
#Alexander Yao, Period 4, 2023