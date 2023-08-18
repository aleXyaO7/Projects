def createConstraint():
    global CC
    CC = {}
    global solutions
    solutions = []
    for i in range(n):
        for j in range(n):
            ind = i*n+j
            cs = set()
            for k in range(n):
                cs.add(i*n+k)
                cs.add(k*n+j)
                if i >= k:
                    if j >= k:
                        cs.add((i-k)*n+j-k)
                    if j < n - k:
                        cs.add((i-k)*n+j+k)
                if i < n - k:
                    if j >= k:
                        cs.add((i+k)*n+j-k)
                    if j < n - k:
                        cs.add((i+k)*n+j+k)
            cs.remove(ind)
            CC[ind] = cs

def bruteForce(puzzle):
    if isSolution(puzzle):
        solutions.append(puzzle)
    else:
        for pzl in neighbors(puzzle):
            bruteForce(pzl)

def placeQueen(puzzle, pos):
    l = list(puzzle)
    l[pos] = 'Q'
    return ''.join(l)

def neighbors(puzzle):
    ind = 0
    for i in range(n):
        if 'Q' not in puzzle[i*n:i*n+n]:
            break
        ind += 1
    nbrs = []
    for i in range(n):
        new_nbr = placeQueen(puzzle, ind*n+i)
        if valid(new_nbr):
            nbrs.append(new_nbr)
    return nbrs

def valid(puzzle):
    for i in range(len(puzzle)):
        if puzzle[i] == 'Q':
            for j in CC[i]:
                if puzzle[j] == 'Q':
                    return False
    return True

def isSolution(puzzle):
    for i in range(n):
        if 'Q' not in puzzle[i*n:i*n+n]:
            return False
    return valid(puzzle)

def reformat(sols):
    result = []
    for i in sols:
        temp = []
        for j in range(n):
            temp.append(i[j*n:j*n+n])
        result.append(temp)
    return result

def main(N):
    global n
    n = N
    createConstraint()
    bruteForce('.'*n*n)
    global solutions
    solutions = reformat(solutions)
    return solutions

for i in range(10):
    print(len(main(i)))