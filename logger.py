import logging
from person import Person

class Logger(object):

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
