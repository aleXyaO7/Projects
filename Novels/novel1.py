import sys; args = sys.argv[1:]
import nltk
myList = open(args[0], 'r').read()
t = nltk.word_tokenize(myList)

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

print(allspoken)