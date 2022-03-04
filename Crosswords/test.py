leng = 24
w, h = 4, 6
edges = set()
for i in range(w): edges.add(i)
for i in range(leng-w, leng): edges.add(i)
for i in range(0, leng-w, w): edges.add(i)
for i in range(w - 1, leng, w): edges.add(i)
print(edges)