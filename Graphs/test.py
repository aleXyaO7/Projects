def BFS(start, goal, myDict):
    if start == goal:
        return [start], start
    parseStart = [start]
    dctSeenStart = {start: 0}
    parseGoal = [goal]
    dctSeenGoal = {goal: 0}
    indexs = 0
    indexg = 0
    while parseStart and parseGoal:
        if indexs < len(parseStart):
            node = parseStart.pop(0)
            if node in dctSeenGoal.values():
                return Pathmaker(dctSeenStart, dctSeenGoal, start, goal, node)
            for i in myDict[node]:
                if i not in dctSeenStart:
                    dctSeenStart[i] = node
        if indexg < len(parseGoal):
            node = parseGoal.pop(0)
            if node in dctSeenStart.values():
                return Pathmaker(dctSeenStart, dctSeenGoal, start, goal, node)
            for i in myDict[node]:
                if i not in dctSeenStart:
                    dctSeenStart[i] = node
        print(parseStart)
        print(parseGoal)
        input()
    return []

def Pathmaker(dcts, dctg, start, goal, n):
    result = [goal]
    node = goal
    while node != n:
        result.append(dctg[node])
        node = dctg[node]
    while node != 0:
        result.append(dcts[node])
        node = dcts[node]
    return result[-2::-1]

def main():
    myDict = {}
    str = "abcdefghijklmnopqrstuvwxyz"
    for i in myWords:
        myDict[i] = set()
        for j in range(len(i)):
            for k in str:
                l = i[0:j] + k + i[j+1:]
                if(i != l and l in myWords):
                    myDict[i].add(l)
    print(myDict)
    print(BFS('abased', 'abases', myDict))

import sys; args = sys.argv[1:]
myList = open('words.txt', 'r').read().splitlines()
myWords = set(myList)
main()
            