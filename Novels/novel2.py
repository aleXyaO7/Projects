import sys; args = sys.argv[1:]
import nltk, numpy
from nltk.tag import pos_tag
myList = open(args[0], 'r').read()
sentences = nltk.sent_tokenize(myList)

first = {}
last = {}
nick = {}

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
            elif i == '\n':
                spoken += ' '
            elif flag:
                if i[0] not in punctuation and i not in contractions:
                    spoken = spoken + ' ' + i
                else: spoken = spoken + i
    return allspoken

def charseen(f, l):
    if not l: return f in first
    if not f: return l in last
    if f:
        for i in last:
            if i == l: return True
            if i == '' and l:
                i += l
                return True
        return False
    if l:
        for i in first:
            if i == f: return True
            if i == '' and f:
                i += f
                return True
        return False
    return False

def removespec(name):
    honorifics = ['Mr.', 'Dr.', 'Mrs.', 'Ms.', 'St.', 'Lt.']
    endings = ['Jr.', 'Sr.']
    namesplit = name.split(' ')
    h, f, m, l, e, t = '', '', '', '', '', ''
    if namesplit[0] in honorifics: 
        h = namesplit[0]
        namesplit = namesplit[1:]
    if namesplit[len(namesplit) - 1] in endings:
        e = namesplit[len(namesplit) - 1]
        namesplit = namesplit[:len(namesplit) - 1]
    if len(namesplit) == 1:
        t = namesplit[0]
    elif len(namesplit) == 2:
        f = namesplit[0]
        l = namesplit[1]
    else:
        f = namesplit[0]
        l = namesplit[len(namesplit) - 1]
    if not charseen(f, l) and not charseen('', t) and not charseen(t, ''):
        if t: l = t
        if f:
            if f not in first: first[f] = []
            first[f].append(l)
        if l:
            if l not in last: last[l] = []
            last[l].append(f)

def findcharacters(sentences):
    chs = {}
    for t in sentences:
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(t))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                removespec(' '.join(c[0] for c in chunk))
    return chs

print(sentences)
allspoken = findspoken(myList)
allchars = findcharacters(sentences)
print(allchars)
print(first)
print(last)