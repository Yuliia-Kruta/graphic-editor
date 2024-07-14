import os
from tkinter import *
from tkinter import filedialog, colorchooser, font, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageGrab

# Constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 500
BRUSH_SIZE = 5
DEFAULT_COLOR = "black"
DEFAULT_BG_COLOR = "white"
DEFAULT_FIGURE_COLOR = "purple"
WINDOW_TITLE = "Yuliia's Graphics Editor"

# Global variables
brush_size = BRUSH_SIZE
color = DEFAULT_COLOR
bg_color = DEFAULT_BG_COLOR
figure_color = DEFAULT_FIGURE_COLOR
figure = 0
text_input = ""
x = 0
y = 0

# Initialize main window
root = Tk()
root.title(WINDOW_TITLE)
messagebox.showinfo("", "Welcome to the graphics editor!")

def fullscreen():
    root.attributes("-fullscreen", True)

def drawing(event):
    x1, y1 = event.x - brush_size, event.y - brush_size
    x2, y2 = event.x + brush_size, event.y + brush_size
    myCanvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    draw.ellipse([x1, y1, x2, y2], fill=color, width=brush_size, outline=color)

def change_brush(new_size):
    global brush_size
    brush_size = new_size

def change_color(new_color):
    global color
    color = new_color

def eraser(new_size):
    global color, brush_size
    color = DEFAULT_BG_COLOR
    brush_size = new_size

def change_bg():
    global bg_color
    bg_color = colorchooser.askcolor(color=bg_color)[1]
    myCanvas['bg'] = bg_color

def save():
    im2 = ImageGrab.grab(bbox=(root.winfo_rootx(), root.winfo_rooty(),
                               root.winfo_rootx() + root.winfo_width(), root.winfo_rooty() + root.winfo_height()))
    im2.save("Picture.png")

def open_file():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose a file",
                                          filetypes=[("Image Files", "*.jpg *.png")])
    if filename:
        img = Image.open(filename)
        myCanvas.image = ImageTk.PhotoImage(img)
        myCanvas.create_image(0, 0, image=myCanvas.image, anchor='nw')
        root.geometry(f"{img.width()}x{img.height()}")

def get_coords(event):
    global x, y
    x, y = event.x, event.y

def draw_figure(event):
    global figure
    if figure == 1:
        myCanvas.create_rectangle(x, y, event.x, event.y, fill=figure_color, outline=figure_color)
    elif figure == 2:
        myCanvas.create_oval(x, y, event.x, event.y, fill=figure_color, outline=figure_color)
    elif figure == 3:
        myCanvas.create_polygon(x, y, event.x, event.y, event.x, event.y - 2 * (event.y - y), fill=figure_color, outline=figure_color)
    elif figure == 4:
        myCanvas.create_line(x, y, event.x, event.y, fill=figure_color, width=10)
    elif figure == 5:
        myCanvas.create_arc(x, y, event.x, event.y, fill=figure_color, outline=figure_color)
    elif figure == 6:
        text_font = font.Font(family='Helvetica', size=20, weight='bold', slant='italic')
        myCanvas.create_text(x, y, fill=figure_color, font=text_font, text=text_input)

def select_figure(fig_type):
    global figure, figure_color
    figure = fig_type
    figure_color = colorchooser.askcolor(color=figure_color)[1]

def add_text():
    global figure, text_input, figure_color
    figure = 6
    text_input = simpledialog.askstring("Input", "Type a text:")
    figure_color = colorchooser.askcolor(color=figure_color)[1]

def small_screen(event):
    root.attributes("-fullscreen", False)

def check_exit():
    if messagebox.askyesnocancel("Warning", "Would you like to save a file?"):
        save()
    root.quit()

image1 = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), bg_color)
draw = ImageDraw.Draw(image1)

myCanvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=bg_color, scrollregion=(0, 0, 2000, 2000))
myCanvas.pack(fill=BOTH, expand=True)

hbar = Scrollbar(root, orient=HORIZONTAL)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=myCanvas.xview)

vbar = Scrollbar(root, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=myCanvas.yview)

myCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Menu
menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label="Fullscreen mode", command=fullscreen)
file_menu.add_command(label="Clear all", command=lambda: myCanvas.delete("all"))
file_menu.add_command(label="Exit", command=check_exit)

size_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Brush size', menu=size_menu)
for size in [5, 10, 15, 20, 25]:
    size_menu.add_command(label=str(size), command=lambda s=size: change_brush(s))

color_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Brush color', menu=color_menu)
colors = ["black", "blue", "red", "pink", "purple", "green", "yellow"]
for col in colors:
    color_menu.add_command(label=col.capitalize(), command=lambda c=col: change_color(c))

bg_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Background color', menu=bg_menu)
bg_menu.add_command(label='Change color', command=change_bg)

figures_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Shapes', menu=figures_menu)
figures_menu.add_command(label='Rectangle', command=lambda: select_figure(1))
figures_menu.add_command(label='Circle', command=lambda: select_figure(2))
figures_menu.add_command(label='Triangle', command=lambda: select_figure(3))
figures_menu.add_command(label='Line', command=lambda: select_figure(4))
figures_menu.add_command(label='Arc', command=lambda: select_figure(5))

text_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Text', menu=text_menu)
text_menu.add_command(label='Add text', command=add_text)

eraser_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Eraser', menu=eraser_menu)
for size in [5, 10, 15, 20, 25]:
    eraser_menu.add_command(label=str(size), command=lambda s=size: eraser(s))

help_menu = Menu(menu, tearoff=FALSE)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='Help', command=lambda: messagebox.showinfo("Help", "Use: \n Left mouse click for drawing \n Right mouse click for adding shapes \n S for saving"))
help_menu.add_command(label='About', command=lambda: messagebox.showinfo("About", "Made by Kruta Yuliia \n © All rights reserved"))

# Bindings
myCanvas.bind("<B1-Motion>", drawing)
myCanvas.bind("<ButtonRelease-3>", draw_figure)
myCanvas.bind("<Button-3>", get_coords)
root.bind("<s>", lambda event: save())
root.bind("<Escape>", small_screen)

root.mainloop()
