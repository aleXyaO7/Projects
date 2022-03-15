import sys; args = sys.argv[1:]
myList = open('dctEckel.txt', 'r').read().splitlines()
myWords = set(myList)

h, w = 7, 7
leng = 49
pospuzzles = []
conpuzzles = []

openchar = '-'
blockchar = '#'
tempchar = '$'

puzzle = '###----#------#---------#---------#------#----###'

letter = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
word = []
spword = {}
awords = {}
splengths = {}
alengths = {}
lengths = [3, 4, 6]

def extractwords(lengths):
    for i in lengths:
        awords[i] = set()
        for j in letter:
            for k in range(i):
                spword[(i, k, j)] = set()
    for i in myWords:
        leng = len(i)
        if leng in lengths and az(i): 
            i = i.lower()
            awords[leng].add(i) 
            for j in range(leng): spword[(leng, j, i[j])].add(i)
    for i, j, k in spword: splengths[(i, j, k)] = len(spword[(i, j, k)])
    for k in awords:
        for i in awords[k]:
            total = 10000
            for j in range(len(i)):
                total = min(total, splengths[(len(i), j, i[j])])
            alengths[i] = total

def az(word):
    for i in word:
        if i not in letter: return False
    return True

extractwords(lengths)
print(spword[(4, 0, 'z')])