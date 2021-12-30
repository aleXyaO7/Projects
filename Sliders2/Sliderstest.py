import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import time

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
    for i in g:
        count += p.find(i)
        p = p.replace(i, '')
    if v % 2 == 0:
        count += (puzzle.find('_') // h) - (goal.find('_') // h)
    return count % 2 == 1

def manhatten(start):
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
    if ind < len(puzzle) - h: neighbor.append(swap(ind, ind + h, puzzle))
    if ind >= h: neighbor.append(swap(ind, ind - h, puzzle))
    if ind % h != 0: neighbor.append(swap(ind, ind - 1, puzzle))
    if ind % h != (h - 1): neighbor.append(swap(ind, ind + 1, puzzle))
    return [y for (x, y) in sorted((manhatten(i), i) for i in neighbor)]

def swap(i, j, puzzle):
    lst = list(puzzle)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def bfs(start, goal):
    if start == goal: #checks if task is already completed
        return "G"
    if inversion(start, goal):
        return 'X'
    parseMe = [start] #creates a list to store unchecked states and a dictionary to keep track of path
    dctSeen = {start: 0}
    for node in parseMe: #takes first node
        dct = neighbors(node)
        for i in dct: #finds neighbors
            if i == goal: #checks if goal is reached
                dctSeen[i] = node
                return pathsymbol(Pathmaker(dctSeen, start, goal)) #finds path
            if not i in dctSeen: #otherwise adds node to list
                dctSeen[i] = node
                parseMe.append(i)
    return '' #returns no solution

def Pathmaker(dct, start, goal):
    result = [goal]
    node = goal
    while node != start:
        result.append(dct[node])
        node = dct[node]
    return result[::-1]

def pathsymbol(path):
    result = ""
    i = path[0]
    indi = i.find('_')
    r = {1:'R', -1:'L', v:'D', -v:'U'}
    for j in path[1:]:
        indj = j.find('_')
        result += r[indj-indi]
        i = j
        indi = indj
    return result


def main():
    for i in myList:
        str = bfs(i, goal)
        print(i, "was solved with path", str)

main()

#Alexander Yao, period 4, 2023