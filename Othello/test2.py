edge = [[0,1,2,3,4,5,6,7],[0,8,16,24,32,40,48,56],[56,57,58,59,60,61,62,63],[7,15,23,31,39,47,55,63]]
cornernums = [0, 7, 56, 63]
edgenums = {1,2,3,4,5,6,8,15,16,23,24,31,32,39,40,47,48,55,57,58,59,60,61,62}
edgedict = {}
for i in edgenums:
    edgedict[i] = []
    for j in edge:
        if i in j:
            edgedict[i].append(j[0:j.index(i)][::-1])
            edgedict[i].append(j[j.index(i) + 1:len(j)])

def safeedgemove(board, pos, token2):           #Othello4 method
    flag1, flag2 = 0, 0
    for j in edgedict[pos][0]:
        if board[j] == token2:
            flag1 = 1
            break
        if board[j] == '.':
            flag1 = 2
            break
    for j in edgedict[pos][1]:
        if board[j] == token2:
            flag2 = 1
            break
        if board[j] == '.':
            flag2 = 2
            break
    if flag1 + flag2 > 2:
        return False
    return True

print(safeedgemove('xo..............................................................', 2, 'o'))