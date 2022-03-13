myList = open('dct20k.txt', 'r').read().splitlines()
myWords = set(myList)
import random

h, w = 7, 7
leng = 49
pospuzzles = []
conpuzzles = []

openchar = '-'
blockchar = '#'
tempchar = '$'

puzzle = '###----#------#---------#---------#------#----###'

letter = 'abcdefghijklmnopqrstuvwxyz'
word = []
def extractwords():
    for i in myWords:
        leng = len(i)
        if leng == 7 and az(i): 
            word.append(i)

def az(word):
    for i in word:
        if i not in letter: return False
    return True

extractwords()
print(len(word))