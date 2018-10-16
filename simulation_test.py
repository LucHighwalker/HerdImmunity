import pytest
import random
import io
import sys
from simulation import Simulation

# Helper Function
def create_simulation():
    return Simulation(4200, 0.17, 'hi', 0.2, 5, 5)


def test__create_population():
    sim = create_simulation()
    assert len(sim.population) == 4200
    assert sim.current_infected == 5
    assert sim.total_infected == 5


def test__simulation_should_continue():
    sim = create_simulation()
    assert sim._simulation_should_continue() == True
    sim.current_infected = 0
    assert sim._simulation_should_continue() == False
    sim.current_infected = 420
    for person in sim.population:
        person.is_alive = False
    assert sim._simulation_should_continue() == False


def test_run():
    sim = create_simulation()
    assert sim.current_infected == 5
    sim.run()
    assert sim.current_infected != 5


def test_time_step():
    sim = create_simulation()
    assert sim.current_infected == 5
    sim.time_step(5)
    assert sim.current_infected != 5


def test_interaction():
    sim = create_simulation()
    death_toll = 0
    interactions = 0
    for person in sim.population:
        if interactions < 10 and person.is_alive:
            random_person = random.choice(sim.population)
            if person != random_person and random_person.is_alive:
                sim.interaction(person, random_person)
                interactions = interactions + 1
        death_toll += person.did_survive_infection(sim.mortality_rate)
    assert death_toll > 0


def test__infect_newly_infected():
    sim = create_simulation()
    victimID = None
    for person in sim.population:
      if person.infected == None:
        sim.newly_infected.append(person._id)
        victimID = person._id
        break
    sim._infect_newly_infected()
    assert sim.population[victimID].infected == True
