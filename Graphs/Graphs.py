import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read().splitlines()
myWords = set(myList)
import time
from math import log10, floor
 
def degreeCount(myDict):
    myCount = {}
    myMax = 0
    for i in myDict.values():
        j = len(i)
        if j not in myCount.keys():
            myCount[j] = 0
        myCount[j] += 1
        if myMax < j:
            myMax = j
    t = ""
    for i in range(myMax + 1):
        if i in myCount.keys():
            t += str(myCount[i]) + " "
        else:
            t += "0 "
    return t
 
def secondHighest(myDict):
    x = {len(i) for i in myDict.values()}
    x.remove(max(x))
    n = max(x)
    for i in myDict:
        if len(myDict[i]) == n:
            return i
 
def merge(a, b, myComp):
    a = find(a, myComp)
    b = find(b, myComp)
    if a != b:
        myComp[b] = a
 
def find(a, myComp):
    if a is myComp[a]:
        return a
    return find(myComp[a], myComp)
 
def group(myComp):
    for i in myComp.keys():
        myComp[i] = find(i, myComp)
 
def countComp(myComp):
    seen = {}
    for i in myComp.keys():
        if not find(i, myComp) in seen:
            seen[find(i, myComp)] = {i}
        else:
            seen[find(i, myComp)].add(i)
    return seen
 
def edge(a, b):
    return 5 == (a[0] == b[0]) + (a[1] == b[1]) + (a[2] == b[2]) + (a[3] == b[3]) + (a[4] == b[4]) + (a[5] == b[5])
 
def countThree(compSizes, myDict):
    three = 0
    for i in compSizes.values():
        if len(i) == 3:
            j = [*i]
            if edge(j[0], j[1]) and edge(j[0], j[2]) and edge(j[1], j[2]):
                three += 1
    return three
 
def countFour(compSizes, myDict):
    result = 0
    for i in compSizes.values():
        if len(i) == 4:
            j = [*i]
            if edge(j[0], j[1]) and edge(j[0], j[2]) and edge(j[0], j[3]) and edge(j[1], j[2]) and edge(j[1], j[3]) and edge(j[2], j[3]):
                result += 1
    return result
 
def compDif(compSizes):
    seen = {}
    for i in compSizes.values():
        if not len(i) in seen:
            seen[len(i)] = 1
        else:
            seen[len(i)] += 1
    return seen
 
def compMax(compSizes):
    return max([len(i) for i in compSizes.values()])
 
def BFS(start, goal, myDict):
    if start == goal:
        return [start], start
    parseMe = [start]
    dctSeen = {start: 0}
    last = ""
    index = 0
    while index < len(parseMe):
        node = parseMe[index]
        index += 1
        for i in myDict[node]:
            if not i in dctSeen:
                dctSeen[i] = node
                parseMe.append(i)
        if index == len(parseMe):
            last = node
    result = Pathmaker(dctSeen, goal)
    return result, last
 
def Pathmaker(dct, goal):
    result = [goal]
    node = goal
    while node != 0:
        result.append(dct[node])
        node = dct[node]
    return result[-2::-1]
 
def main():
    z = len(args) > 1
    start = time.time()
    myDict = {}
    myEdge = 0
    myComp = {}
    for i in myWords:
        myComp[i] = i
    str = "abcdefghijklmnopqrstuvwxyz"
    for i in myWords:
        myDict[i] = set()
        for j in range(len(i)):
            for k in str:
                l = i[0:j] + k + i[j+1:]
                if(i != l and l in myWords):
                    myDict[i].add(l)
                    myEdge += 1
                    if z:
                        merge(i, l, myComp) #create both the graph and the components at the same time
    end = time.time()
    total = end - start
 
    print("Word count:", len(myWords))                                              #Graph Construction
    print("Edge count:", myEdge // 2)                                               #Number of edges
    print("Degree list:", degreeCount(myDict))                                      #Degree List
    print("Construction time:", round(total, 3 - int(floor(log10(total)))-1), ' s') #Length of Time
 
    if z:
        compSizes = countComp(myComp)
        count = compDif(compSizes)
        s = args[1]
        t = args[2]
        result, farthest = BFS(s, t, myDict)
        three = countThree(compSizes, myDict)
        four = countFour(compSizes, myDict) #Find all the answers or necessary data structures for exercizes 5-13
 
        print("Second degree word:", secondHighest(myDict))
        print("Connected component size count:", len(count))
        print("Largest component size:", compMax(compSizes))
        print("K2 count:", count[2])
        print("K3 count:", three)
        print("K4 count:", four)
        print("Neighbors:", " ".join(myDict[s]))
        print("Farthest:", farthest)
        print("Path:", " ".join(result))
 
main()
 
 
#Alexander Yao, pd 4, 2023
 
 
 
