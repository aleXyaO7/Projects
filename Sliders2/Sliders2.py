import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()

goal = myList[0]

for i in range((int)(len(goal) ** (1/2)), 0, -1):
    if len(goal) % i == 0:
        global v, h
        v = i
        h = (int)(len(goal)/v)
        break

def inversion(puzzle, goal):
    count = 0
    p, g = puzzle.replace('_', ''), goal.replace('_', '')
    for i in range(len(g)):
        for j in range(i):
            if(p[j] > p[i]):
                count += 1
    if v % 2 == 0:
        count += (puzzle.find('_') // h) - (goal.find('_') // h)
    return count % 2 == 1

def manhatten(start, goal):
    count = 0
    for i in range(len(start)):
        if start[i] != '_':
            h1, w1 = i//v, i%v
            j = goal.find(start[i])
            h2, w2 = j//v, j%v
            count += abs(h2 - h1) + abs(w2 - w1)
    return count

def neighbors(puzzle):
    ind = puzzle.find("_")
    neighbor = []
    if ind < len(puzzle) - h: neighbor[swap(ind, ind + h, puzzle)] = 'D'
    if ind >= h: neighbor[swap(ind, ind - h, puzzle)] = 'U'
    if ind % h != 0: neighbor[swap(ind, ind - 1, puzzle)] = 'L'
    if ind % h != (h - 1): neighbor[swap(ind, ind + 1, puzzle)] = 'R'
    n = [y for (x, y) in sorted((manhatten(i), i) for i in neighbor.keys())]
    print(n)
    input()
    return [y for (x, y) in sorted((i, neighbor[i]) for i in neighbor.keys())]

def swap(i, j, puzzle):
    lst = list(puzzle)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def bibfs(puzzle, goal):
    startSeen = {puzzle}
    startPath = {puzzle: 0}
    endSeen = {goal}
    endPath = {goal: 0}
    

def Pathmaker(dct, start, goal, step):
    result = []
    node = goal
    while node != start:
        result.append(step[node])
        node = dct[node]
    return result[::-1]