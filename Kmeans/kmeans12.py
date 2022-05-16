import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import math
k = int(args[1])
pix = img.load()
h, w = img.size
leng = h*w
pixels = {}
nbrs = {}
rvpixels = {}
for i in range(h):
    for j in range(w):
        color = pix[i, j]
        if color not in pixels: pixels[color] = []
        pixels[color].append((i,j))
        nbrs[(i,j)] = []
        if i != 0: nbrs[(i,j)].append((i-1, j))
        if j != 0: nbrs[(i,j)].append((i, j-1))
        if i != h-1: nbrs[(i,j)].append((i+1, j))
        if j != w-1: nbrs[(i,j)].append((i, j+1))
        if i != 0 and j != 0: nbrs[(i,j)].append((i-1, j-1))
        if i != 0 and j != w-1: nbrs[(i,j)].append((i-1, j+1))
        if i != h-1 and j != 0: nbrs[(i,j)].append((i+1, j-1))
        if i != h-1 and j != w-1: nbrs[(i,j)].append((i+1, j+1))

maxamount = 0
maxpixel = ()
for i in pixels:
    if len(pixels[i]) >= maxamount:
        maxpixel = i
        maxamount = len(pixels[i])
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

def findmean(points):
    l,x,y,z = 0,0,0,0
    if not points:
        return 0
    for a,b,c in points:
        n = len(pixels[(a,b,c)])
        x += a * n
        y += b * n
        z += c * n
        l += n
    return (x//l,y//l,z//l)

def sortpoints(points, means):
    clusters = {}
    for i in means:
        clusters[i] = []
    for i in points:
        m = closestmean(i, means)
        for j in pixels[i]:
            clusters[m].append(j)
            rvpixels[j] = m
    return clusters

def epoch(means, points, sums):
    clusters = {}
    newmeans = []
    tempsums = {}
    newsums = {}
    for i in range(k):
        clusters[means[i]] = []
        newsums[means[i]] = 0
        tempsums[means[i]] = 0
    for i in points:
        m = closestmean(i, means)
        clusters[m].append(i)
        tempsums[m] += i[0]*i[0]+i[1]*i[1]+i[2]*i[2]
    for i in means:
        if tempsums[i] == sums[i]:
            newmeans.append(i)
            newsums[i] = tempsums[i]
        else:
            newm = findmean(clusters[i])
            newmeans.append(newm)
            newsums[newm] = tempsums[i]
    return newmeans, newsums

def length(mean, clusters):
    total = 0

    for i in clusters[mean]:
        total += len(pixels[i])
    return total

def output(means):
    print('Size:', h, 'x', w)
    print('Pixels:', h*w)
    print('Distinct pixel count:', len(pixels))
    print('Most common pixel:', maxpixel, '->', maxamount)
    print('Final means:')
    pointer = 1
    clusters = sortpoints(pixels, means)
    for i in means:
        print(str(pointer) + ':', i, '=>', len(clusters[i]))
        pointer += 1
    print('Region counts:', ', '.join([str(i) for i in floodfill()]))

def dictcompare(dct1, dct2):
    for i in dct1:
        if i not in dct2: return False
        if dct1[i] != dct2[i]: return False
    return True

def reimage(means):
    global pix
    for i in pixels:
        for a,b in pixels[i]:
            m = closestmean(i,means)
            pix[a,b] = m
            means[pix[a,b]].append((a,b))
            grid[a][b] = str(dct[m])

def floodfill():
    total = []
    seen = set()
    unseen = set()
    for i in range(h):
        for j in range(w):
            unseen.add((i,j))
    while unseen:
        node = unseen.pop()
        stk = [node]
        t = 0
        while stk:
            n = stk.pop()
            t += 1
            seen.add(n)
            for i in nbrs[n]:
                if rvpixels[i] == rvpixels[n] and i not in seen:
                    stk.append(i)
        total.append(t)
    return total

means = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)][:k]
sums = {}
for i in means:
    sums[i] = 0
while True:
    psums = {i:sums[i] for i in sums}
    means, sums = epoch(means, pixels, sums)
    if dictcompare(sums, psums): break

output(means)
reimage(means)
#Alexander Yao, Period 4, 2023