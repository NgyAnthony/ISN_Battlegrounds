from math import cos, sin, sqrt, radians  # imports used to create hexagons
import tkinter as tk

hexagons = [[]]  # This is a list of list of the boards of each canvas_instance that is created
base_hexagon = 0  # targets current list used for the base
new_hexagon = 1  # targets to the empty list to be appended
squad_list = []  # this list contains all the instances of the Squad class

class App:
    def __init__(self, canvas_instance=None):
        """
        This function creates a new canvas_instance which is used everytime Game is called.
        """
        self.canvas_instance = canvas_instance


class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Battlegrounds")
        self.canvas_instance = tk.Canvas(self.master, width=1280, height=800, bg="#a1e2a1")
        self.canvas_instance.pack()
        self.app_instance = App(self.canvas_instance)
        self.initGrid(35, 18, 25, debug=False)  # Calls init grid with cols, rows and size.

        self.previous_clicked = []
        self.neighbours = []  # this list includes all the tags of the neighbours of the selected position
        self.enemy_neighbour = []
        self.enemy_neighbour_inrange = []
        self.friendly_neighbour = []
        self.obstacles = []

        # This if statement hides the previous instance.
        if base_hexagon == 0:
            hexagons[0][0].parent.pack_forget()  # exception : hide "0" at the beginning
        elif base_hexagon > 0:
            hexagons[base_hexagon - 1][0].parent.pack_forget()

        self.canvas_instance.bind("<Button-1>", self.click)  # bind click function when RMB is used

    def initGrid(self, cols, rows, size, debug):
        """
                This function creates the grid of hexagon which will be used as the board.
        :param cols: number of columns used on the board
        :param rows: number of rows used on the board
        :param size: size of one side of hexagon
        :param debug: True/False, make text appear on hexagons
        :return: game board is returned
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
                Hexagon detection on mouse click.
                Movements and attack detection.
        :param evt: get the x and y position of the click
        :return: determine if we need to find the neighbours or if hex is empty
        """
        x, y = evt.x, evt.y  # get the x and y position of RMB event
        for i in hexagons[base_hexagon]:  # this for loop erase any trace of its use
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own
        clicked = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        self.previous_clicked.append(clicked)
        hexagons[base_hexagon][int(clicked) - 1].selected = True

        for i in hexagons[base_hexagon]:
            if i.selected:
                previous_squad = hexagons[base_hexagon][self.previous_clicked[len(self.previous_clicked) - 2] - 1].tags

                # This loop moves the hexagon
                if i.tags in self.neighbours:
                    for x in range(len(hexagons[base_hexagon - 1])):  #
                        if hexagons[base_hexagon][x].tags == i.tags:
                            i.color = hexagons[base_hexagon][self.previous_clicked[len(self.previous_clicked) - 2] - 1].color
                            hexagons[base_hexagon][self.previous_clicked[len(self.previous_clicked) - 2] - 1].color = "#a1e2a1"
                            self.reinstance()
                            print("Click:", i.color, "squad moved to", i.tags)

                            # This for loop changes the position in squad_list
                            for r in range(len(squad_list)):
                                if squad_list[r].position == previous_squad:
                                    squad_list[r].position = i.tags
                                    print("Click: squad_list at", previous_squad, "now at", i.tags, ".")

                # This for loop look for enemies if user has attacked.
                for p in range(len(self.enemy_neighbour_inrange)):
                    if i.tags in self.enemy_neighbour_inrange[p].tags:
                        for b in self.enemy_neighbour_inrange:
                            for l in range(len(squad_list)):
                                if squad_list[l].position == previous_squad:
                                    attacker = squad_list[l]
                            self.attack(b, attacker)
                            break

                # If the hexagon is empty or an obstacle
                if i.color == "#a1e2a1" or i.color == "#60ace6" or i.color == "#a1603a":
                    self.canvas_instance.itemconfigure(i.tags, fill="#bdc3c7")  # fill the clicked hex with color
                    print("Click: empty hexagon or obstacle at", i.tags, " selected.")

                # If the hexagon is a Squad
                elif i.color != "#a1e2a1":
                    print("Click:", i.color, "hexagon at", i.tags, "has been selected.")
                    for a in range(len(squad_list)):
                        if i.tags == squad_list[a].position:
                            mp = squad_list[a].mp
                    if mp == 1:  # assigning pixel density to reach neighbours depending on movement points
                        area = 50
                    elif mp == 2:
                        area = 80
                    self.getNear(i.x, i.y, area, i.tags)  # call possible movements

    def attack(self, defencer, attacker):
        for x in range(len(squad_list)):
            if squad_list[x].position == defencer.tags:
                squad_list[x].units -= attacker.ap
                print(squad_list[x].units)
                if squad_list[x].units == 3:
                    defencer.color = "#EE5A24"
                    self.reinstance()
                if squad_list[x].units <= 0:
                    defencer.color = "#a1e2a1"
                    self.reinstance()

    def getNear(self, x, y, area, origin):
        """
                This function determines the neighbours of a Squad.
        :param x: x position of the clicked hexagon
        :param y: y position of the clicked hexagon
        :param area: pixel width used to determine neighbours
        :param origin: clicked hexagon (to remove him from neighbours list)
        :return: colors the area where action is possible

        """

        self.neighbours.clear()
        self.enemy_neighbour.clear()
        self.friendly_neighbour.clear()

        for a in range(630):
            # define x and y define the zone in which movement will be possible
            neighbour_x0 = x - area
            neighbour_x1 = x + area

            neighbour_y0 = y - area
            neighbour_y1 = y + area

            if neighbour_x1 >= hexagons[base_hexagon][a].x >= neighbour_x0 and \
                    neighbour_y1 >= hexagons[base_hexagon][a].y >= neighbour_y0:
                self.neighbours.append(hexagons[base_hexagon][a].tags)

        # This statement removes the original position from the list
        for m in range(len(self.neighbours)):
            if origin == self.neighbours[m]:
                self.neighbours.remove(self.neighbours[m])
                break

        # This statement removes every obstacles from the neighbours
        for m in range(len(self.neighbours) - 1):
            for i in hexagons[base_hexagon]:
                if i.tags == self.neighbours[m] and (i.color == "#60ace6" or i.color == "#a1603a"):
                    self.obstacles.append(self.neighbours[m])

        self.neighbours = list(set(self.neighbours) - set(self.obstacles))

        # This for loops removes enemies and friendlies and append them to another list
        for m in range(len(self.neighbours)):
            for i in hexagons[base_hexagon]:
                if i.tags == self.neighbours[m] and (i.color == "#c0392b" or i.color == "#EE5A24"):
                    self.enemy_neighbour.append(self.neighbours[m])
                if i.tags == self.neighbours[m] and (i.color == "#013dc6" or i.color == "#0652DD"):
                    self.friendly_neighbour.append(self.neighbours[m])

        self.neighbours = list(set(self.neighbours) - set(self.enemy_neighbour))
        self.neighbours = list(set(self.neighbours) - set(self.friendly_neighbour))

        red_side_colors = ["#c0392b", "#EE5A24"]
        blue_side_colors = ["#013dc6", "#0652DD"]

        # This for loop determines if the ennemy is within range
        for p in range(630):
            attackable_x0 = x - 50
            attackable_x1 = x + 50

            attackable_y0 = y - 50
            attackable_y1 = y + 50

            for a in range(len(red_side_colors)):
                if hexagons[base_hexagon][p].color == red_side_colors[a] and \
                        attackable_x1 >= hexagons[base_hexagon][p].x >= attackable_x0 and \
                        attackable_y1 >= hexagons[base_hexagon][p].y >= attackable_y0:
                        self.enemy_neighbour_inrange.append(hexagons[base_hexagon][p])

        # The two following for statements fill the near elements of the clicked hexagons
        for m in range(len(self.neighbours)):
            for i in hexagons[base_hexagon]:  # this for loop erase any trace of its use
                self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own

        for m in range(len(self.neighbours)):
            for i in hexagons[base_hexagon]:
                if i.tags == self.neighbours[m]:
                    self.canvas_instance.itemconfigure(i.tags, fill="#f1c40f")  # fill the clicked hex with color

    def reinstance(self):
        global hexagons, base_hexagon, new_hexagon
        hexagons.append([])  # append a new empty list to be used as new_hexagon at the next instance
        base_hexagon += 1
        new_hexagon += 1
        Game(root)  # create new Game instance


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
            for x in range(len(hexagons[base_hexagon - 1])):
                # this for loop searches the object in hex list and give the color
                if hexagons[base_hexagon - 1][x].tags == self.tags:
                    self.color = hexagons[base_hexagon - 1][x].color
                    break
                else:
                    self.color = "#a1e2a1"  # foolproofing color assignment
        self.draw()

    def draw(self):
        """
        draw() creates the hexagon
        :return: one hexagon is drawn on the board.
        """
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


class Field:
    # Class field changes the color of an object in hexagons
    #
    types = {
        "water": "#60ace6",
        "mountain": "#a1603a"
    }

    def __init__(self, position, kind):
        self.position = position
        self.kind = kind
        self.color = Field.types[self.kind]
        self.placeField()
        self.reinstance()


    def placeField(self):
        for x in range(len(hexagons[base_hexagon])):
            if self.position == hexagons[base_hexagon][x].tags:
                hexagons[base_hexagon][x].color = self.color

    def reinstance(self):
        global hexagons, base_hexagon, new_hexagon
        hexagons.append([])  # append a new empty list to be used as new_hexagon at the next instance
        base_hexagon += 1
        new_hexagon += 1
        Game(root)  # create new Game instance


class Squad:
    def __init__(self, side, units, arsenal, ap, dp, mp, position, color):
        """
                       This class generates a Squad and re-instances the board.
        :param side: The side determines if you're on the blue or red side.
        :param units: Units are the numbers of units. They're basically HP.
        :param arsenal: Arsenal determines if the Squad is made of tanks, rangers...
        :param ap: Attack points.
        :param dp: Defense points.
        :param mp: Movement points.
        :param position: Position on the board. (x.y)
        :param color: Color code.
        """
        self.side = side
        self.units = units
        self.arsenal = arsenal
        self.ap = ap  # attack points
        self.dp = dp  # defense points
        self.mp = mp  # movement points
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
        squad_list.append(self)  # append the instance object to a list
        print("Squad:", self.side, "squad at", self.position, "has been created.")
        Game(root)  # create new Game instance


root = tk.Tk()
Game(root)  # first instance of canvas

squad_1 = Squad("blue", 6, 'infantry', 3, 3, 2, '15.5', "#013dc6")
squad_2 = Squad("red", 6, 'infantry', 3, 3, 2, '15.4', "#c0392b")
squad_3 = Squad("blue", 6, 'infantry', 3, 3, 2, '14.5', "#013dc6")
field_1 = Field('13.10', "mountain")
field_1 = Field('13.11', "mountain")


root.mainloop()
