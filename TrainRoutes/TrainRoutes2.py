from math import pi, acos, sin, cos
from tkinter import *


#Graph Creation
def createGraph():
    temp = open('./rrNodes.txt', 'r').read().splitlines()
    temp2 = open('./rrEdges.txt', 'r').read().splitlines()
    temp3 = open('./rrNodeCity.txt', 'r').read().splitlines()
    nodes = {}
    edges = {}
    cities = {}

    for n in temp:
        i,j,k = n.split(' ')
        nodes[i] = (float(j), float(k))
        edges[i] = set()
    
    for n in temp2:
        i, j = n.split(' ')
        edges[i].add(j)
        edges[j].add(i)

    for n in temp3:
        i, j = n.split(' ', 1)
        cities[j] = i
    
    return nodes, edges, cities, temp2


#Astar Function
def astar(start, goal):
    if start == goal: return [start]
    openset = []
    y1, x1 = n[start]
    y2, x2 = n[goal]
    startlen = calcd(y1,x1,y2,x2)
    openset.append((startlen, 0, start, 0))
    closedset = {}
    seen = []
    while openset:
        openset = sorted(openset)
        h, leng, node, par = openset.pop(0)
        if node in closedset: continue
        else:
            nodey, nodex = n[node]
            if par != 0:
                pary, parx = n[par]
                seen.append((1, translate(nodey, nodex), translate(pary, parx)))
            closedset[node] = par
            if node == goal: return closedset, seen, leng
            for nbr in e[node]:
                nbry, nbrx = n[nbr]
                openset.append((calcd(nbry, nbrx, y2, x2), leng + calcd(nbry, nbrx, nodey, nodex), nbr, node))
                seen.append((0, translate(nbry, nbrx), translate(nodey, nodex)))

#Heuristic Calculator
def calcd(y1, x1, y2, x2):
    R = 3958.76
    y1 = y1 * pi / 180.0
    x1 = x1 * pi / 180.0
    y2 = y2 * pi / 180.0
    x2 = x2 * pi / 180.0
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

#Pathmaker 
def Pathmaker(dct, start, goal, seen):
    result = [goal]
    node = goal
    while node != start:
        result.append(dct[node])
        nodey, nodex = n[node]
        newy, newx = n[dct[node]]
        seen.append((2, translate(nodey, nodex), translate(newy, newx)))
        node = dct[node]
    return result[::-1]


#Heap methods
def extract(lst):
    if len(lst) == 1:
        return lst.pop(0)
    lst[0], lst[len(lst)-1] = lst[len(lst)-1], lst[0]
    val = lst.pop()
    heapdown(lst, 0)
    return val

def add(lst, node):
    lst.append(node)
    heapup(lst, len(lst) - 1)
    
def heapdown(lst, index):
    left,right = index * 2 + 1, index * 2 + 2
    m = lst[index][0]
    if not isleaf(lst, index) and ((lst[left][0]) < m or (right < len(lst) and (lst[right][0]) < m)):
        new = [left, right][right<len(lst) and lst[right][0]<lst[left][0]]
        lst[index], lst[new] = lst[new], lst[index]
        heapdown(lst, new)

def heapup(lst, index):
    if index == 0: return
    par = (index - 1)//2
    m,p = lst[index][0], lst[par][0]
    if m < p:
        lst[index], lst[par] = lst[par], lst[index]
        heapup(lst, par)

def isleaf(lst, index):
    return 2*index + 2 > len(lst)

def translate(y, x):
    return x*11+1550, y*-14+800

n, e, c, ed = createGraph()

root = Tk()
canvas = Canvas(root, height=600, width = 1000, bg="#fff")
canvas.pack(expand=True)
img = PhotoImage(file="Map.png")
canvas.create_image(500, 250, image = img)
for line in ed:
    i = line.split()
    y1, x1 = n[i[0]]
    y2, x2 = n[i[1]]
    line = canvas.create_line([translate(y1,x1), translate(y2,x2)])

s = input()
g = input()
start, goal = c[s], c[g]
path, seen, length = astar(start, goal)
print(Pathmaker(path, start, goal, seen))
print('Length:', length, 'mi')
for n, node1, node2 in seen:
    line = canvas.create_line([node1,node2])
    if n == 0:
        canvas.itemconfig(line, fill="red")
        canvas.update()
    elif n == 1:
        canvas.itemconfig(line, fill="green")
        canvas.update()
    else:
        canvas.itemconfig(line, fill="white")
root.mainloop()

#Alexander Yao, Period 4, 2023