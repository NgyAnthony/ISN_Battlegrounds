from math import cos, sin, sqrt, radians  # imports used to create hexagons
import tkinter as tk

hexagons = [[]]  # This is a list of list of the boards of each canvas_instance that is created
base_hexagon = 0  # targets current list used for the base
new_hexagon = 1  # targets to the empty list to be appended

class App:
    """
    This function creates a new canvas_instance which is used everytime Game is called.
    """
    def __init__(self, canvas_instance=None):
        self.canvas_instance = canvas_instance

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Battlegrounds")
        self.canvas_instance = tk.Canvas(self.master, width=1280, height=800, bg="#a1e2a1")
        self.canvas_instance.pack()
        self.app_instance = App(self.canvas_instance)
        self.initGrid(35, 18, 25, debug=True)  # Calls init grid with cols, rows and size.

        # This if statement hides the previous instance.
        if base_hexagon == 0:
            hexagons[0][0].parent.pack_forget()  # exception : hide "0" at the beginning
        elif base_hexagon > 0:
            hexagons[base_hexagon - 1][0].parent.pack_forget()

        self.canvas_instance.bind("<Button-1>", self.click)  # bind click function when RMB is used

    def initGrid(self, cols, rows, size, debug):
        """
        This function creates the grid of hexagon which will be used as the board.
        """
        color = "#a1e2a1"  # default color
        for c in range(cols):  # avoid overlapping hexagons
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                h = FillHexagon(self.canvas_instance,
                                c * (size * 1.5),
                                (r * (size * sqrt(3))) + offset,
                                size,
                                color,
                                "{}.{}".format(c, r))  # Call FillHexagon to generate the hexagon
                if base_hexagon == 0:  # exception : initial instancing
                    hexagons[0].append(h)
                elif base_hexagon > 0:  # append to the new_hexagon list
                    hexagons[new_hexagon - 1].append(h)

                # This if statement writes position on every hexagon
                    # Warning : click doesn't work when debug is on
                if debug:
                    coords = "{}, {}".format(c, r)
                    self.canvas_instance.create_text(c * (size * 1.5) + (size / 2),
                                         (r * (size * sqrt(3))) + offset + (size / 2),
                                         text=coords, anchor="n", state="disabled")

    def click(self, evt):
        """
        Hexagon detection on mouse click
        """
        x, y = evt.x, evt.y  # get the x and y position of RMB event
        for i in hexagons[base_hexagon]:  # this for loop erase any trace of its use
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own
        clicked = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        hexagons[base_hexagon][int(clicked) - 1].selected = True
        for i in hexagons[base_hexagon]:
            if i.selected:
                self.canvas_instance.itemconfigure(i.tags, fill="#bdc3c7")  # fill the clicked hex with color
                print(i.__dict__)



class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        """ Define parameters of the hexagon """
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.tags = tags
        self.selected = False
        if base_hexagon == 0:  # the first instance leaves the default color
            self.color = color
        else:
            for x in range(630):
                # this for loop searches the object in hex list and give the color
                if hexagons[base_hexagon - 1][x].tags == self.tags:
                    self.color = hexagons[base_hexagon - 1][x].color
                    break
                else:
                    self.color = "#a1e2a1"  # foolproofing color assignment
        self.draw()

    def draw(self):
        """draw() creates the hexagon"""
        start_x = self.x
        start_y = self.y
        angle = 60  # angle of hexagon
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        # create_polygon creates a polygon based on coords
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
    """
    This class generates a Squad and re-instances the board.
    """
    def __init__(self, side, units, arsenal, ap, dp, position, color):
        self.side = side
        self.units = units
        self.arsenal = arsenal
        self.ap = ap
        self.dp = dp
        self.position = position
        self.color = color
        self.squadAppear()

    def squadAppear(self):
        global hexagons, base_hexagon, new_hexagon
        # get the global variables needed to create the board and modify it
        for x in range(len(hexagons[base_hexagon])):
            # this for loop targets the position of the instance with the current position in the form of tags
            # and change the color of the targeted hexagon
            if hexagons[base_hexagon][x].tags == self.position:
                hexagons[base_hexagon][x].color = self.color
                break
        hexagons.append([])  # append a new empty list to be used as new_hexagon at the next instance
        base_hexagon += 1
        new_hexagon += 1
        Game(root)  # create new Game instance


root = tk.Tk()
Game(root)  # first instance of canvas

squad_1 = Squad("blue", 6, 'infantry', 3, 3, '15.5', "#013dc6")
squad_2 = Squad("blue", 6, 'infantry', 3, 3, '10.5', "#013dc6")
squad_3 = Squad("blue", 6, 'infantry', 3, 3, '5.5', "#013dc6")

root.mainloop()
