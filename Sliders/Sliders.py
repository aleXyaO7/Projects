import sys; args = sys.argv[1:]
import time
from math import log10, floor
# Alex Yao, pd 4
global puzzle, goal
puzzle = args[0]
try:
    goal = args[1]
except:
    goal = ''.join(sorted(puzzle)).replace('_', '') + '_'
def main():
    for i in range((int)(len(puzzle) ** (1/2)), 0, -1):
        if len(puzzle) % i == 0:
            global v, h
            v = i
            h = (int)(len(puzzle)/v)
            break
    print()
    Format(BFS(puzzle, goal))
 
def neighbors(puzzle):
    ind = puzzle.find("_")
    neighbor = []
    if ind < len(puzzle) - h:
        lst = list(puzzle)
        lst[ind], lst[ind + h] = lst[ind + h], lst[ind]
        neighbor.append(''.join(lst))
    if ind >= h:
        lst = list(puzzle)
        lst[ind], lst[ind - h] = lst[ind - h], lst[ind]
        neighbor.append(''.join(lst))
    if ind % h != 0:
        lst = list(puzzle)
        lst[ind], lst[ind - 1] = lst[ind - 1], lst[ind]
        neighbor.append(''.join(lst))
    if ind % h != (h - 1):
        lst = list(puzzle)
        lst[ind], lst[ind + 1] = lst[ind + 1], lst[ind]
        neighbor.append(''.join(lst))
        #neighbor.append(''.join((puzzle[:ind], puzzle[ind + 1], puzzle[ind], puzzle[ind + 2:])))
    return neighbor
 
def BFS(start, goal):
    if start == goal:
        return [start]
    parseMe = [start]
    dctSeen = {start: 0}
    while parseMe:
        node = parseMe.pop(0)
        for i in neighbors(node):
            if i == goal:
                dctSeen[i] = node
                return Pathmaker(dctSeen, goal)
            if not i in dctSeen:
                dctSeen[i] = node
                parseMe.append(i)
    return []
 
def Pathmaker(dct, goal):
    result = [goal]
    node = goal
    while node != 0:
        result.append(dct[node])
        node = dct[node]
    return result[-2::-1]
 
def Format(result):
    if(result):
        for k in range(len(result)//12 + 1):
            for j in range(v):
                res = []
                for i in result[k * 12:(k + 1) * 12]:
                    res.append(''.join(i[j * h:(j + 1)*h]))
                print('  '.join(res))
            print()
        print("Steps: " + (str)(len(result) - 1))
    else:
        for j in range(v):
            print(''.join(puzzle[j * h:(j + 1)*h]))
        print("Steps: -1")
    print('')
start = time.time()
main()
end = time.time()
total = end - start
print('Time: ', round(total, 3 - int(floor(log10(total)))-1), ' s')
 
 

