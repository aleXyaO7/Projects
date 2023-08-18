def tower_of_hanoi(n):
    puzzle = [[],[],[]]
    for i in range(n, 0, -1):
        puzzle[0].append(i)
    
    print('-----Start-----')
    print(puzzle)

    input('-----Enter to Solve-----')
    solve(puzzle, n, 0, 2, 1)

def solve(puzzle, t, start, end, aux):
    if t == 1:
        puzzle[end].append(puzzle[start].pop())
        print('Move:', start, end)
        print(puzzle)
    else:
        solve(puzzle, t-1, start, aux, end)
        puzzle[end].append(puzzle[start].pop())
        print('Move:', start, end)
        print(puzzle)
        solve(puzzle, t-1, aux, end, start)

tower_of_hanoi(int(input('Enter a number')))