import nltk
from nltk.tag import pos_tag

sentence = 'I quickly said, @0'

person = ''
for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))[::-1]:
    a, b = chunk
    print(a, b)
    if b == 'PRP' or b == 'NNP' or b == 'PRP$' or b == 'NN':
        person += a + ' '
    elif b == 'VBD': continue
    else: 
        print(person)
        break