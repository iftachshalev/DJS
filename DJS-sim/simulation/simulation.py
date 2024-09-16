from junction import *
import logging as log


def check_junction():

    jc = Junction()
    jc.run(2)


check_junction()

# log.basicConfig(level=log.DEBUG,
#                     format='%(levelname)s - %(message)s',
#                     filename='app.log',
#                     filemode='w')
#
# log.debug('This is a debug message')
# log.info('This is an info message')
# log.warning('This is a warning message')
# log.error('This is an error message')
# log.critical('This is a critical message')
