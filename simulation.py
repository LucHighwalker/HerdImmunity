import random
import sys
import datetime
random.seed(42)
from person import Person
from logger import Logger


class Simulation(object):
    population_size = 0
    population = []
    total_infected = 0
    current_infected = 0
    next_person_id = 0
    virus_name = ''
    mortality_rate = 0
    vacc_percentage = 0
    basic_repro_num = 0
    file_name = ''
    logger = None
    newly_infected = []

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.next_person_id = 0
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.vacc_percentage = vacc_percentage
        self.basic_repro_num = basic_repro_num
        self.file_name = "logs/{}_simulation_pop_{}_vp_{}_infected_{}_{}.log".format(
            virus_name, population_size, vacc_percentage, initial_infected, datetime.datetime.now())

        self.logger = Logger(self.file_name)

        self.logger.write_metadata(
            population_size, vacc_percentage, virus_name, 0.75, 0)

        self.newly_infected = []
        self.population = self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        population = []
        infected_count = 0
        while len(population) != self.population_size:
            if infected_count != initial_infected:
                person = Person(self.next_person_id, False, True)
                population.append(person)

                infected_count += 1
            else:
                rand = random.random()
                if rand < self.vacc_percentage:
                    person = Person(self.next_person_id, True)
                else:
                    person = Person(self.next_person_id, False)
                population.append(person)
            self.next_person_id = self.next_person_id + 1
        return population

    def _simulation_should_continue(self):
        infected_remain = False
        population_alive = False

        if self.current_infected > 0:
            infected_remain = True

        for person in self.population:
            if person.is_alive:
                population_alive = True
                break

        if infected_remain and population_alive:
            return True
        else:
            return False

    def run(self):
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            time_step_counter += 1
            self.time_step(time_step_counter)
            should_continue = self._simulation_should_continue()
        print('The simulation has ended after {} turns.'.format(
            time_step_counter))

    def time_step(self, counter):
        interactions = 0
        death_toll = 0
        for person in self.population:
            if interactions < 100 and person.is_alive:
                random_person = random.choice(self.population)
                if person != random_person and random_person.is_alive:
                    self.interaction(person, random_person)
                    interactions = interactions + 1
            death_toll = death_toll + person.did_survive_infection(self.mortality_rate)
        newly_infected_count = len(self.newly_infected)
        self._infect_newly_infected()
        self.logger.log_time_step(counter, newly_infected_count, death_toll)



    def interaction(self, person, random_person):
        assert person != random_person
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.is_vaccinated or random_person.infected:
            self.logger.log_interaction(person, random_person, False, random_person.is_vaccinated, random_person.infected)
        elif person.infected:
            rand = random.random()
            if rand < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, True, random_person.is_vaccinated, random_person.infected)
            else:
                self.logger.log_interaction(person, random_person, False, random_person.is_vaccinated, random_person.infected)
            

    def _infect_newly_infected(self):
        for ID in self.newly_infected:
            for person in self.population:
                if person._id == ID:
                    person.infected = True
                    self.current_infected += 1
                    break
        self.newly_infected = [] 


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()
