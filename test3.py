class App(Tk):
    [...]
    def colorize(self, position, color):  # "self" is required to know that colorize must have an effect on the current App instance
        self.can.itemconfigure(position, fill=color) # position and color of the Squad instance are correctly passed into colorize()
        # However "self.can" is not recognized since "self" of App is overwritten by Squad when

class Squad():
    nb_of_squads = 0

    def __init__(self, side, units, arsenal, ap, dp, position, color):
        self.side = side
        self.units = units
        self.arsenal = arsenal
        self.ap = ap
        self.dp = dp
        self.position = position
        self.color = color
        Squad.nb_of_squads += 1

        self.squadAppear()

    def squadAppear(self):  # self is required to pass the position and color, it cannot be a static method
       App.colorize(self, self.position, self.color)  # This part doesn't work because the object "Squad" is passed into ".colorize(self...)"
        #App.colorize(App.canvas, self.position, self.color) # gives an error that App.canvas doesn't exist.
squad_1 = Squad("blue", 6, 'infantry', 3, 3, 21.23, "#013dc6")
squad_2 = Squad("red", 6, 'infantry', 3, 3, 21.24, "#b71717")