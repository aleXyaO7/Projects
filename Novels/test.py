import sys; args = sys.argv[1:]
import nltk
myList = open(args[0], 'r').read()
t = nltk.word_tokenize(myList)

print(t)

flag = False
spoken = ''
allspoken = []
for i in t:
    if i == '``': 
        flag = True
    elif i == '\'\'': 
        flag = False
        allspoken.append(spoken)
        spoken = ''
    elif flag:
        spoken = spoken + i + ' '

print(t)
