from tkinter import *
import random

rows = int(input('Rows of graph:'))
cols = int(input('Cols of graph:'))

grid = [[0 for _ in range(cols)] for _ in range(rows)]
button_grid = [[0 for _ in range(cols)] for _ in range(rows)]
letters_boolean = False

def update(r, c):
    nbrs = [(r, c)]
    if r > 0:
        nbrs.append((r-1, c))
    if r < rows - 1:
        nbrs.append((r+1, c))
    if c > 0:
        nbrs.append((r, c-1))
    if c < cols - 1:
        nbrs.append((r, c+1))
    for nr, nc in nbrs:
        grid[nr][nc] = 1 - grid[nr][nc]
        if grid[nr][nc] == 1:
            button_grid[nr][nc].configure(bg='yellow')
        else:
            button_grid[nr][nc].configure(bg='white')

def update_letters():
    global letters_boolean
    letters_boolean = not letters_boolean
    for r in range(len(button_grid)):
        for c in range(len(button_grid[0])):
            if letters_boolean:
                button_grid[r][c].configure(text=str(r * rows + c + 1))
            else:
                button_grid[r][c].configure(text='')

def random_shuffle():
    reset()
    for _ in range(random.randint(1, rows * cols)):
        r, c = random.randint(0, rows-1), random.randint(0, cols-1)
        update(r, c)

def reset():
    global grid, button_grid
    for r in range(rows):
        for c in range(cols):
            b = Button(window, height=5, width=10, bg="white", command=lambda r = r, c = c : update(r, c))
            b.grid(row=r, column=c)
            button_grid[r][c] = b

    letter_button = Button(window, height=2, width=8, bg="white", command=update_letters, text='numbers')
    letter_button.grid(row=rows, column=0)

    reset_button = Button(window, height=2, width=8, bg="white", command=reset, text='reset')
    reset_button.grid(row=rows, column=1)

    random_button = Button(window, height=2, width=8, bg="white", command=random_shuffle, text='random')
    random_button.grid(row=rows, column=2)

window = Tk()

reset()

window.mainloop()
