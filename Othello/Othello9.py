import time
# Alexander Yao, pd 4
logging = True
LIMIT_NM = 13
LIMIT_MG = 3
constraints = {}
default = '.' * 27 + 'ox' + '.' * 6 + 'xo' + '.' * 27
edge = []
edgenums = {0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63}
edgedict = {}
cx = {0:{1,8,9},7:{6,14,15},56:{48,49,57},63:{54,55,62}}
corner = {0,7,56,63}
weight_c = 1000000
weight_e = 5000
weight_m = 1
weight_mc = 20
weight_me = 5
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
for i in edgenums:
    edgedict[i] = []
    for j in edge:
        if i in j:
            edgedict[i].append({*j} - {i})

class Strategy:

    def valid(self, board, pos, t1, t2):      #Checks if move is valid
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

    def findpossible(self, board, t1, t2):    #Finds valid moves
        possible = []
        for i in range(64):
            if board[i] == '.' and self.valid(board, i, t1, t2):
                possible.append(i)
        return possible

    def safeedgemove(self, board, pos):           #Othello4 method
        for i in edgedict[pos]:
            for j in i:
                if board[j] == '.':
                    return False
        return True

    def findmove(self, board, token1, token2):        #Othello7's findmove
        if board.count('.') < LIMIT_NM:
            nextmove = self.alphabeta(board, token1, token2, -10000000, 10000000)[1].split(' ')[0]
            if nextmove: return int(nextmove)
        else:
            nextmove = self.midgame(board, token1, token2, -10000000, 10000000, LIMIT_MG)[1].split(' ')[0]
            if nextmove: return int(nextmove)
        return -1

    def findmove4(self, board, token1, token2):        #Othello4's findmove
        pos = self.findpossible(board, token1, token2)
        if not pos:
            return -1
        for i in corner:
            if i in pos:
                return i
        for i in edgenums:
            if i in pos and self.safeedgemove(board, i):
                return i

        mx = 0
        val = -1000000
        for k in pos:
            newboard = self.move(board, k, token1, token2)
            newval = self.evaluate(newboard, token1, token2)
            if newval > val:
                mx = k
                val = newval
        return mx

    def move(self, board, pos, token1, token2):       #Makes a move
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

    def mobility(self, board, token1, token2, weight_mc, weight_me):
        cxtotal = {*self.findpossible(board, token2, token1)}
        for i in corner:
            if board[i] == '.':
                cxtotal -= cx[i]
        total1 = len(cxtotal)
        for i in corner:
            if i in cxtotal:
                total1 += weight_mc
        for i in edgenums:
            if i in cxtotal and self.safeedgemove(board, i): total1 += weight_me
        return total1

    def evaluate(self, board, token1, token2):        #Evaluates how good a position is
        total = 0
        for i in corner:
            if board[i] == token1: total += weight_c
        for i in edgenums:
            if self.safeedgemove(board, i) and board[i] == token1: total += weight_e
        totalm = self.mobility(board, token1, token2, weight_mc, weight_me)
        return total - totalm * weight_m

    def weightedpos(self, board, pos, token1, token2):        #Weights the positions depending on their evaluation
        result = []
        for i in corner:
            if i in pos:
                pos.remove(i)
                result.append(i)
        for i in edgenums:
            if i in pos and self.safeedgemove(board, i):
                pos.remove(i)
                result.append(i)
        temp = []
        for k in pos:
            newboard = self.move(board, k, token1, token2)
            newval = self.evaluate(newboard, token1, token2)
            temp.append((newval, k))
        temp.sort()
        temp2 = [i for j,i in temp[::-1]]
        result = result + temp2
        return result

    def midgame(self, board, token1, token2, alpha, beta, depth):
        if depth == -1:
            return self.evaluate(board, token1, token2), ''
        p1 = self.findpossible(board, token1, token2)
        if not p1:
            p2 = self.findpossible(board, token2, token1)
            if not p2:
                k = board.count(token1) - board.count(token2)
                return k, ''
        
        nextmoves = ''
        if p1:
            p1 = self.weightedpos(board, p1, token1, token2)
            for i in p1:
                score, newpath = self.midgame(self.move(board, i, token1, token2), token2, token1, -1 * beta, -1 * alpha, depth - 1)
                score = -score
                if score >= beta:
                    return score, ''
                if score <= alpha:
                    continue
                alpha = score
                nextmoves = str(i) + ' ' + newpath
        else:
            maxi, new = self.midgame(board, token2, token1, -1 * beta, -1 * alpha, depth - 1)
            return -maxi, '-1 ' + new

        return alpha, nextmoves

    def alphabeta(self, board, token1, token2, alpha, beta):
        p1 = self.findpossible(board, token1, token2)
        if not p1:
            p2 = self.findpossible(board, token2, token1)
            if not p2:
                k = board.count(token1) - board.count(token2)
                return k, ''
        
        nextmoves = ''
        if p1:
            p1 = self.weightedpos(board, p1, token1, token2)
            for i in p1:
                score, newpath = self.alphabeta(self.move(board, i, token1, token2), token2, token1, -1 * beta, -1 * alpha)
                score = -score
                if score >= beta:
                    return score, ''
                if score <= alpha:
                    continue
                alpha = score
                nextmoves = str(i) + ' ' + newpath
        else:
            maxi, new = self.alphabeta(board, token2, token1, -1 * beta, -1 * alpha)
            return -maxi, '-1 ' + new

        return alpha, nextmoves

    def endgame(self, board, token1, token2):             #Checks if game is over
        one, two = 0, 0
        for i in board:
            if i == token1:
                one += 1
            elif i == token2:
                two += 1
        return one, two

    def best_strategy(self, board, player, best_move, running):
        time.sleep(1)
        player2 = 'xo'[player == 'x']
        if running.value:
            best_move.value = self.findmove4(board, player, player2)
            best_move.value = self.findmove(board, player, player2)

#Alexander Yao, Period 4, 2023