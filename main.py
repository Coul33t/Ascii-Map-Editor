# coding=utf-8

from __future__ import division

from collections import namedtuple
from bearlibterminal import terminal as blt

import pdb

CONSOLE_SIZE = {'x': 80, 'y': 25}
MAP_CONSOLE = {'x': 2, 'y': 2, 'w': 57, 'h': 21}

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

    game_map = Map(10, 10)

    precise_mouse = False
    cursor_visible = True
    mlx = -1; mly = -1
    mrx = -1; mry = -1
    scroll = 0
    plate = False

    # Flush input
    while blt.has_input():
        blt.read()

    counter = 0

    proceed = True
    while proceed:
        blt.clear()

        blt.color("white")
        blt.puts(
            1, 3,
            "Buttons: "
            "[color=%s]left "
            "[color=%s]middle "
            "[color=%s]right "
            "[color=%s]x1 "
            "[color=%s]x2 " % (
                "orange" if blt.state(blt.TK_MOUSE_LEFT) else "dark gray",
                "orange" if blt.state(blt.TK_MOUSE_MIDDLE) else "dark gray",
                "orange" if blt.state(blt.TK_MOUSE_RIGHT) else "dark gray",
                "orange" if blt.state(blt.TK_MOUSE_X1) else "dark gray",
                "orange" if blt.state(blt.TK_MOUSE_X2) else "dark gray"))


        blt.puts(
            1, 5,
            "Wheel: [color=orange]%d[/color] [color=dark gray]delta[/color]"
            ", [color=orange]%d[/color] [color=dark gray]cumulative" % (
                blt.state(blt.TK_MOUSE_WHEEL), scroll))

        blt.puts(double_click_area.x, double_click_area.y - 1, "Double-click here:")
        blt.color("darker orange" if plate else "darker gray")
        double_click_area.fill()

        if blt.state(blt.TK_MOUSE_LEFT) and is_in_map_console():
            x = blt.state(blt.TK_MOUSE_X)-2
            y = blt.state(blt.TK_MOUSE_Y)-2
            if x >= 0 and x < game_map.w and y >= 0 and y < game_map.h:
                if game_map.get_tile(x,y).char == '.':
                    game_map.get_tile(x,y).char = '#'
                elif game_map.get_tile(x,y).char == '#':
                    game_map.get_tile(x,y).char = '.'

        render(game_map)

        mx = blt.state(blt.TK_MOUSE_X)
        my = blt.state(blt.TK_MOUSE_Y)
        blt.color(0x60FFFFFF)
        for x in range(blt.state(blt.TK_WIDTH)): blt.put(x, my, 0x2588)
        for y in range(blt.state(blt.TK_HEIGHT)): blt.put(mx, y, 0x2588)

        blt.color(0x8000FF00)
        blt.put(mlx, mly, 0x2588)

        blt.color(0x80FF00FF)
        blt.put(mrx, mry, 0x2588)

        blt.refresh()

        while True:
            code = blt.read()
            counter += 1

            if code in (blt.TK_ESCAPE, blt.TK_CLOSE):
                proceed = False

            elif code == blt.TK_MOUSE_LEFT:
                x = blt.state(blt.TK_MOUSE_X)
                y = blt.state(blt.TK_MOUSE_Y)

                if x == 1 and (y == 7 or y == 8):
                    if y == 7:
                        precise_mouse = not precise_mouse
                        blt.set("input.precise-mouse=%s" % ("true" if precise_mouse else "false"))
                    else:
                        cursor_visible = not cursor_visible
                        blt.set("input.mouse-cursor=%s" % ("true" if cursor_visible else "false"))
                elif (x,y) in double_click_area:
                    clicks = blt.state(blt.TK_MOUSE_CLICKS)
                    if clicks > 0 and clicks % 2 == 0:
                        plate = not plate
                else:
                    mlx = x
                    mly = y

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
    if (blt.state(blt.TK_MOUSE_X) > MAP_CONSOLE['x'] and
        blt.state(blt.TK_MOUSE_X) < MAP_CONSOLE['x'] + MAP_CONSOLE['w'] and
        blt.state(blt.TK_MOUSE_Y) > MAP_CONSOLE['y'] and
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
    # Then the scrolling bar
    for y in range(MAP_CONSOLE['y'], MAP_CONSOLE['y'] + MAP_CONSOLE['h']):
        blt.puts(0, y, "░")

    # For now, it's a placeholder
    blt.puts(0, 2, "▓")

    blt.color("white")
    blt.puts(61, 2, f"Cursor: [color=orange]{blt.state(blt.TK_MOUSE_X)}:{blt.state(blt.TK_MOUSE_Y)}[/color]")

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