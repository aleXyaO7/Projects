# CS3100 - Spring 2024 - Programming Assignment 5
#################################
# Collaboration Policy: You may discuss the problem and the overall
# strategy with up to 4 other students, but you MUST list those people
# in your submission under collaborators.  You may NOT share code,
# look at others' code, or help others debug their code.  Please read
# the syllabus carefully around coding.  Do not seek published or online
# solutions for any assignments. If you use any published or online resources
# (which may not include solutions) when completing this assignment, be sure to
# cite them. Do not submit a solution that you are unable to explain orally to a
# member of the course staff.
#################################

from __future__ import print_function
import sys
import time
from TilingDino import TilingDino

fp = open("test2.txt", 'r')
fulllines = fp.readlines()
lines = []
for line in fulllines:
    lines.append(line.strip())


# Call the tiling dino function passing in the
# contents of the file
start = time.time()
td = TilingDino()
result = td.compute(lines)
end = time.time()

for i in range(len(result)):
    print(result[i])
print("time: "+ str(end-start))
