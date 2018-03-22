# coding=utf-8
import os
import json

from bearlibterminal import terminal as blt

import pdb

CONSOLE_SIZE = {'x': 80, 'y': 25}
MAP_CONSOLE = {'x': 2, 'y': 2, 'w': 57, 'h': 20}
TILES = {'wall': '#', 'floor': '.', 'door': '+'}

class Tile(object):
    def __init__(self, char='.'):
        self.char = char

class Map(object):
    def __init__(self, w=20, h=20, name=None):
        self.name = name
        self.w = w
        self.h = h
        self.map_tiles = [[Tile() for y in range(h)] for x in range(w)]

    def get_tile(self, x, y):
        if x < len(self.map_tiles) and y < len(self.map_tiles[0]):
            return self.map_tiles[x][y]

    def get_map_as_ascii(self):
        return [[t.char for t in row] for row in self.map_tiles]

    def export(self, filename='map'):
        with open (filename + '.json', 'w') as o_f:
            json.dump([self.name, self.w, self.h, self.get_map_as_ascii()], o_f)
        
class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __contains__(self, pos):
        x,y = pos
        return self.x <= x <= self.x + self.width and \
               self.y <= y <= s+elf.y + self.height

    def fill(self, c = 0x2588):
        for i in range(self.x, self.x + self.width + 1):
            for j in range(self.y, self.y + self.height + 1):
                blt.put(i, j, c)

def test_mouse():
    blt.set("window.title='Omni: mouse input'")
    blt.set("input.filter={keyboard, mouse+}")
    blt.composition(True)

    game_map = Map(20, 10)

    precise_mouse = False
    cursor_visible = True
    mlx = -1; mly = -1
    mrx = -1; mry = -1
    scroll = 0
    plate = False

    character = 'wall'

    menu_open = None

    # Flush input
    while blt.has_input():
        blt.read()

    proceed = True

    # Every tick (can repeat)
    while proceed:
        
        blt.clear()

        render(game_map, menu_open)

        blt.color("white")

        if blt.state(blt.TK_MOUSE_LEFT) and is_in_map_console() and not menu_open:
            x = blt.state(blt.TK_MOUSE_X)-2
            y = blt.state(blt.TK_MOUSE_Y)-2
            if x >= 0 and x < game_map.w and y >= 0 and y < game_map.h:
                game_map.get_tile(x,y).char = TILES[character]

        blt.put(blt.state(blt.TK_MOUSE_X), blt.state(blt.TK_MOUSE_Y), 0x2588)

        blt.refresh()

        # Only once (no repeat)
        while True:
            code = blt.read()

            if code in (blt.TK_ESCAPE, blt.TK_CLOSE):
                proceed = False

            elif code == blt.TK_MOUSE_LEFT:
                x = blt.state(blt.TK_MOUSE_X)
                y = blt.state(blt.TK_MOUSE_Y)

                if x > 60 and 4 <= y <= 4 + len(TILES.keys()):
                    character = list(TILES.keys())[y-4]

                if y == 0 and 2 <= x <= 6:
                    game_map.export()

                if y == 0 and 14 <= x <= 20:
                    menu_open = 'Font'
                
                

            elif code == blt.TK_MOUSE_RIGHT:
                pass

            elif code == blt.TK_MOUSE_SCROLL:
                pass

            elif code == blt.TK_SPACE:
                cursor_visible = not cursor_visible
                blt.set("input.mouse-cursor=%s" % ("true" if cursor_visible else "false"))
    
            if not (proceed and blt.has_input()): break

    blt.color("white")
    blt.composition(False);
    blt.set("input: precise-mouse=false, mouse-cursor=true, filter={keyboard}")


def is_in_map_console():
    if (blt.state(blt.TK_MOUSE_X) > MAP_CONSOLE['x'] - 1 and
        blt.state(blt.TK_MOUSE_X) < MAP_CONSOLE['x'] + MAP_CONSOLE['w'] and
        blt.state(blt.TK_MOUSE_Y) > MAP_CONSOLE['y'] - 1 and
        blt.state(blt.TK_MOUSE_Y) < MAP_CONSOLE['y'] + MAP_CONSOLE['h']):

        return True


def render(game_map, menu_open):
    blt.color("orange")
    # first render the top bar
    blt.puts(2, 0, "Save")
    blt.puts(8, 0, "Load")
    blt.puts(14, 0, "Font")
    blt.puts(20, 0, "Exit")

    blt.puts(61, 0, "ASCII Editor")

    # Then the top and bottom delimitator
    for x in range(80):
        blt.puts(x, 1, "═")
        blt.puts(x, CONSOLE_SIZE['y']-2, "═")
    # Then the left and right delimitator
    for y in range(25):
        blt.puts(1, y, "║")
        blt.puts(60, y, "║")
    # Then the left scrolling bar
    for y in range(MAP_CONSOLE['y'], MAP_CONSOLE['y'] + MAP_CONSOLE['h']):
        blt.puts(0, y, "░")

    # For now, it's a placeholder
    blt.puts(0, 2, "▓")

    # Then the bottom scrolling bar
    for x in range(MAP_CONSOLE['x'], MAP_CONSOLE['x'] + MAP_CONSOLE['w']):
        blt.puts(x, CONSOLE_SIZE['y']-1, "░")

    # For now, it's a placeholder
    blt.puts(2, CONSOLE_SIZE['y']-1, "▓")

    blt.color("white")

    # Right panel display

    # Cursor position
    x = blt.state(blt.TK_MOUSE_X)-2
    if x > MAP_CONSOLE['w'] - 1:
        x = MAP_CONSOLE['w']

    if x < 0:
        x = 0
    
    y = blt.state(blt.TK_MOUSE_Y)-2
    if y > MAP_CONSOLE['h'] - 1:
        y = MAP_CONSOLE['h']

    if y < 0:
        y = 0

    blt.puts(61, 2, f"Cursor: [color=orange]{x}:{y}[/color]")

    blt.puts(61, 3, f"Map size: [color=orange]{game_map.w}x{game_map.h}[/color]")

    for y,(key, val) in enumerate(TILES.items()):
        blt.put(61, y+4, 0x25CB)
        blt.puts(63, y+4, f"{key}")

    for x in range(game_map.w):
        for y in  range(game_map.h):
            blt.puts(x+2, y+2, game_map.get_tile(x, y).char)

    if menu_open:
        if menu_open == 'Font':
            
            fonts_names = os.listdir('fonts/')
            total_h = len(fonts_names)
            max_w = -1

            # Once to clear the area (lel)
            for y,font in enumerate(os.listdir('fonts/')):
                
                name = ' '.join(font.split('_')[:-1])
                size_x = font.split('_')[-1].split('x')[0]
                size_y = font.split('_')[-1].split('x')[1][:-4]

                if max_w < len(name + ' (' + size_x + 'x' + size_y + ')'):
                    max_w = len(name + ' (' + size_x + 'x' + size_y + ')')

            blt.clear_area(13, 1, max_w + 2, total_h)

            for y,font in enumerate(os.listdir('fonts/')):
                
                name = ' '.join(font.split('_')[:-1])
                size_x = font.split('_')[-1].split('x')[0]
                size_y = font.split('_')[-1].split('x')[1][:-4]
                blt.puts(14, y+1, f'{name} ({size_x}x{size_y})')

            blt.color("orange")
            
            for y in range(2, 2 + total_h - 1):
                #TODO: add a thing character
                blt.puts(13, y, "║")
                blt.puts(13 + max_w + 1, y, "║")

            for x in range(14, 14 + max_w):
                blt.puts(x, total_h + 1, "═")

            blt.puts(13, 1, "╗")
            blt.puts(14 + max_w, 1, "╔")
            blt.puts(13, total_h + 1, "╚")
            blt.puts(14 + max_w, total_h + 1, "╝")


if __name__ == "__main__":
    blt.open()
    blt.set(f"window: size={CONSOLE_SIZE['x']}x{CONSOLE_SIZE['y']}, cellsize=auto, title='Omni: menu'; font: default")
    blt.color("white")
    blt.refresh()
    test_mouse()
    blt.close()