# coding=utf-8
import os
import json

from bearlibterminal import terminal as blt

import pdb

CONSOLE_SIZE = {'x': 80, 'y': 25}
MAP_CONSOLE = {'x': 2, 'y': 2, 'w': 57, 'h': 20}
TILES = {}

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

    def fill(self, c='green'):
        for i in range(self.x, self.x + self.width + 1):
            for j in range(self.y, self.y + self.height + 1):
                blt.puts(i, j, f"[color={c}]░[/color]")

def test_mouse():
    blt.composition(True)

    game_map = Map(20, 10)

    precise_mouse = False
    cursor_visible = True
    mlx = -1; mly = -1
    mrx = -1; mry = -1
    scroll = 0
    plate = False

    character = next(iter(TILES))

    menu_open = None

    tile_clicked = 0

    # Flush input
    while blt.has_input():
        blt.read()

    proceed = True

    # Every tick (can repeat)
    while proceed:

        blt.clear()

        render(game_map, menu_open, tile_clicked)

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
                    character = list(TILES.keys())[y-5]
                    tile_clicked = y-5

                if y == 0 and 2 <= x <= 6:
                    game_map.export()

                if y == 0 and 14 <= x <= 17:
                    menu_open = 'Font'

                if y == 0 and 20 <= x <= 23:
                    return



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


def render(game_map, menu_open, tile_clicked):
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
    blt.puts(61, 3, f"True cursor: [color=orange]{blt.state(blt.TK_MOUSE_X)}:{blt.state(blt.TK_MOUSE_Y)}[/color]")
    blt.puts(61, 4, f"Map size: [color=orange]{game_map.w}x{game_map.h}[/color]")

    for y,(key, val) in enumerate(TILES.items()):
        if y == tile_clicked:
            area_to_fill = Rect(MAP_CONSOLE['x'] + MAP_CONSOLE['w'] + 2, y+5, CONSOLE_SIZE['x'] - MAP_CONSOLE['x'] - MAP_CONSOLE['w'], 0)
            area_to_fill.fill('dark orange')
            blt.puts(61, y+5, f"[color=orange]{chr(0x25CB)}[/color]")
        else:
            blt.put(61, y+5, 0x25CB)
        blt.puts(63, y+5, f"{key}")

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

def load_ressources(path):
    with open(path, 'r') as tile_name:
        lines = [line.rstrip('\n').split(' ') for line in tile_name]
        for line in lines:
            TILES[line[0]] = line[1]

def selection_menu():
    selected = False

    line_to_bg = -1

    tilesets = os.listdir('tilesets/')
    nb_of_tilesets = len(tilesets)

    tilesets_comp = []
    for ts in tilesets:
        first_ascii = []
        with open('tilesets/'+ts, 'r') as ts_o:
            names = [line.rstrip('\n').split(' ')[0] for line in ts_o]
        tilesets_comp.append([ts, '/'.join(names[0:3])])

    while not selected:
        blt.clear()

        blt.color("orange")
        blt.puts(3, 4, "[[Load a tileset]]")

        for x in range(5 + len("Load a tileset"), CONSOLE_SIZE['x'] - 3):
            blt.puts(x, 4, "═")

        for x in range(3, CONSOLE_SIZE['x'] - 3):
            blt.puts(x, CONSOLE_SIZE['y'] - 1, "═")

        for y in range(5, CONSOLE_SIZE['y'] - 1):
            blt.puts(2, y, "║")
            blt.puts(CONSOLE_SIZE['x'] - 3, y, "║")

        blt.puts(2, 4, "╔")
        blt.puts(CONSOLE_SIZE['x'] - 3, 4, "╗")
        blt.puts(CONSOLE_SIZE['x'] - 3, CONSOLE_SIZE['y'] - 1, "╝")
        blt.puts(2, CONSOLE_SIZE['y'] - 1, "╚")

        while blt.has_input():
            key = blt.read()

            if key in (blt.TK_ESCAPE, blt.TK_CLOSE):
                return False

            if key == blt.TK_MOUSE_LEFT:
                if (2 < blt.state(blt.TK_MOUSE_X) < CONSOLE_SIZE['x'] - 3) and (5 < blt.state(blt.TK_MOUSE_Y) < 5 + nb_of_tilesets + 1):
                    selected = blt.state(blt.TK_MOUSE_Y) - 5

        if (2 < blt.state(blt.TK_MOUSE_X) < CONSOLE_SIZE['x'] - 3) and (5 < blt.state(blt.TK_MOUSE_Y) < 5 + nb_of_tilesets + 1):
            line_to_bg = blt.state(blt.TK_MOUSE_Y)
            area_to_fill = Rect(4, blt.state(blt.TK_MOUSE_Y), CONSOLE_SIZE['x'] - 8, 0)
            area_to_fill.fill('orange')


        blt.color("white")

        for y,tileset in enumerate(tilesets_comp):
            name = tileset[0][:-4]
            blt.puts(5, y+6, f'{chr(0x25CB)} {name} ({tileset[1]})')

        line_to_bg = -1
        blt.refresh()

    load_ressources(f'tilesets/{tilesets[selected-1]}')
    test_mouse()


if __name__ == "__main__":
    blt.open()
    blt.set(f"window: size={CONSOLE_SIZE['x']}x{CONSOLE_SIZE['y']}, cellsize=auto, title='Omni: menu'; font: default")
    blt.set("window.title='Omni: mouse input'")
    blt.set("input.filter={keyboard, mouse+}")
    blt.color("white")
    blt.refresh()
    selection_menu()
    blt.close()