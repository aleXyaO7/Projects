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

lookUp = {}
for ind in range(16):
    lookUp[ind] = []
    if ind % h + 1 != h:
       lookUp[ind].append(ind + 1)
    if ind % h != 0:
        lookUp[ind].append(ind - 1)
    if ind + h < 16:
        lookUp[ind].append(ind + h)
    if ind - h >= 0:
        lookUp[ind].append(ind - h)

dict = {}
for i in range(len(goal)):
    dict[goal[i]] = (i//v, i%v)
q = goal.find('_')
gv, gh = q//v, q%v

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
            (h2, w2) = dict[start[i]]
            count += abs(h2 - h1) + abs(w2 - w1)
    return count

def minhatten(puzzle1, ind1, puzzle2, ind2):
    (t1, t2) = dict[puzzle1[ind2]]
    h1, w1 = ind1//v, ind1%v
    h2, w2 = ind2//v, ind2%v
    r1 = abs(h1 - t1) + abs(w1 - t2)
    s1 = abs(h2 - t1) + abs(w2 - t2)
    if s1 < r1:
        return -1
    else:
        return 1

def neighbors(puzzle, ind):
    neighbor = []
    for i in lookUp[ind]:
        neighbor.append((swap(ind, i, puzzle), i))
    return neighbor

def swap(i, j, puzzle):
    lst = list(puzzle)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)

def astar(start, goal):
    if start == goal: #checks if task is already completed
        return "G"
    if inversion(start, goal):
        return 'X'
    openset = []
    for i in range(52):
        openset.append([])
    pointer = manhatten(start)
    openset[pointer].append((start.find('_'), 0, start, 0)) #creates a list to store unchecked states and a dictionary to keep track of path
    closedset = {}
    point = 0
    while openset: #takes first node
        if point == len(openset[pointer]):
            pointer += 2
            point = 0
        (index, leng, node, parent) = openset[pointer][point]
        point += 1
        if node not in closedset:
            closedset[node] = parent
        for (nbr, ind) in neighbors(node, index):
            if nbr == goal:
                closedset[nbr] = node
                return pathsymbol(Pathmaker(closedset, start, goal))
            if nbr not in closedset:
                p = pointer
                if minhatten(node, index, nbr, ind) > 0:
                    p += 2
                if p < 52:
                    openset[p].append((ind, leng + 1, nbr, node))
    return 'X' #returns no solution

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
        str = astar(i, goal)
        print(i, "was solved with path", str, time.process_time(), len(str))

main()

#Alexander Yao, period 4, 2023