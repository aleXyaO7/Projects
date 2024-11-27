import sys
fp = open("input.txt", 'r')
alphabet = 'abcdefghijklmnopqrstuvwxyz'
punctuation = '.,!?()-'
words = []
lines = fp.readlines()
for i in range(0, len(lines)):
    line = lines[i].strip().replace(punctuation, '')
    for j in line.split(' '):
        if not j == '':
            words.append(j)

print(words)

