# coding=utf-8

from __future__ import division

from collections import namedtuple
from bearlibterminal import terminal as blt

import pdb

CONSOLE_SIZE = {'x': 80, 'y': 25}
MAP_CONSOLE = {'x': 2, 'y': 2, 'w': 57, 'h': 21}
TILES = {'wall': '#', 'floor': '.', 'door': '+'}

class Tile(object):
    def __init__(self, char='.'):
        self.char = char

class Map(object):
    def __init__(self, w=20, h=20):
        self.w = w
        self.h = h
        self.map_tiles = [[Tile() for y in range(h)] for x in range(w)]

    def get_tile(self, x, y):
        if x < len(self.map_tiles) and y < len(self.map_tiles[0]):
            return self.map_tiles[x][y]
        


class Rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __contains__(self, pos):
        x,y = pos
        return self.x <= x <= self.x + self.width and \
               self.y <= y <= self.y + self.height

    def fill(self, c = 0x2588):
        for i in range(self.x, self.x + self.width + 1):
            for j in range(self.y, self.y + self.height + 1):
                blt.put(i, j, c)


double_click_area = Rect(1, 11, 17, 4)

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

    # Flush input
    while blt.has_input():
        blt.read()

    proceed = True

    while proceed:

        blt.clear()

        render(game_map)

        blt.color("white")

        if blt.state(blt.TK_MOUSE_LEFT) and is_in_map_console():
            x = blt.state(blt.TK_MOUSE_X)-2
            y = blt.state(blt.TK_MOUSE_Y)-2
            if x >= 0 and x < game_map.w and y >= 0 and y < game_map.h:
                game_map.get_tile(x,y).char = TILES[character]

        blt.put(blt.state(blt.TK_MOUSE_X), blt.state(blt.TK_MOUSE_Y), 0x2588)

        blt.refresh()

        while True:
            code = blt.read()

            if code in (blt.TK_ESCAPE, blt.TK_CLOSE):
                proceed = False

            elif code == blt.TK_MOUSE_LEFT:
                x = blt.state(blt.TK_MOUSE_X)
                y = blt.state(blt.TK_MOUSE_Y)

                if x > 60 and 3 <= y <= 3 + len(TILES.keys()):
                    character = list(TILES.keys())[y-3]
                
                

            elif code == blt.TK_MOUSE_RIGHT:
                mrx = blt.state(blt.TK_MOUSE_X)
                mry = blt.state(blt.TK_MOUSE_Y)

            elif code == blt.TK_MOUSE_SCROLL:
                scroll += blt.state(blt.TK_MOUSE_WHEEL)

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


def render(game_map):
    blt.color("orange")
    # first render the top bar
    blt.puts(2, 0, "Save")
    blt.puts(8, 0, "Load")
    blt.puts(14, 0, "Exit")

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
    blt.puts(61, 2, f"Cursor: [color=orange]{blt.state(blt.TK_MOUSE_X)-2}:{blt.state(blt.TK_MOUSE_Y)-2}[/color]")

    for y,(key, val) in enumerate(TILES.items()):
        blt.put(61, y+3, 0x25CB)
        blt.puts(63, y+3, f"{key}")

    for x in range(game_map.w):
        for y in  range(game_map.h):
            blt.puts(x+2, y+2, game_map.get_tile(x, y).char)

if __name__ == "__main__":
    blt.open()
    blt.set(f"window: size={CONSOLE_SIZE['x']}x{CONSOLE_SIZE['y']}, cellsize=auto, title='Omni: menu'; font: default")
    blt.color("white")
    blt.refresh()
    test_mouse()
    blt.close()