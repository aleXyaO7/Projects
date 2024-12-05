def reverse_binary(num, n):
    result = ''
    while num > 0:
        result = str(num % 2) + result
        num //= 2
    return '0' * (n * n - len(result)) + result

def update_board(board, k, n):
    new_board = board[:]
    nbrs = [k]
    if k % n > 0:
        nbrs.append(k-1)
    if k % n < n - 1:
        nbrs.append(k+1)
    if k // n > 0:
        nbrs.append(k-n)
    if k // n < n - 1:
        nbrs.append(k+n)
    for nbr in nbrs:
        new_board[nbr] = 1 - new_board[nbr]
    return new_board

def iterate(n):
    all_boards = {}
    for i in range(pow(2, n * n)):
        board = [0 for _ in range(n * n)]
        flip = reverse_binary(i, n)
        for j in range(n * n):
            if flip[j] == '1':
                board = update_board(board, j, n)
        key = ''.join([str(k) for k in board])
        if key in all_boards:
            print(all_boards[key])
            print(flip)
            input()
        all_boards[key] = flip
    return all_boards

def recur(board, step, n):
    if step == n*n:
        return {''.join([str(i) for i in board])}
    all_boards = set()
    all_boards.update(recur(board, step+1, n))
    all_boards.update(recur(update_board(board, step, n), step+1, n))
    return all_boards

n = 5

all_boards = iterate(n)
all_boards = recur([0 for _ in range(n * n)], 0, n)

print(len(all_boards))