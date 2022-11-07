#Dungeon Generator for DnD or similar games, built by Bogaevskiy, in autumn of 2022
import random
from ursina import *

class Block:
    def __init__(self, name, dirs):
        self.name = name
        self.dirs = dirs

    def __repr__(self):
        return self.name

def represent(labyrinth):
    for i in range(len(labyrinth)):
        print(labyrinth[i])

app = Ursina()

#setting elements
elements =[ ['hall4', 'nesw'],
['cros4', 'nesw'],
['cor_v', 'ns'],
['cor_h', 'ew'],
['roomn', 'n'],
['roome', 'e'],
['rooms', 's'],
['roomw', 'w'],
['blank', ''],
['hallh', 'ew'],
['hallv', 'ns'],
['anges', 'es'],
['angsw', 'sw'],
['angwn', 'wn'],
['angne', 'ne'],
['hales', 'es'],
['halsw', 'sw'],
['halwn', 'wn'],
['halne', 'ne'],
['t_wne', 'wne'],
['t_nes', 'nes'],
['t_esw', 'esw'],
['t_swn', 'swn'],
['h_wne', 'wne'],
['h_nes', 'nes'],
['h_esw', 'esw'],
['h_swn', 'swn'] ]

elems = []
tiles = []
for i in elements:
    exec("{} = Block('{}', '{}')".format(i[0], i[0], i[1]))
    exec('elems.append({})'.format(i[0]))

dung_width = 5
dung_height = 5

#buttons procedures
def width_increase():
    global dung_width
    if dung_width < 9:
        dung_width += 1
        width_text = 'Width: ' + str(dung_width * 5 - 10)
        caption_width.text = width_text
def width_decrease():
    global dung_width
    if dung_width > 4:
        dung_width -= 1
        width_text = 'Width: ' + str(dung_width * 5 - 10)
        caption_width.text = width_text
def height_increase():
    global dung_height
    if dung_height < 7:
        dung_height+= 1
        height_text = 'Height: ' + str(dung_height * 5 - 10)
        caption_height.text = height_text
def height_decrease():
    global dung_height
    if dung_height > 4:
        dung_height -= 1
        height_text = 'Height: ' + str(dung_height * 5 - 10)
        caption_height.text = height_text

def build_dungeon():
    global dungeon, dung_width, dung_height

    # creating initial dungeon pattern
    # borders are made with blanks
    border_line = [blank for i in range(dung_width)]
    dungeon = [None] * dung_height
    for i in range(dung_height):
        dungeon[i] = [None] * dung_width
    for i in range(dung_height):
        for j in range(dung_width):
            right_limit = dung_width - 1
            if j == 0 or j == right_limit:
                dungeon[i][j] = blank
    dungeon[0] = border_line
    dungeon[-1] = border_line

    #cleaning shown tiles, if there are any
    if len(tiles) > 0:
        for i in tiles:
            i.enabled = False
    #building the dungeon
    for i in range(1, dung_height - 1):
        for j in range(1, dung_width - 1):
            #analysing neighbours
            needed_dirs = []
            if dungeon[i-1][j] != None:
                if 's' in dungeon[i-1][j].dirs:
                    needed_dirs.append('n')
            else:
                if random.randint(0, 2):
                    needed_dirs.append('n')
            if dungeon[i+1][j] != None:
                if 'n' in dungeon[i+1][j].dirs:
                    needed_dirs.append('s')
            else:
                if random.randint(0, 2):
                    needed_dirs.append('s')
            if dungeon[i][j-1] != None:
                if 'e' in dungeon[i][j-1].dirs:
                    needed_dirs.append('w')
            else:
                if random.randint(0, 2):
                    needed_dirs.append('w')
            if dungeon[i][j+1] != None:
                if 'w' in dungeon[i][j+1].dirs:
                    needed_dirs.append('e')
            else:
                if random.randint(0, 2):
                    needed_dirs.append('e')
            #finding and placing suitable block
            good_blocks = []
            for elem in elems:
                if set(needed_dirs) == set(elem.dirs):
                    good_blocks.append(elem)
            dungeon[i][j] = random.choice(good_blocks)

    #showing dungeon with Ursina, inner core without 'blank' borders
    shift_x = dung_width / 2 - 1.1
    shift_y = (dung_height - 1) / 2
    for i in range(1, dung_height -1):
        for j in range(1, dung_width -1):
            tile = Entity()
            tile.model = 'quad'
            tile.position = (j - shift_x, -i + shift_y, -7.5)
            tile.texture = 'Textures/' + dungeon[i][j].name
            tiles.append(tile)

#buttons and text
width_text = 'Width: ' + str(dung_width * 5 - 10)
height_text = 'Height: ' + str(dung_height * 5 -10)

caption_width = Text(text=width_text, x = -0.77, y = 0.25)
caption_height = Text(text=height_text, x = -0.77, y = 0.1)

width_plus = Button(text = "+5", scale = 0.05, scale_x = 0.05, x = -0.67, y = 0.19)
width_plus.on_click = width_increase
width_minus = Button(text = "-5", scale = 0.05, scale_x = 0.05,  x = -0.75, y = 0.19)
width_minus.on_click = width_decrease
height_plus = Button(text = "+5", scale = 0.05, scale_x = 0.05, x = -0.67, y = 0.04)
height_plus.on_click = height_increase
height_minus = Button(text = "-5", scale = 0.05, scale_x = 0.05, x = -0.75, y = 0.04)
height_minus.on_click = height_decrease
launch_button = Button(text = "Generate", scale = 0.05, scale_x = 0.2, x = -0.71, y = -0.2)
launch_button.on_click = build_dungeon

size_text = '''Minimal width is 10

Maximum width is 35

Minimal height is 10

Maximum height is 25'''

caption_size = Text(text = size_text, scale = 0.75, x = -0.80, y = -0.02)

window.exit_button.visible = False
window.borderless = False
app.run()
