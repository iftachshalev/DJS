from junction import *
import logging as log


def check_junction():

    jc = Junction()
    print(jc)

    while True:

        jc.advance_junction(2)
        print(jc)

        cars = [len(j.cars) for j in jc.roads]
        if sum(cars) == 0:
            print(jc.end_of_simulation())
            break

        jc.action_algo()


check_junction()


log.basicConfig(level=log.DEBUG,
                    format='%(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w')

log.debug('This is a debug message')
log.info('This is an info message')
log.warning('This is a warning message')
log.error('This is an error message')
log.critical('This is a critical message')
