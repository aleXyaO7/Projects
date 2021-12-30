jug1 = (int)(input("Enter value of first jug."))
jug2 = (int)(input("Enter value of second jug."))
final = (int)(input("Enter value of amount of water."))

def neighbors(j1, j2):
    nbr = []
    if j1 > 0: nbr.append((0, j2))
    if j2 > 0: nbr.append((j1, 0))
    if j1 > 0 and j2 < jug2: nbr.append((max(j1 + j2 - jug2, 0), min(jug2, j1 + j2)))
    if j1 < jug1 and j2 > 0: nbr.append((min(jug1, j1 + j2), max(j1 + j2 - jug1, 0)))
    if j1 < jug1: nbr.append((jug1, j2))
    if j2 < jug2: nbr.append((j1, jug2))
    return nbr

def BFS():
    queue = []
    path = {}
    path[(0, 0)] = 0
    queue.append((0, 0))
    for j1, j2 in queue:
        for k1, k2 in neighbors(j1, j2):
            if k1 == final or k2 == final:
                path[(k1, k2)] = (j1, j2)
                return Pathmaker(path, (0, 0), (k1, k2))
            if (k1, k2) not in path:
                queue.append((k1, k2))
                path[(k1, k2)] = (j1, j2)
    return -1

def Pathmaker(dct, start, goal):
    result = [goal]
    node = goal
    while node != start:
        result.append(dct[node])
        node = dct[node]
    return result[::-1]

def main():
    result = BFS()
    if result == -1:
        print("Impossible to solve.")
    else:
        for i in result:
            print(i)

main()