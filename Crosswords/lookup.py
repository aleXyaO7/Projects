w, h = 13, 13
leng = w * h
blocknbrs = {}
for i in range(leng):
    nbr = {}
    if i+3*w < leng: nbr[i+3*w] = [i+2*w, i+w, leng-i-2*w-1, leng-i-w-1]
    if i-3*w >= 0: nbr[i-3*w] = [i-2*w, i-w, leng-i+2*w-1, leng-i+w-1]
    if i % w > 2: nbr[i-3] = [i-1, i-2, leng-i, leng-i+1]
    if i % w < w - 3: nbr[i+3] = [i+1, i+2, leng-i-3, leng-i-2]
    blocknbrs[i] = nbr

print(blocknbrs)