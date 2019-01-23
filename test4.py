from tkinter import *
from math import cos, sin, sqrt, radians
import tkinter as tk

hexagons = [[]]  # This is a list of list of the boards of each instance that is created
base_hexagon = 0
new_hexagon = 1

class App:
    def __init__(self, canvas_instance=None):
        self.canvas_instance = canvas_instance

class Game:
    def __init__(self, master):
        self.master = master
        self.canvas_instance = tk.Canvas(self.master, width=1280, height=800, bg="#a1e2a1")
        self.canvas_instance.pack()
        self.app_instance = App(self.canvas_instance)
        self.initGrid(35, 18, 25, debug=False)

    # a1e2a1
    def initGrid(self, cols, rows, size, debug):
        """
        2d grid of hexagons
        """
        if base_hexagon == 0:
            color = "#a1e2a1"
        else:
            color = "#b71717"
            # This is just a test, the board is supposed to be red when you run the program but it's green.
            # The new instance which use the new color is supposed to make the canvas appear red.

        #for x in range(len(hexagons[base_hexagon])):
        #    if hexagons[base_hexagon][x].tags == "%s.%s" %(c, r):
        #       color = hexagons[base_hexagon][x].color
        # the actual code I want to implement
        if new_hexagon >= 2:
            for x in range(len(hexagons[0])):
                self.canvas_instance.tag_raise(hexagons[base_hexagon-1][x].tags)

        for c in range(cols):
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                h = FillHexagon(self.canvas_instance,
                                c * (size * 1.5),
                                (r * (size * sqrt(3))) + offset,
                                size,
                                color, # The color here must be changed
                                "{}.{}".format(r, c))
                if base_hexagon == 0:
                    hexagons[0].append(h)
                elif base_hexagon > 0:
                    hexagons[new_hexagon - 1].append(h)

                if debug:
                    coords = "{}, {}".format(r, c)
                    self.canvas_instance.create_text(c * (size * 1.5) + (size / 2),
                                         (r * (size * sqrt(3))) + offset + (size / 2),
                                         text=coords, anchor="n", state="disabled")  # state disabled not working

class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        """Définition des paramètres d'un hexagone de base"""
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.color = color

        self.selected = False
        self.tags = tags

        self.draw()

    def draw(self):
        """draw() trace l'hexagone."""
        start_x = self.x
        start_y = self.y
        angle = 60
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        self.parent.create_polygon(coords[0][0],
                                   coords[0][1],
                                   coords[1][0],
                                   coords[1][1],
                                   coords[2][0],
                                   coords[2][1],
                                   coords[3][0],
                                   coords[3][1],
                                   coords[4][0],
                                   coords[4][1],
                                   coords[5][0],
                                   coords[5][1],
                                   fill=self.color,
                                   outline="grey",
                                   tags=self.tags)

class Squad:
    def __init__(self, side, units, arsenal, ap, dp, position, color):
        self.side = side
        self.units = units
        self.arsenal = arsenal
        self.ap = ap
        self.dp = dp
        self.position = position
        self.color = color
        Game(root)

        self.squadAppear()

    def squadAppear(self):
        global hexagons, base_hexagon, new_hexagon
        for x in range(len(hexagons[base_hexagon])):
            if hexagons[base_hexagon][x].tags == self.position:
                hexagons[base_hexagon][x].color = self.color
                print(hexagons[0][5].color)
                break
        hexagons.append([])
        base_hexagon += 1
        new_hexagon += 1
        Game(root)
        print(hexagons[1][5].color)

        # Call Game(root) and replace the color of self.position

root = tk.Tk()
squad_1 = Squad("blue", 6, 'infantry', 3, 3, '5.0', "#013dc6")
root.mainloop()

# print(hexagons)
# print(hexagons[5].tags)
# print(len(hexagons))
# print(hexagons[x].color)
