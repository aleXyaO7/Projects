from tkinter import *

root = Tk()
root.config(bg = '#345')
canvas = Canvas(root, height=600, width = 1000, bg = 'black')
canvas.pack(expand=True)

img = PhotoImage(file="Map.png")
canvas.create_image(500, 250, image = img)

root.mainloop()