h, w = 1, 3
rows, cols = [], []
for i in range(h): rows.append([*range(i*w, i*w+w)])
for i in range(w): cols.append([*range(i, i+h*w, w)])
print(rows)
print(cols)
blockchar = '#'
def rowcheck(puzzle, lst):
    flag = 0
    for i in lst:
        if puzzle[i] == blockchar:
            if flag != 0 and flag < 3:
                return False
            flag = 0
        else: flag += 1
    if flag > 2 or flag == 0:
        return True
    return False

print(rowcheck([*'##--#'], rows[0]))