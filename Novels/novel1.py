import sys; args = sys.argv[1:]
import nltk, numpy
from nltk.tag import pos_tag
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
myList = open(args[0], 'r').read()
sentences = nltk.sent_tokenize(myList)

def findspoken(myList):
    punctuation = ',.?:;\'\"()-!'
    contractions = ['n\'t']
    flag = False
    spoken = ''
    allspoken = []
    for t in sentences:
        for i in nltk.word_tokenize(t):
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

def removespec(name):
    honorifics = ['Mr.', 'Dr.', 'Mrs.', 'Ms.', 'St.', 'Lt.']
    namesplit = name.split(' ')
    if namesplit[0] in honorifics:
        return ' '.join(namesplit[1:])
    return name

def findcharacters(sentences):
    chs = {}
    for t in sentences:
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(t))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                name = removespec(' '.join(c[0] for c in chunk))
                if name not in chs: chs[name] = 0
                chs[name] += 1
    return chs

print(sentences)
allspoken = findspoken(myList)
allchars = findcharacters(sentences)
print(allchars)