import sys; args = sys.argv[1:]
import nltk, numpy
from nltk.tag import pos_tag
myList = open(args[0], 'r').read()
t = nltk.word_tokenize(myList)

def findspoken(myList):
    punctuation = ',.?:;\'\"()-!'
    contractions = ['n\'t']
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
            if i[0] not in punctuation and i not in contractions:
                spoken = spoken + ' ' + i
            else: spoken = spoken + i
    return allspoken

def findcharacters(t):
    chs = {}
    entities = pos_tag(t)
    for i, j in entities:
        if j == 'NNP':
            if i not in chs: chs[i] = 1
            else: chs[i] += 1
    return chs

allspoken = findspoken(myList)
allchars = findcharacters(t)
print(allchars)