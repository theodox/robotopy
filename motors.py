import logging
import atexit
import math

# this is installed on the pi; source is here
# https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

logger = logging.getLogger('motors')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)




FORWARD = Adafruit_MotorHAT.FORWARD
BACKWARD = Adafruit_MotorHAT.BACKWARD
RELEASE = Adafruit_MotorHAT.RELEASE

# default motor address on the i2c bus
ADDRESS = 0x60

try:
    controller = Adafruit_MotorHAT(ADDRESS)
except IOError:
    logging.critical("unable to configure motors: hardware needs to be reset")
    raise


def desired_speed(ms):
    normalized = min (ms / 0.8, 1)
    normalized = max(normalized, 0)
    # this is a very basic approximation
    # a spline through recorded data
    # would be much better
    normalized = pow(normalized, 1.1)
    return 16 + (239 * normalized)

def set_speed(self, ms):
    self.setSpeed(desired_speed(ms))

def _init_motor(idx):
    # patch the adafruit controller
    # to set speeds in m/s
    motor = controller.getMotor(idx)
    motor.set_speed = set_speed
    return motor

left_rear = _init_motor(1)
left_front = _init_motor(2)
right_front = _init_motor(3)
right_rear = _init_motor(4)
logger.info("motors initialized created")



# a motor value of 255 is about .8m/s  for a well charged battery
# 128 = .38m/s
# 64 = 0.18/s
# 32 =  0.064m/s
# 16 = effectively 0





def shutdown():
    for eachmotor in left_rear, left_front, right_front, right_rear:
        eachmotor.run(RELEASE)

    logging.info("motors shut down")

atexit.register(shutdown())


