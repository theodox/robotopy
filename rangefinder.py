from grovepi import *
import logging
import sys
logger  = logging.getLogger("range")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel (logging.DEBUG)


RANGE_PORT = 4




def get_range():
    stop = 0
    while not stop:
        stop = yield
	logger.warning("got: %s", stop)    
	try:
        	# Read distance value from Ultrasonic
        	yield ultrasonicRead(RANGE_PORT) 

	except TypeError:
        	logger.warning ("TYPE ERROR")
		stop = 1
    	except IOError:
       		logger.warning("IO Error")
        	stop = 1

