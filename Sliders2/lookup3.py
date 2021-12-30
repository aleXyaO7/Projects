import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
import time

goal = myList[0]

lookUp = {}
for ind in range(16):
    lookUp[ind] = []
    if ind % 4 + 1 != 4:
       lookUp[ind].append(ind + 1)
    if ind % 4 != 0:
        lookUp[ind].append(ind - 1)
    if ind + 4 < 16:
        lookUp[ind].append(ind + 4)
    if ind - 4 >= 0:
        lookUp[ind].append(ind - 4)

dict = {}
for i in range(len(goal)):
    dict[goal[i]] = (i//4, i%4)
q = goal.find('_')
gv, gh = q//4, q%4

def inversion(puzzle, goal):
    count = 0
    p, g = puzzle.replace('_', ''), goal.replace('_', '')
    for i in g:
        count += p.find(i)
        p = p.replace(i, '')
    if 4 % 2 == 0:
        count += (puzzle.find('_') // 4) - (goal.find('_') // 4)
    return count % 2 == 1

def manhatten(start):
    count = 0
    for i in range(len(start)):
        if start[i] != '_':
            h1, w1 = i//4, i%4
            (h2, w2) = dict[start[i]]
            count += abs(h2 - h1) + abs(w2 - w1)
    return count


def minhatten(puzzle1, ind1, puzzle2, ind2):
    (t1, t2) = dict[puzzle1[ind2]]
    r = ind2
    s = ind1
    h1, w1 = r//4, r%4
    h2, w2 = s//4, s%4
    r1 = abs(h1 - t1) + abs(w1 - t2)
    s1 = abs(h2 - t1) + abs(w2 - t2)
    if s1 < r1:
        return -1
    else:
        return 1

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
    paths = 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
    point = 0
    if start in branch:
        return branch[start]
    while openset: #takes first node
        while point == len(openset[pointer]):
            pointer += 2
            point = 0
        if pointer >= len(paths):
            break
        (index, leng, node, parent) = openset[pointer][point]
        point += 1
        if node not in closedset:
            closedset[node] = parent
        for ind in lookUp[index]:
            nbr = swap(index, ind, node)
            if nbr == goal:
                closedset[nbr] = node
                return pathsymbol(Pathmaker(closedset, start, goal), '')
            if nbr in branch:
                closedset[nbr] = node
                p = pathsymbol(Pathmaker(closedset, start, nbr), branch[nbr])
                if len(paths) > len(p):
                    paths = p
            if nbr not in closedset:
                p = pointer
                if minhatten(node, index, nbr, ind) > 0:
                    p += 2
                if p < len(paths):
                    openset[p].append((ind, leng + 1, nbr, node))
    return paths #returns no solution

def Pathmaker(dct, start, goal):
    result = [goal]
    node = goal
    while node != start:
        result.append(dct[node])
        node = dct[node]
    return result[::-1]

def pathsymbol(path, leg):
    result = ""
    i = path[0]
    indi = i.find('_')
    r = {1:'R', -1:'L', 4:'D', -4:'U'}
    for j in path[1:]:
        indj = j.find('_')
        result += r[indj-indi]
        i = j
        indi = indj
    return result + leg

def ballgen(puzzle, gen):
    result = {}
    for i in gen:
        k = genneighbors(i)
        for j in k:
            if j not in puzzle:
                puzzle[j] = k[j] + puzzle[i]
                result[j] = puzzle[j]
    return puzzle, result

def genneighbors(puzzle):
    ind = puzzle.find("_")
    neighbor = {}
    if ind < 12: neighbor[swap(ind, ind + 4, puzzle)] = 'U'
    if ind >= 4: neighbor[swap(ind, ind - 4, puzzle)] = 'D'
    if ind % 4 != 0: neighbor[swap(ind, ind - 1, puzzle)] = 'R'
    if ind % 4 != (3): neighbor[swap(ind, ind + 1, puzzle)] = 'L'
    return neighbor

def main():
    for i in myList:
        str = astar(i, goal)
        print(i, "was solved with path", str, time.process_time(), len(str))

branch = {goal : ''}
gen = {goal : ''}
for i in range(12):
    branch, gen = ballgen(branch, gen)

main()

#Alexander Yao, period 4, 2023