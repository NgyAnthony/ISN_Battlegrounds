from math import cos, sin, sqrt, radians  # imports used to create hexagons
import tkinter as tk
colorblind = 0  # 0 for normal, 1 for colorblind

hexagons = []  # This is a list of list of the boards of each canvas_instance that is created
squad_list = []  # this list contains all the instances of the Squad class

if colorblind == 0:
    red_side_colors = ["#c0392b", "#EE5A24"]
    blue_side_colors = ["#013dc6", "#0652DD"]
    objective_color = "#8c7ae6"
    grass_color = "#a1e2a1"
    mountain_color = "#a1603a"
    water_color = "#60ace6"
    moving_color = "#f1c40f"

    objective_red = ['27.4']
    objective_blue = ['5.14']

elif colorblind == 1:
    pass

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
        self.master.geometry("1440x800")

        # <---Tkinter --->
        # Frame and canvas
        self.canvas_instance = tk.Canvas(self.master, width=1280, height=800, bg=grass_color, relief="ridge", borderwidth="10")
        self.frame = tk.Frame(self.master, width=130, height=800, bg="blue", padx="5", relief="ridge", borderwidth="10", pady="5")
        self.frame.pack_propagate(0)
        self.frame.pack(side="left")
        self.canvas_instance.pack()

        # Title
        self.title = tk.Text(self.frame, height="1")
        self.title.insert(tk.INSERT, "BATTLEGROUNDS")
        self.title.config(state=tk.DISABLED)
        self.title.pack(pady=(10, 50))

        # Title of turn
        self.current_player = tk.Text(self.frame, height="1")
        self.current_player.insert(tk.INSERT, "Turn of:")
        self.current_player.config(state=tk.DISABLED)
        self.current_player.pack()

        # Images
        self.blue_player_img = tk.PhotoImage(file='images/blue_player.gif')
        self.red_player_img = tk.PhotoImage(file='images/red_player.gif')
        self.water_img = tk.PhotoImage(file='images/water.gif')
        self.mountain_img = tk.PhotoImage(file='images/mountain.gif')
        self.objective_img = tk.PhotoImage(file='images/obj.gif')
        self.grass_img = tk.PhotoImage(file='images/grass.gif')

        # Image of current playing player
        self.show_player = tk.Button(self.frame)
        self.show_player.config(image=self.red_player_img)
        self.show_player.pack()

        # Title of hovering
        self.current = tk.Text(self.frame, height="1")
        self.current.insert(tk.INSERT, "Hovering:")
        self.current.config(state=tk.DISABLED)
        self.current.pack(pady=(50, 0))

        # Name of hovering object
        self.current_player = tk.Button(self.frame)
        self.current_player.config(text="Grass")
        self.current_player.pack(fill="x")

        # Image of hovering hexagon
        self.show_hover = tk.Button(self.frame)
        self.show_hover.config(image=self.grass_img, state=tk.DISABLED)
        self.show_hover.pack()

        # Information and details of hexagon
        self.current_squad = tk.Button(self.frame, height="5")
        self.current_squad.config(text="")
        self.current_squad.pack(fill="x")

        # Quit button
        self.quit = tk.Button(self.frame, text="Quit", bg="red", command=root.destroy)
        self.quit.pack(fill="x", side="bottom")

        # End turn button
        self.end_turn = tk.Button(self.frame, text="End turn", bg="red", command=self.endTurn)
        self.end_turn.pack(fill="x", side="bottom")
        # < --- Tkinter --->

        self.app_instance = App(self.canvas_instance)
        self.initGrid(35, 18, 25, debug=False)  # Calls init grid with cols, rows and size.
        Create()
        self.reset_board()

        self.previous_clicked = []
        self.neighbours = []  # this list includes all the tags of the neighbours of the selected position
        self.enemy_neighbour = []
        self.enemy_neighbour_inrange = []
        self.friendly_neighbour = []
        self.obstacles = []
        self.playing_side = "red"

        self.canvas_instance.bind("<Button-1>", self.click)  # bind click function when RMB is used
        self.canvas_instance.bind("<Motion>", self.moved)

        self.tag = self.canvas_instance.create_text(20, 20, text="", anchor="nw")
        self.hexagon = self.canvas_instance.create_text(20, 35, text="", anchor="nw")

    def moved(self, evt):
        x, y = evt.x, evt.y  # get the x and y position of RMB event
        self.hover = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        self.canvas_instance.itemconfigure(self.tag, text="(%r, %r)" % (evt.x, evt.y))
        self.canvas_instance.itemconfigure(self.hexagon, text="(%r)" % self.hover)

        if hexagons[self.hover - 1].color in blue_side_colors:
            self.show_hover.config(image=self.blue_player_img)
            self.current_player.config(text="Player 1")
            for x in range(len(squad_list)):
                if squad_list[x].position == hexagons[self.hover - 1].tags:
                    self.current_squad.config(text="HP = %s\nMP = %s" % (squad_list[x].units, squad_list[x].mp))

        elif hexagons[self.hover - 1].color in red_side_colors:
            self.show_hover.config(image=self.red_player_img)
            self.current_player.config(text="Player 2")
            for x in range(len(squad_list)):
                if squad_list[x].position == hexagons[self.hover - 1].tags:
                    self.current_squad.config(text="HP = %s\nMP = %s" % (squad_list[x].units, squad_list[x].mp))

        elif hexagons[self.hover - 1].color == water_color:
            self.show_hover.config(image=self.water_img)
            self.current_player.config(text="Water")
            self.current_squad.config(text="Indestructible\nobject.")

        elif hexagons[self.hover - 1].color == mountain_color:
            self.show_hover.config(image=self.mountain_img)
            self.current_player.config(text="Mountain")
            self.current_squad.config(text="Indestructible\nobject.")

        elif hexagons[self.hover - 1].color == objective_color:
            self.show_hover.config(image=self.objective_img)
            self.current_player.config(text="Objective")
            self.current_squad.config(text="Empty\nposition.")

        elif hexagons[self.hover - 1].color == grass_color:
            self.show_hover.config(image=self.grass_img)
            self.current_player.config(text="Grass")
            self.current_squad.config(text="Empty\nposition.")

        self.show_hover.pack()

    def endTurn(self):
        if self.playing_side == "red":
            self.playing_side = "blue"
            self.show_player.config(image=self.blue_player_img)
            self.show_player.pack()

        elif self.playing_side == "blue":
            self.playing_side = "red"
            self.show_player.config(image=self.red_player_img)
            self.show_player.pack()

    def reset_board(self):
        for i in hexagons:
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon to its own

    def initGrid(self, cols, rows, size, debug):
        """
                This function creates the grid of hexagon which will be used as the board.
        :param cols: number of columns used on the board
        :param rows: number of rows used on the board
        :param size: size of one side of hexagon
        :param debug: True/False, make text appear on hexagons
        :return: game board is returned
        """
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
                                grass_color,
                                "{}.{}".format(c, r))  # Call FillHexagon to generate the hexagon
                hexagons.append(h)

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
        for i in hexagons:  # this for loop erase any trace of its use
            i.selected = False  # set every hex object to "not selected"
            self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own
        clicked = self.canvas_instance.find_closest(x, y)[0]  # define "clicked" as the closest object near x,y
        self.previous_clicked.append(clicked)
        previous_squad = hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].tags
        hexagons[int(clicked) - 1].selected = True

        for i in hexagons:
            # <--First click-->
            if i.selected and len(self.previous_clicked) % 2 == 1:
                # If the hexagon is empty or an obstacle
                if i.color == grass_color or i.color == mountain_color or i.color == water_color:
                    self.clear_sight()
                    self.canvas_instance.itemconfigure(i.tags, fill="#bdc3c7")  # fill the clicked hex with color
                    self.previous_clicked.clear()
                    print("Click: empty hexagon or obstacle at", i.tags, " selected.")

                # If the hexagon is on the playing side, allow movement
                if self.playing_side == "red" and i.color in red_side_colors:
                    print("Click:", i.color, "hexagon at", i.tags, "has been selected.")
                    for a in range(len(squad_list)):
                        if i.tags == squad_list[a].position:
                            mp = squad_list[a].mp
                    if mp == 1:  # assigning pixel density to reach neighbours depending on movement points
                        area = 50
                    elif mp == 2:
                        area = 80
                    self.getNear(i.x, i.y, area, i.tags)  # call possible movements

                elif self.playing_side == "blue" and i.color in blue_side_colors:
                    print("Click:", i.color, "hexagon at", i.tags, "has been selected.")
                    for a in range(len(squad_list)):
                        if i.tags == squad_list[a].position:
                            mp = squad_list[a].mp
                    if mp == 1:  # assigning pixel density to reach neighbours depending on movement points
                        area = 50
                    elif mp == 2:
                        area = 80
                    self.getNear(i.x, i.y, area, i.tags)  # call possible movements

                # If it's not the turn of the clicked object, disallow movements
                elif self.playing_side == "red" and i.color in blue_side_colors:
                    self.clear_sight()
                    self.previous_clicked.clear()
                    print("Click: it's not the turn of the selected unit.")

                elif self.playing_side == "blue" and i.color in red_side_colors:
                    self.clear_sight()
                    self.previous_clicked.clear()
                    print("Click: it's not the turn of the selected unit.")

            # <--Second click-->
            elif i.selected and len(self.previous_clicked) % 2 == 0:
                # This loop moves the hexagon
                if i.tags in self.neighbours:
                    for x in range(len(hexagons) - 1):
                        if hexagons[x].tags == i.tags:
                            i.color = hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color
                            hexagons[self.previous_clicked[len(self.previous_clicked) - 2] - 1].color = "#a1e2a1"
                            print("Click:", i.color, "squad moved to", i.tags)

                            # This for loop changes the position in squad_list
                            for r in range(len(squad_list)):
                                if squad_list[r].position == previous_squad:
                                    squad_list[r].position = i.tags
                                    print("Click: squad_list at", previous_squad, "now at", i.tags, ".")

                # This for loop look for hexagons that can be attacked.
                for p in range(len(self.enemy_neighbour_inrange)):
                    if i.tags == self.enemy_neighbour_inrange[p].tags:
                        defencer = self.enemy_neighbour_inrange[p]
                        for l in range(len(squad_list)):
                            if squad_list[l].position == previous_squad:
                                attacker = squad_list[l]
                        self.attack(defencer, attacker)
                        break
                self.reset_board()
                self.checkObjective()

    # This function resets the "targets" of the chosen position
    def clear_sight(self):
        self.neighbours.clear()
        self.enemy_neighbour.clear()
        self.friendly_neighbour.clear()

    def attack(self, defencer, attacker):
        for x in range(len(squad_list)):
            if squad_list[x].position == defencer.tags:
                squad_list[x].units -= attacker.ap
                if self.playing_side == "blue":
                    if squad_list[x].units == 3:
                        defencer.color = "#EE5A24"
                    if squad_list[x].units <= 0:
                        defencer.color = "#a1e2a1"
                elif self.playing_side == "red":
                    if squad_list[x].units == 3:
                        defencer.color = "#0652DD"
                    if squad_list[x].units <= 0:
                        defencer.color = "#a1e2a1"

    def getNear(self, x, y, area, origin):
        """
                This function determines the neighbours of a Squad.
        :param x: x position of the clicked hexagon
        :param y: y position of the clicked hexagon
        :param area: pixel width used to determine neighbours
        :param origin: clicked hexagon (to remove him from neighbours list)
        :return: colors the area where action is possible

        """
        self.clear_sight()

        for a in range(630):
            # define x and y define the zone in which movement will be possible
            neighbour_x0 = x - area
            neighbour_x1 = x + area

            neighbour_y0 = y - area
            neighbour_y1 = y + area

            if neighbour_x1 >= hexagons[a].x >= neighbour_x0 and \
                    neighbour_y1 >= hexagons[a].y >= neighbour_y0:
                self.neighbours.append(hexagons[a].tags)

        # This statement removes the original position from the list
        for m in range(len(self.neighbours)):
            if origin == self.neighbours[m]:
                self.neighbours.remove(self.neighbours[m])
                break

        # This statement removes every obstacles from the neighbours
        for m in range(len(self.neighbours)):
            for i in hexagons:
                if i.tags == self.neighbours[m] and (i.color == "#60ace6" or i.color == "#a1603a"):
                    self.obstacles.append(self.neighbours[m])
        self.neighbours = list(set(self.neighbours) - set(self.obstacles))

        # This for loops removes enemies and friendlies and append them to another list
        for m in range(len(self.neighbours)):
            for i in hexagons:
                if self.playing_side == "blue":
                    if i.tags == self.neighbours[m] and (i.color == "#c0392b" or i.color == "#EE5A24"):
                        self.enemy_neighbour.append(self.neighbours[m])
                    if i.tags == self.neighbours[m] and (i.color == "#013dc6" or i.color == "#0652DD"):
                        self.friendly_neighbour.append(self.neighbours[m])
                elif self.playing_side == "red":
                    if i.tags == self.neighbours[m] and (i.color == "#c0392b" or i.color == "#EE5A24"):
                        self.friendly_neighbour.append(self.neighbours[m])
                    if i.tags == self.neighbours[m] and (i.color == "#013dc6" or i.color == "#0652DD"):
                        self.enemy_neighbour.append(self.neighbours[m])

        self.neighbours = list(set(self.neighbours) - set(self.enemy_neighbour))
        self.neighbours = list(set(self.neighbours) - set(self.friendly_neighbour))

        # This for loop determines if the ennemy is within range
        for p in range(630):
            attackable_x0 = x - 50
            attackable_x1 = x + 50

            attackable_y0 = y - 50
            attackable_y1 = y + 50

            for a in range(len(red_side_colors)):
                if self.playing_side == "blue":
                    if hexagons[p].color == red_side_colors[a] and \
                            attackable_x1 >= hexagons[p].x >= attackable_x0 and \
                            attackable_y1 >= hexagons[p].y >= attackable_y0:
                            self.enemy_neighbour_inrange.append(hexagons[p])
                elif self.playing_side == "red":
                    if hexagons[p].color == blue_side_colors[a] and \
                            attackable_x1 >= hexagons[p].x >= attackable_x0 and \
                            attackable_y1 >= hexagons[p].y >= attackable_y0:
                            self.enemy_neighbour_inrange.append(hexagons[p])

        # The two following for statements fill the near elements of the clicked hexagons
        for m in range(len(self.neighbours)):
            for i in hexagons:  # this for loop erase any trace of its use
                self.canvas_instance.itemconfigure(i.tags, fill=i.color)  # fill the color of the hexagon back to its own

        for m in range(len(self.neighbours)):
            for i in hexagons:
                if i.tags == self.neighbours[m] and i.color != objective_color:
                    self.canvas_instance.itemconfigure(i.tags, fill=moving_color)  # fill the clicked hex with color

    def checkObjective(self):
        for i in range(len(hexagons)):
            if hexagons[i].tags == objective_red[0]:
                for x in blue_side_colors:
                    if hexagons[i].color == x:
                        print("Blue has won !")
                        #TODO : Create prompt "do you want to play again?"

        for i in range(len(hexagons)):
            if hexagons[i].tags == objective_blue[0]:
                for x in red_side_colors:
                    if hexagons[i].color == x:
                        print("Red has won !")


class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        """ Define parameters of the hexagon """
        self.parent = parent
        self.x = x
        self.y = y
        self.length = length
        self.tags = tags
        self.selected = False
        self.color = color

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
        "water": water_color,
        "mountain": mountain_color
    }

    def __init__(self, position, kind):
        self.position = position
        self.kind = kind
        self.color = Field.types[self.kind]
        self.placeField()

    def placeField(self):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags:
                hexagons[x].color = self.color


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
        for x in range(len(hexagons)):
            # this for loop targets the position of the instance with the current position in the form of tags
            # and change the color of the targeted hexagon
            if hexagons[x].tags == self.position:
                hexagons[x].color = self.color
                break
        squad_list.append(self)  # append the instance object to a list
        print("Squad:", self.side, "squad at", self.position, "has been created.")


class Objective:
    def __init__(self, position, side, opposite_side):
        self.position = position
        self.side = side
        self.opposite_side = opposite_side
        self.color = objective_color

        if self.side == "blue":
            for c in red_side_colors:
                self.check_ally(c)

        elif self.side == "red":
            for c in blue_side_colors:
                self.check_ally(c)

    def check_ally(self, enemy_color):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags and hexagons[x].color != enemy_color:
                self.plant_objective()

    def plant_objective(self):
        for x in range(len(hexagons)):
            if self.position == hexagons[x].tags:
                hexagons[x].color = self.color


class Create:
    def __init__(self):
        self.red_squad_infantry = ['21.10', '23.10', '25.10', '27.10', '29.10', '31.10',
                              '33.10', '10.3', '11.4', '12.4', '13.5', '14.5',
                              '15.6', '22.9', '24.9', '26.9', '28.9', '30.9',
                              '32.9', '15.7']

        self.blue_squad_infantry = ['9.4', '10.4', '11.5', '12.5', '13.6', '14.6', '14.7',
                               '7.6', '8.6', '9.7', '10.7', '11.8', '12.8',
                               '13.9', '21.11', '22.10', '23.11', '24.10', '26.10',
                               '28.10', '30.10', '32.10', '25.11', '27.11', '29.11',
                               '31.11', '33.11']

        self.water_list = ['14.8', '14.9', '14.10', '14.11', '15.8', '15.9',
                      '15.10', '15.11', '16.8', '16.9', '16.10', '16.11',
                      '17.9', '17.10', '17.11', '17.12', '18.9', '18.10',
                      '18.11', '19.10', '19.11', '19.12', '20.10', '20.11']

        self.mountain_list = ['11.0', '11.1', '10.0', '10.1', '9.1', '8.1',
                         '8.2', '8.3', '9.2', '9.3', '7.3', '7.4',
                         '7.5', '6.3', '6.4', '6.5']

        self.red_squad_infantry_debug = ['5.13', '15.11']
        self.blue_squad_infantry_debug = ['26.3', '16.11']
        self.water_list_debug = ['17.10']
        self.mountain_list_debug = ['17.5']
        self.objective_red_debug = ['27.4']
        self.objective_blue_debug = ['5.14']

        self.place_element()

    def place_element_debug(self):
        for r in range(len(self.red_squad_infantry_debug)):
            Squad("red", 6, 'infantry', 3, 3, 2, self.red_squad_infantry_debug[r], red_side_colors[0])
        for b in range(len(self.blue_squad_infantry_debug)):
            Squad("blue", 6, 'infantry', 3, 3, 2, self.blue_squad_infantry_debug[b], blue_side_colors[0])
        for w in range(len(self.water_list_debug)):
            Field(self.water_list_debug[w], "water")
        for m in range(len(self.mountain_list_debug)):
            Field(self.mountain_list_debug[m], "mountain")
        for x in self.objective_red_debug:
            Objective(x, "red", "blue")
        for x in self.objective_blue_debug:
            Objective(x, "blue", "red")

    def place_element(self):
        for r in range(len(self.red_squad_infantry)):
            Squad("red", 6, 'infantry', 3, 3, 2, self.red_squad_infantry[r], red_side_colors[0])
        for b in range(len(self.blue_squad_infantry)):
            Squad("blue", 6, 'infantry', 3, 3, 2, self.blue_squad_infantry[b], blue_side_colors[0])
        for w in range(len(self.water_list)):
            Field(self.water_list[w], "water")
        for m in range(len(self.mountain_list)):
            Field(self.mountain_list[m], "mountain")
        for x in objective_red:
            Objective(x, "red", "blue")
        for x in objective_blue:
            Objective(x, "blue", "red")


root = tk.Tk()
Game(root)  # canvas instance
root.mainloop()