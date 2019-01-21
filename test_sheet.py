"""
class board :
    - background
    - hexagon with position (x,y)

class unit
    - create a unit
        - image of unit
        - number of HP
        - defence
        - attack

class movement
    - click on unit
        -> change the color of positions near unit except where there is an enemy or friendly unit
            -> make it so that you can't go behind enemies if there is no path behind them
        - if there is something an other unit on the position, don't do anything
        - if there is an enemy unit and it is within range of attack, then attack
            -> call attack
        - if click on unit again, cancel
        - if click on somewhere in the range of unit, move there

    def move unit
        - move the unit

class player
    - start the turn of the other player when the player clicks on "end turn"

class attack
    - take the attack of the unit minus the defense of the enemy
    - if defence of ennemy > attack of unit, remove the HP of unit
    - if attack > defence, remove defence of ennemy
    - if HP <= 0, make enemy dissapear

def dissapear
    - make unit dissapear

class map
    - places different units on the board before the game starts


"""


class Employee:

    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + "@company.com"

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amount = amount

emp_1 = Employee('Corey', "Schafer", 50000)
emp_2 = Employee('Red', "mark", 20000)


Employee.set_raise_amt(1.05)
Employee.raise_amount = 1.05
#emp_1.raise_amount = 1.05
#print(emp_1.__dict__)
print(emp_1.raise_amount)
print(Employee.raise_amount)
print(emp_2.raise_amount)

#emp_1.raise_amount
#Employee.raise_amount
"""

print(emp_1.email)
print(emp_2.email)

print(emp_1.fullname())
#print('{} {}'.format(emp_1.first, emp_1.last))

#print(emp_1)
#print(emp_2)

emp_1.fullname()
print(Employee.fullname(emp_1))

emp_1.first = 'Corey'
emp_1.last = "Schafer"
emp_1.email = "Corey@gmail.com"
emp_1.pay = "50000"

emp_2.first = 'Red'
emp_2.last = "Shar"
emp_2.email = "red@gmail.com"
emp_2.pay = "30000"
"""