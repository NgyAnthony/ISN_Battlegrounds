class Create:
    def __init__(self):
        # <--------- MAP 0 --------->
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
        self.bonus = ['5.5']

        # <--------- MAP DEBUG --------->
        self.red_squad_infantry_debug = ['5.11']
        self.blue_squad_infantry_debug = ['10.11']
        self.water_list_debug = ['15.11']
        self.mountain_list_debug = ['20.11']
        self.objective_red_debug = ['25.11']
        self.objective_blue_debug = ['30.16']
        self.bonus_debug = ['5.5']

        # <--------- MAP 1 --------->
        self.red_squad_infantry_map1 = ['5.1', '5.2', '5.3', '30.12', '31.13', '32.13', '23.3', '22.4', '24.4', '20.1', '18.2', '20.3', '31.4', '30.5', '32.6', '16.7']
        self.blue_squad_infantry_map1 = ['13.9', '4.13', '6.12', '6.14', '2.10', '1.12', '4.11', '10.14', '9.16', '11.16', '1.3', '2.3', '3.4', '27.14', '28.14', '29.15']
        self.water_list_map1 = []
        self.mountain_list_map1 = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11', '0.12', '0.13', '0.14', '0.15', '0.16', '0.17', '1.17', '2.17', '3.17', '4.17', '5.17', '6.17', '7.17', '8.17', '9.17', '10.17', '11.17', '12.17', '13.17', '14.17', '15.17', '16.17', '17.17', '18.17', '19.17', '20.17', '21.17', '22.17', '23.17', '24.17', '25.17', '26.17', '27.17', '28.17', '29.17', '30.17', '31.17', '32.17', '33.17', '34.17', '34.16', '34.15', '34.14', '34.13', '34.12', '34.11', '34.10', '34.9', '34.8', '34.7', '34.6', '34.5', '34.4', '34.3', '34.2', '34.1', '34.0', '33.0', '32.0', '31.0', '30.0', '29.0', '28.0', '27.0', '26.0', '25.0', '24.0', '23.0', '22.0', '21.0', '20.0', '19.0', '18.0', '17.0', '16.0', '15.0', '14.0', '13.0', '12.0', '11.0', '10.0', '9.0', '8.0', '7.0', '6.0', '5.0', '4.0', '3.0', '2.0', '1.0', '4.3', '10.8', '5.11', '10.13', '17.9', '21.12', '20.11', '19.11', '18.11', '17.12', '16.9', '17.10', '16.10', '15.11', '15.12', '15.13', '12.11', '11.12', '11.13', '13.11', '13.12', '13.13', '15.10', '4.4', '5.4', '5.5', '4.5', '5.6', '6.5', '7.6', '7.7', '7.8', '6.8', '5.8', '9.8', '9.7', '9.9', '8.9', '7.10', '5.10', '6.10', '10.7', '10.6', '9.6', '7.5', '6.4', '11.4', '12.4', '13.5', '14.5', '15.6', '16.5', '19.8', '20.7', '21.8', '21.9', '22.8', '22.9', '23.9', '23.10', '24.9', '24.10', '25.11', '26.11', '25.12', '24.11', '26.10', '27.10', '28.10', '28.11', '29.9', '30.9', '30.10', '30.11', '28.8', '28.7', '27.7', '26.6', '26.5', '26.4', '22.7', '23.7', '24.6', '18.4', '17.4', '16.3', '18.3', '19.4', '23.8', '24.7', '25.8', '24.8', '25.9', '27.5', '27.6', '28.6', '29.7', '29.8', '30.8', '13.4', '14.3']
        self.objective_red_map1 = ['33.1']
        self.objective_blue_map1 = ['1.16']
        self.bonus_map1 = ['12.12', '6.7', '6.6', '20.8', '25.10', '27.11', '14.4', '15.5', '12.3']

        self.place_element_map1()

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
        for a in self.bonus_debug:
            Bonus(a, 3)

    def place_element(self):
        for r in range(len(self.red_squad_infantry)):
            Squad("red", 6, 'infantry', 2, 1, 2, self.red_squad_infantry[r], red_side_colors[0])
        for b in range(len(self.blue_squad_infantry)):
            Squad("blue", 6, 'infantry', 2, 1, 2, self.blue_squad_infantry[b], blue_side_colors[0])
        for w in range(len(self.water_list)):
            Field(self.water_list[w], "water")
        for m in range(len(self.mountain_list)):
            Field(self.mountain_list[m], "mountain")
        for x in objective_red:
            Objective(x, "red", "blue")
        for x in objective_blue:
            Objective(x, "blue", "red")
        for a in self.bonus:
            Bonus(a, 3)

    def place_element_map1(self):
        for r in range(len(self.red_squad_infantry_map1)):
            Squad("red", 6, 'infantry', 2, 1, 2, self.red_squad_infantry_map1[r], red_side_colors[0])
        for b in range(len(self.blue_squad_infantry_map1)):
            Squad("blue", 6, 'infantry', 2, 1, 2, self.blue_squad_infantry_map1[b], blue_side_colors[0])
        for w in range(len(self.water_list_map1)):
            Field(self.water_list_map1[w], "water")
        for m in range(len(self.mountain_list_map1)):
            Field(self.mountain_list_map1[m], "mountain")
        for x in self.objective_red_map1:
            Objective(x, "red", "blue")
        for x in self.objective_blue_map1:
            Objective(x, "blue", "red")
        for a in self.bonus_map1:
            Bonus(a, 3)
