#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from math import cos, sin, sqrt, radians


# Solution : assign each coordinate to the hexagon with the identification number

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Hexagon Grid")  # Titre
        self.can = Canvas(self, width=1280, height=800, bg="#a1e2a1")  # Dimensions
        self.can.pack()

        self.hexagons = []  # TODO : Take this list and assign each object created to a list with a [x,y] position, make it with the loop to add an option called "position" which inclueds "x and y"
        self.initGrid(35, 18, 25, debug=False)  # Longueur/Largeur/Longeur d'hexagone

        self.can.bind("<Button-1>", self.click)  # Détection de clic

    def initGrid(self, cols, rows, size, debug):
        """
        2d grid of hexagons
        """
        for c in range(cols):  # Détermine le décalage: évite la superposition des hexagones
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                h = FillHexagon(self.can,
                                c * (size * 1.5),  # Position "x"
                                (r * (size * sqrt(3))) + offset,  # Position "y"
                                size,  # Taille de base
                                "#a1e2a1",  # Couleur de base de l'hexagone
                                "{}.{}".format(r, c))  # Debug : texte de position
                self.hexagons.append(h)

                if debug:
                    coords = "{}, {}".format(r, c)
                    self.can.create_text(c * (size * 1.5) + (size / 2),
                                         (r * (size * sqrt(3))) + offset + (size / 2),
                                         text=coords, anchor="n", state="disabled")  # state disabled not working
    def click(self, evt):
        """
        hexagon detection on mouse click
        """
        x, y = evt.x, evt.y
        for i in self.hexagons:
            i.selected = False
            self.can.itemconfigure(i.tags, fill=i.color)  # Make all hexagons the color of the object
            self.colorize()
        clicked = self.can.find_closest(x, y)[0]  # find closest
        print("Number :", int(clicked) - 1)
        self.hexagons[int(clicked) - 1].selected = True  # Make the closest object selected
        for i in self.hexagons:  # re-configure selected only
            if i.selected:
                self.can.itemconfigure(i.tags, fill="#4286f4")  # Fill the object with color
                print(i.color)
        print(len(self.hexagons))
        self.colorize()
        #WHAT I could do : create a class with variables that changes and a "refresh" method that basically makes a item.configure of the board

    def colorize(self):
        self.can.itemconfigure(self.hexagons[301].tags, fill="#a1603a")
        self.can.itemconfigure(self.hexagons[300].tags, fill="#a1603a")
        self.can.itemconfigure(self.hexagons[299].tags, fill="#a1603a")
        print(self.hexagons[15].tags)
        # take the position of the hexagone to colorize and its assigned color

# ------------------------------------------------------------------------------
class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        """Définition des paramètres d'un hexagone de base"""
        self.parent = parent  # Canvas
        self.x = x  # axe x (haut gauche)
        self.y = y  # axe y (haut gauche)
        self.length = length  # longueur d'un côté d'hexagone
        self.color = color  # couleur

        self.selected = False  # Case non sélectionnée
        self.tags = tags  # Tags pour apparition des coordonnées

        self.draw()  # Appel de la fonction draw

    def draw(self):
        """draw() trace l'hexagone."""
        start_x = self.x  # Nombre de colonnes
        start_y = self.y  # Nombre de lignes
        angle = 60  # Angle d'un hexagone
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            # Définition des points x,y de l'hexagone
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        # Traçage de l'hexagone avec la fonction create_polygon
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


# ---------------------------------------------------------
class Field:
    types = {
        "grass": "#a1e2a1",
        "water": "#60ace6",
        "mountain": "#a1603a"
    }

    def __init__(self, parent, x, y, kind, size, tags):
        self.parent = parent
        self.x = x
        self.y = y
        self.kind = kind
        self.color = Field.types[self.kind]
        self.selected = False
        self.size = size
        self.tags = tags
        self.draw()

    def draw(self):
        FillHexagon(self.parent, self.x, self.y, self.size, self.color, self.tags)

# ----------------------------------------------------------
if __name__ == '__main__':
    app = App()
    app.mainloop()
#{'parent': <tkinter.Canvas object .!canvas>, 'x': 75.0, 'y': 627.8684177437179, 'length': 25, 'color': '#a1e2a1', 'selected': False, 'tags': '14.2'}
