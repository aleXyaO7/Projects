import sys; args = sys.argv[1:]
myLines = open(args[0], 'r').readlines()
myList = ' '.join([i.strip() for i in myLines])
irrelevant = '\",.?!:;()[]- \n\t'
words = {}
total = 0
for i in range(len(myList)):
    if myList[i] in irrelevant: 
        if total > 0:
            if total not in words: words[total] = 0
            words[total] += 1
            total = 0
    else: total += 1

print(words)