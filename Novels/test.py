import nltk
from nltk.tag import pos_tag

sentence = 'On the very day that I had come to this conclusion, I was standing at the Criterion Bar, when some one tapped me on the shoulder, and turning round I recognized young Stamford, who had been a dresser under me at Bart\'s.'

t = nltk.word_tokenize(sentence)
entities = pos_tag(t)
mainchars = []

print(entities)

for chunk in nltk.ne_chunk(nltk.pos_tag(t)):
    if hasattr(chunk, 'label'):
        mainchars.append((chunk.label(), ' '.join(c[0] for c in chunk)))

print(mainchars)