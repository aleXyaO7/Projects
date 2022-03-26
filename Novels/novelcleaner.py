import sys; args = sys.argv[1:]
myList = open(args[0], 'r').read()
irrelevant = '\",.?!:;()[]- \n\t'
words = {}
total = 0
for i in range(len(myList)):
    if myList[i] in irrelevant: 
        if total > 0:
            if total not in words: words[total] = 0
            words[total] += 1
            total = 0
    total += 1

print(words)