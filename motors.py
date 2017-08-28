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
    normalized = pow(normalized, 0.85)
    output = int(255 * normalized)
    return output

# patch the Adafruit motor to allow 
# setting speeds by m/s.  This also
# applies a drift setting that is
# intended to keep the robot tracking straight
def set_speed(self, ms):
    raw_speed = desired_speed(ms)
    drift = 0
    if hasattr(self, 'drift'):
        drift = self.drift
        logger.info("%s: %i", self, drift)
    adjusted = raw_speed + drift
    adjusted = max(min(adjusted, 255), 0)
    self.setSpeed(adjusted)

Adafruit_DCMotor.set_speed = set_speed

left_rear = controller.getMotor(1)
left_front = controller.getMotor(3)
right_front = controller.getMotor(4)
right_rear = controller.getMotor(2)

# patch the motor to adjust for left-right drift
right_rear.drift = 0
right_front.drift = 64
left_rear.drift = 64
left_front.drift = 32

logger.info("motors initialized created")

# a motor value of 255 is about .8m/s  for a well charged battery
# 128 = .38m/s
# 64 = 0.18/s
# 32 =  0.064m/s
# 16 = effectively 0

def forward(speed):
    for motor in left_rear, right_rear, right_front, left_front:
        motor.set_speed(speed)
        motor.run(FORWARD)

def halt():
    for motor in left_rear, right_rear, right_front, left_front:
        motor.run(RELEASE)

def turn_right():
    for motor in left_rear, left_front, right_front, right_rear:
	motor.set_speed(0.4)
    for motor in left_rear, left_front:
        motor.run(FORWARD)
    for motor in right_rear, right_front:
        motor.run(BACKWARD)


def shutdown():
    for eachmotor in left_rear, right_front, left_front, right_rear:
        eachmotor.run(RELEASE)

    logger.info("motors shut down")

atexit.register(shutdown)

