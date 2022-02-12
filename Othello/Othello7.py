from json.encoder import INFINITY
import sys; args = sys.argv[1:]
# Alexander Yao, pd 4
LIMIT_NM = 13
LIMIT_MG = 3

import random, time

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

default = '.' * 27 + 'ox' + '.' * 6 + 'xo' + '.' * 27

def output(board, t1, t2):      #Snapshot
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
    print('My prefered move is', findmove(board, t1, t2))
    print()

    if board.count('.') < LIMIT_NM:
        score, path = alphabeta(board, t1, t2, -64, 64)
        path = ' '.join(path.split(' ')[::-1])
        print('score:', score,', path', path)

def valid(board, pos, t1, t2):      #Checks if move is valid
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

def findpossible(board, t1, t2):    #Finds valid moves
    possible = []
    for i in range(64):
        if board[i] == '.' and valid(board, i, t1, t2):
            possible.append(i)
    return possible

weights = {
    0:100000,7:100000,56:100000,63:100000,
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
cornernums = [0, 7, 56, 63]
edgenums = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
edgedict = {}
for i in edgenums:
    edgedict[i] = []
    for j in edge:
        if i in j:
            edgedict[i].append({*j} - {i})

def safeedgemove(board, pos):           #Othello4 method
    for i in edgedict[pos]:
        for j in i:
            if board[j] == '.':
                return False
    return True

def findmove(board, token1, token2):        #Othello4's findmove
    if board.count('.') < LIMIT_NM:
        nextmove = alphabeta(board, token1, token2, -INFINITY, INFINITY)[1].split(' ')[0]
        if nextmove: return int(nextmove)
    else:
        nextmove = midgame(board, token1, token2, -INFINITY, INFINITY, LIMIT_MG)[1].split(' ')[0]
        if nextmove: return int(nextmove)
    return -1

def move(board, pos, token1, token2):       #Makes a move
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
def evaluate(board, token1, token2):        #Evaluates how good a position is
    total = 0
    for i in cornernums:
        if board[i] == token1: total += 100000
    for i in edgenums:
        if safeedgemove(board, i) and board[i] == token1: total += 5000
    cxtotal = {*findpossible(board, token2, token1)}
    for i in corner:
        if board[i] == '.':
            cxtotal -= cx[i]
    total1 = len(cxtotal)
    for i in corner:
        if i in cxtotal:
            total1 += 20
    
    return total - total1

def weightedpos(board, pos, token1, token2):        #Weights the positions depending on their evaluation
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

def quickMove(puzzle, token1):          #Quickmove method
    tokens = ['x','o']
    tokens.remove(token1)
    token2 = tokens[0]
    return findmove(puzzle, token1, token2)

def midgame(board, token1, token2, alpha, beta, depth):
    if depth == -1:
        return evaluate(board, token1, token2), ''
    p1 = findpossible(board, token1, token2)
    if not p1:
        p2 = findpossible(board, token2, token1)
        if not p2:
            k = board.count(token1) - board.count(token2)
            return k, ''
    
    nextmoves = ''
    if p1:
        p1 = weightedpos(board, p1, token1, token2)
        for i in p1:
            score, newpath = midgame(move(board, i, token1, token2), token2, token1, -1 * beta, -1 * alpha, depth - 1)
            score = -score
            if score >= beta:
                return score, ''
            if score <= alpha:
                continue
            alpha = score
            nextmoves = str(i) + ' ' + newpath
    else:
        maxi, new = midgame(board, token2, token1, -1 * beta, -1 * alpha, depth - 1)
        return -maxi, '-1 ' + new

    return alpha, nextmoves

def alphabeta(board, token1, token2, alpha, beta):
    p1 = findpossible(board, token1, token2)
    if not p1:
        p2 = findpossible(board, token2, token1)
        if not p2:
            k = board.count(token1) - board.count(token2)
            return k, ''
    
    nextmoves = ''
    if p1:
        p1 = weightedpos(board, p1, token1, token2)
        for i in p1:
            score, newpath = alphabeta(move(board, i, token1, token2), token2, token1, -1 * beta, -1 * alpha)
            score = -score
            if score >= beta:
                return score, ''
            if score <= alpha:
                continue
            alpha = score
            nextmoves = str(i) + ' ' + newpath
    else:
        maxi, new = alphabeta(board, token2, token1, -1 * beta, -1 * alpha)
        return -maxi, '-1 ' + new

    return alpha, nextmoves

def endgame(board, token1, token2):             #Checks if game is over
    one, two = 0, 0
    for i in board:
        if i == token1:
            one += 1
        elif i == token2:
            two += 1
    return one, two

def randommove(board, token1, token2):          #Makes random move
    pos = findpossible(board, token1, token2)
    if not pos:
        return -1
    rand = random.randint(0, len(pos) - 1)
    return pos[rand]

def tournamentmove(bd, token1, token2, result):         #Simulates a tournament game
    result = result + ''
    board = str(bd)
    randmove = randommove(board, token1, token2)
    if randmove != -1:
        board = move(board, randmove, token1, token2)
        m = str(randmove)
        if len(m) == 1: m = '_' + m
        result += m
        playermove = quickMove(board, token2)
        if playermove != -1:
            m = str(playermove)
            if len(m) == 1: m = '_' + m
            result += m
            board = move(board, playermove, token2, token1)
        else: result += '-1'
    else:
        playermove = quickMove(board, token2)
        if playermove == -1:
            return board, -1, result
        else:
            result += '-1'
            board = move(board, playermove, token2, token1)
            m = str(playermove)
            if len(m) == 1: m = '_' + m
            result += m
    return board, 0, result

def tournament():                               #Simulates tournament
    rcount, pcount = 0, 0
    scores = []
    games = []
    result = ''
    rand = random.randint(0, 100)
    for k in range(rand):
        token1 = 'x'
        token2 = 'o'
        puzzle = default
        while True:
            puzzle, i, result = tournamentmove(puzzle, token1, token2, result)
            if i == -1:
                one, two = endgame(puzzle, token1, token2)
                if one > two:
                    one = 64 - two
                elif two > one:
                    two = 64 - one
                rcount += one
                pcount += two
                scores.append(two - one)
                while result[-2:] == '-1':
                    result = result[:-2]
                games.append((two - one, result, 'o', k))
                result = ''
                break
    for k in range(100-rand):
        token1 = 'o'
        token2 = 'x'
        puzzle = default
        playermove = quickMove(puzzle, token2)
        puzzle = move(puzzle, playermove, token2, token1)
        result += str(playermove)
        while True:
            puzzle, i, result = tournamentmove(puzzle, token1, token2, result)
            if i == -1:
                one, two = endgame(puzzle, token1, token2)
                if one > two:
                    one = 64 - two
                elif two > one:
                    two = 64 - one
                rcount += one
                pcount += two
                scores.append(str(two - one))
                while result[-2:] == '-1':
                    result = result[:-2]
                games.append((two - one, result, 'x', k + rand))
                result = ''
                break
    
    for i in range(10):
        for j in range(10):
            print(scores[i * 10 + j], end = ' ')
        print()
    print()
    print('My Tokens:', pcount, ';', 'Opponent Tokens:', rcount)
    print('Score:', pcount/(rcount + pcount)*100, '%')
    print('NM/AB Limit:', LIMIT_NM)
    print()

    games.sort()
    score, path, token, num = games[0]
    print('Game', num, ':', token, '=>', score, ':')
    print(path)
    score, path, token, num = games[1]
    print('Game', num, ':', token, '=>', score, ':')
    print(path)

    print()
    print('Elapsed time:', time.process_time(), 's')

def main():
    if args:
        pointer = 0
        board, token1, token2 = default, 'x', 'o'
        if pointer < len(args) and len(args[pointer]) == 64:
            board = args[0]
            pointer += 1
        if pointer < len(args) and len(args[pointer]) == 1:
            token1 = args[1]
            token2 = ['x', 'o'][token1 == 'x']
            pointer += 1
        else:
            token1 = ['x', 'o'][board.count('.') % 2]
            token2 = ['x', 'o'][token1 == 'x']
        if pointer < len(args):
            if len(args[pointer]) <= 2:
                for i in args[pointer:]:
                    if int(i) < 0: continue
                    board = move(board, int(i), token1, token2)
                    token1 = 'xo'[token1=='x']
                    token2 = 'xo'[token1=='x']
            else:
                for i in range(len(args[pointer:][0])//2):
                    j = args[pointer][i*2:i*2+2]
                    if '_' in j: j = j[1]
                    if int(j) < 0: continue
                    board = move(board, int(j), token1, token2)
                    token1 = 'xo'[token1=='x']
                    token2 = 'xo'[token1=='x']
        if findpossible(board, token1, token2):
            output(board, token1, token2)
        else:
            output(board, token2, token1)
    else:
        tournament()

main()
#Alexander Yao, Period 4, 2023