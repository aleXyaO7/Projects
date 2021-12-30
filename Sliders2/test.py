goal = 'ABCDEFGHIJKLMNO_'
def linear(puzzle):
    count = 0
    for i in range(4):
        pz1 = puzzle[4*i:4*i+4].replace('_', '')
        pz2 = goal[4*i:4*i+4].replace('_', '')
    for i in pz1:
        if i not in pz2:
            pz1 = pz1.replace(i, '')
    for i in pz2:
        if i not in pz1:
            pz2 = pz2.replace(i, '')
    for i in pz1:
        pz1 = pz1.replace(i, (str)(pz2.find(i)))
    count += lin[pz1]
    for i in range(4):
        pz1 = ''.join([puzzle[i],puzzle[4+i],puzzle[8+i],puzzle[12+i]]).replace('_', '')
        pz2 = ''.join([goal[i],goal[4+i],goal[8+i],goal[12+i]]).replace('_', '')
    for i in pz1:
        if i not in pz2:
            pz1 = pz1.replace(i, '')
    for i in pz2:
        if i not in pz1:
            pz2 = pz2.replace(i, '')
    for i in pz1:
        pz1 = pz1.replace(i, (str)(pz2.find(i)))
    count += lin[pz1]
    return count

lin = {
    '0':0,
    '01':0,
    '10':1,
    '012':0,
    '021':1,
    '102':1,
    '120':1,
    '201':1,
    '210':2,
    '0123':0,
    '0132':1,
    '0213':1,
    '0231':1,
    '0213':1,
    '0321':2,
    '1023':1,
    '1032':2,
    '1203':1,
    '1230':1,
    '1203':1,
    '1320':2,
    '2103':2,
    '2130':2,
    '2013':1,
    '2031':2,
    '2013':1,
    '2301':2,
    '3120':2,
    '3102':2,
    '3210':3,
    '3201':2,
    '3012':1,
    '3021':2
}

print(linear('ABCDEFGHIJKLMO_N'))