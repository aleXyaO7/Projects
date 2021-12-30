import sys; args = sys.argv[1:]
import time

start = args[0]
row, col = 0, 0
if start.find('x') != -1:
    row, col = start.split('x')
    args = args[1:]
elif start.find('X') != -1:
    row, col = start.split('X')
    args = args[1:]
else:
    row = start
    col = args[1]
    args = args[2:]
row, col = int(row), int(col)

def inputcleaner(args):
    pointer = len(args) - 1
    blocks = []
    while pointer >= 0:
        if args[pointer].find('x') != -1:
            i, j = args[pointer].split('x')
            blocks.append((int(i), int(j)))
            pointer -= 1
        else:
            i, j = args[pointer], args[pointer - 1]
            blocks.append((int(i), int(j)))
            pointer -= 2
    return blocks

def findindex(board):
    return board.find('0')

def checkblock(board, blockrow, blockcol, index):
    if (blockrow * col + index)//col > (len(board))//col:
        return False
    boardend = (index//col + 1) * col
    for i in range(blockcol):
        if index + i >= boardend or board[index + i] != '0':
            return False
    return True

def fillblock(board, blockrow, blockcol, index):
    boardlst = list(board)
    for i in range(blockrow):
        for j in range(blockcol):
            boardlst[index + i * col + j] = '1'
    return ''.join(boardlst)

def choices(board, blocks, index):
    result = []
    for r, c in blocks:
        if checkblock(board, r, c, index) and (c, r) not in result:
            result.append((c * r, c, r))
        if c != r:
            if checkblock(board, c, r, index) and (r, c) not in result:
                result.append((c * r, r, c))
    return sorted(result)[::-1]

def removeblock(blocks, row, col):
    newblock = list(blocks)
    if (row, col) in blocks:
        newblock.remove((row, col))
    else:
        newblock.remove((col, row))
    return newblock

def format(board):
    for i in range(row):
        print(board[i*col:i*col+col])

def formatblocks(blocks):
    result = ''
    for i, j in blocks:
        result += str(i) + 'x' + str(j) + ' '
    return result

def main(board, blocks, holes, blocklist):
    index = findindex(board)
    nbrs = choices(board, blocks, index)
    if not nbrs: 
        newholes = holes + 1
        if newholes > holesmax:
            return '', blocklist
        boardlst = list(board)
        boardlst[index] = '1'
        newholeslist = [i for i in blocklist]
        return main(''.join(boardlst), blocks, newholes, newholeslist + [(1, 1)])
    for t, c, r in nbrs:
        newboard = fillblock(board, r, c, index)
        newblocks = removeblock(blocks, r, c)
        if not newblocks:
            blocklist += [(r, c)]
            if findindex(newboard) != -1:
                for i in range(len(newboard)):
                    if newboard[i] == '0':
                        blocklist += [(1, 1)]
            return newboard, blocklist
        result, holeslist = main(newboard, newblocks, holes, blocklist + [(r, c)])
        if result: 
            return result, holeslist
    newholes = holes + 1
    if newholes > holesmax:
        return '', blocklist
    boardlst = list(board)
    boardlst[index] = '1'
    newholeslist = [i for i in blocklist]
    return main(''.join(boardlst), blocks, newholes, newholeslist + [(1, 1)])

givenblocks = inputcleaner(args)
maxspace = row * col
total = 0
for i, j in givenblocks:
    total += i * j
if total > maxspace:
    print('No solution')
else:
    holesmax = maxspace - total
    board = '0' * row * col
    result, holelist = main(board, givenblocks, 0, [])
    format(result)
    if holelist:
        print('Decomposition: ' + formatblocks(holelist))
    else:
        print('No solution')
print(time.process_time())
#Alexander Yao, pd 4, 2023