import sys; args = sys.argv[1:]
from PIL import Image; img = Image.open(args[0])
import math
k = int(args[1])
pix = img.load()
h, w = img.size
pixels = {}

for i in range(h):
    for j in range(w):
        color = pix[i, j]
        if color not in pixels: pixels[color] = []
        pixels[color].append((i,j))

start = [(0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255)]
means = {start[i]:[] for i in range(k)}

def dist(p1, p2):
    a, b, c = p1
    d, e, f = p2
    return math.sqrt(math.pow(a-d,2)+math.pow(b-e,2)+math.pow(c-f,2))

def closestmean(p1, means):
    s,t = min([(dist(p1, m), m) for m in means])
    return t

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
        newmeans[(w//z,x//z,y//z)] = []
    means = newmeans

def floodfill():
    global pix
    for i in pixels:
        for a,b in pixels[i]:
            pix[a,b] = closestmean(i,means)

while True:
    tempmeans = dict(means)
    epoch()
    if means == tempmeans: break

floodfill()
print(means)
img.save("kmeans1.png")