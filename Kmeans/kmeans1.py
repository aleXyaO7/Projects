import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import math
k = int(args[1])
pix = img.load()
h, w = img.size
leng = h*w
pixels = {}
nbrs = {}
for ind in range(leng): 
    stk = []
    if ind % w != w - 1:
        stk.append(ind + 1)
    if ind % w != 0:
        stk.append(ind - 1)
    if ind + w < leng:
        stk.append(ind + w)
    if ind - w >= 0:
        stk.append(ind - w)
    if ind % w != w - 1 and ind + w < leng:
        stk.append(ind + w + 1)
    if ind % w != 0 and ind + w < leng:
        stk.append(ind + w - 1)
    if ind % w != w - 1 and ind - w >= 0:
        stk.append(ind + 1 - w)
    if ind % w != 0 and ind - w >= 0:
        stk.append(ind - 1 - w)
    nbrs[ind] = stk

for i in range(h):
    for j in range(w):
        color = pix[i, j]
        if color not in pixels: pixels[color] = []
        pixels[color].append((i,j))
maxamount = 0
maxpixel = ()
for i in pixels:
    if len(i) > maxamount:
        maxpixel = i
        maxamount = len(i)

start = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]
means = {start[i]:[] for i in range(k)}
grid = []
for i in range(h):
    grid.append([])
    for j in range(w):
        grid[i].append(0)
dct = {}

def dist(p1, p2):
    a, b, c = p1
    d, e, f = p2
    return math.sqrt(math.pow(a-d,2)+math.pow(b-e,2)+math.pow(c-f,2))

def closestmean(p1, means):
    s,t = min([(dist(p1, m), m) for m in means])
    return t

def sort(points, means):
    for i in points:
        means[closestmean(i, means)].append(i)
    return means

def findmean(points):
    w,x,y,z = 0,0,0,0
    if not points:
        return 0
    for a,b,c in points:
        n = pixels[(a,b,c)]
        x += a * n
        y += b * n
        z += c * n
        w += n

def epoch():
    global means
    newmeans = {}
    temp = {}
    for i in means: 
        temp[i] = (0,0,0,0)
    for d,e,f in pixels:
        a, b, c = closestmean((d,e,f), means)
        w, x, y, z = temp[(a,b,c)]
        n = len(pixels[(d,e,f)])
        w += d * n
        x += e * n
        y += f * n
        z += n
        temp[(a,b,c)] = (w,x,y,z)
    for a,b,c in temp:
        w,x,y,z = temp[(a,b,c)]
        if z != 0:
            newmeans[(w//z,x//z,y//z)] = []
        else: newmeans[(w,x,y)] = []
    means = newmeans

def reimage():
    global pix
    for i in pixels:
        for a,b in pixels[i]:
            m = closestmean(i,means)
            pix[a,b] = m
            means[pix[a,b]].append((a,b))
            grid[a][b] = str(dct[m])

def dfs(val):
    global grid
    total = []
    while str(val) in ''.join([''.join(i) for i in grid]):
        mp = ''.join([''.join(i) for i in grid])
        ind = mp.find(str(val))
        t = 0
        stk = [ind]
        while stk:
            node = stk.pop()
            grid[node//w][node%w] = '*'
            t += 1
            for i in nbrs[node]:
                if grid[i//w][i%w] == str(val):
                    stk.append(i)
        total.append(t)
    return total

def floodfill():
    total = []
    for i in range(k):
        for j in dfs(i):
            total.append(j)
    return total

def output():
    print('Size:', h, 'x', w)
    print('Pixels:', h*w)
    print('Distinct pixel count:', len(pixels))
    print('Most common pixel:', maxpixel, '->', maxamount)
    print('Final means:')
    pointer = 1
    for i in means:
        print(str(pointer) + ':', i, '=>', len(means[i]))
        pointer += 1
    print('Region counts:', ', '.join([str(i) for i in floodfill()]))

def train():
    while True:
        tempmeans = dict(means)
        epoch()
        if means == tempmeans: break
    pointer = 0
    for i in means:
        dct[i] = pointer
        pointer += 1

train()
reimage()
output()
img.save("kmeans.png")
#Alexander Yao, Period 4, 2023