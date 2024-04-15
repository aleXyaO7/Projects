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
# Your Computing ID: qxe3fj
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen
#################################

class TilingDino:
    def __init__(self):
        return

    # This is the method that should set off the computation
    # of Tiling Dino.  It takes as input a list lines of input
    # as strings.  You should parse that input, find a tiling,
    # and return a list of strings representing the tiling
    #
    # @return the list of strings representing the tiling

    def to_string(o1, o2, e1, e2):
        return o1 + ' ' + o2 + ' ' + e1 + ' ' + e2
    
    def to_coords(str):
        s = str.split(' ')
        return int(s[0]), int(s[1]), int(s[2]), int(s[3])

    def compute(self, lines):
        odds = set()
        evens = set()
        for r in range(len(lines)):
            for c in range(len(lines[r])):
                if lines[r][c] == '.':
                    if (r + c) % 2:
                        odds.add((c, r))
                    else:
                        evens.add((c, r))
        
        if len(odds) != len(evens):
            return 'impossible'
        
        start = len(odds)
        end = 0

        edges = {}
        dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for o1, o2 in odds:
            for d1, d2 in dir:
                if (o1 + d1, o2 + d2) in evens:
                    edges[]
