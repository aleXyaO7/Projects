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

def safeedgemove(board, pos):
    for i in edgedict[pos]:
        for j in i:
            if board[j] == '.':
                return False
    return True

def findmove(board, token1, token2):
    if board.count('.') <= 10:
        nextmove = negamax(board, token1, token2, '')[1].split(' ')[0]
        if nextmove: return int(nextmove)
        return -1
    pos = findpossible(board, token1, token2)
    if not pos:
        return -1
    corner = [0, 7, 56, 63]
    for i in corner:
        if i in pos:
            return i
    for i in edgenums:
        if i in pos and safeedgemove(board, i):
            return i

    mx = 0
    val = -1000000
    for k in pos:
        newboard = move(board, k, token1, token2)
        newval = evaluate(newboard, token1, token2)
        if newval > val:
            mx = k
            val = newval
    return mx

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

cx = {0:{1,8,9},7:{6,14,15},56:{48,49,57},63:{54,55,62}}
corner = {0,7,56,63}
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

def quickMove(puzzle, token1):
    tokens = ['x','o']
    tokens.remove(token1)
    token2 = tokens[0]
    return findmove(puzzle, token1, token2)

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
#Alexander Yao, Period 4, 2023