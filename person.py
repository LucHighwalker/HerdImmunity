import random

class Person(object):
    _id = 0
    is_vaccinated = False
    is_alive = True
    infected = None

    def __init__(self, _id, is_vaccinated, infected=None):
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.infected = infected


    def did_survive_infection(self, mortality_rate):
        chance = random.random()
        if chance < mortality_rate:
            self.is_alive = False
            return 1
        else:
            self.infected = None
            self.is_vaccinated = True
            return 0
        
