import logging
from person import Person

class Logger(object):
    '''
    Utility class responsible for logging all interactions of note during the
    simulation.


    _____Attributes______

    file_name: the name of the file that the logger will be writing to.

    _____Methods_____

    __init__(self, file_name):

    write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
        basic_repro_num):
        - Writes the first line of a logfile, which will contain metadata on the
            parameters for the simulation.

    log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        - Expects person1 and person2 as person objects.
        - Expects did_infect, person2_vacc, and person2_sick as Booleans, if passed.
        - Between the values passed with did_infect, person2_vacc, and person2_sick, this method
            should be able to determine exactly what happened in the interaction and create a String
            saying so.
        - The format of the log should be "{person1.ID} infects {person2.ID}", or, for other edge
            cases, "{person1.ID} didn't infect {person2.ID} because {'vaccinated' or 'already sick'}"
        - Appends the interaction to logfile.

    log_infection_survival(self, person, did_die_from_infection):
        - Expects person as Person object.
        - Expects bool for did_die_from_infection, with True denoting they died from
            their infection and False denoting they survived and became immune.
        - The format of the log should be "{person.ID} died from infection" or
            "{person.ID} survived infection."
        - Appends the results of the infection to the logfile.

    log_time_step(self, time_step_number):
        - Expects time_step_number as an Int.
        - This method should write a log telling us when one time step ends, and
            the next time step begins.  The format of this log should be:
                "Time step {time_step_number} ended, beginning {time_step_number + 1}..."
        - STRETCH CHALLENGE DETAILS:
            - If you choose to extend this method, the format of the summary statistics logged
                are up to you.  At minimum, it should contain:
                    - The number of people that were infected during this specific time step.
                    - The number of people that died on this specific time step.
                    - The total number of people infected in the population, including the newly
                        infected
                    - The total number of dead, including those that died during this time step.
    '''

    def __init__(self, file_name):
        self.file_name = file_name
        logging.basicConfig(filename=file_name, level=logging.DEBUG)

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        logging.info('\n\tPopulation size: {}\n\tVaccination percentage: {}\n\n\tVirus name: {}\n\tMortality rate: {}\n\tReproduction num: {}\n'.format(
            pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num))

    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        log = '\n\tperson ({}) interacted with person ({})\n'.format(person1._id, person2._id)
        if did_infect:
            log = log + '\n\t person ({}) infected person ({})\n'.format(person1._id, person2._id)
        if person2_vacc:
            log = log + '\n\t person({}) is vaccinated\n'.format(person2._id)
        if person2_sick:
            log = log + '\n\t person ({}) is sick\n'.format(person2._id)
        
        logging.info(log)

    def log_infection_survival(self, person, did_die_from_infection):
        if did_die_from_infection:
            logging.info('\n\tperson ({}) died from the infection\n'.format(person._id))
        else:
            logging.info('\n\tperson ({}) survived the infection\n'.format(person._id))

    def log_time_step(self, time_step_number, newly_infected, death_toll):
        # TODO: Finish this method.  This method should log when a time step ends, and a
        # new one begins.  See the documentation for more information on the format of the log.
        # NOTE: Stretch challenge opportunity! Modify this method so that at the end of each time
        # step, it also logs a summary of what happened in that time step, including the number of
        # people infected, the number of people dead, etc.  You may want to create a helper class
        # to compute these statistics for you, as a Logger's job is just to write logs!
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!
        logging.info("""\n\nEND TIME STEP {}\n
        There have been {} newly infected\n
        There have been {} deaths\n\n""".format(time_step_number, newly_infected, death_toll))

if __name__ == '__main__':
    logger = Logger('test.log')
    logger.write_metadata(5600, 0.56, 'polio', 0.75, 45)
    person1 = Person(32489234, False)
    person2 = Person(23423411, True)
    logger.log_interaction(person1, person2, False)
    logger.log_infection_survival(person1, True)
    logger.log_time_step(420, 710, 215)
