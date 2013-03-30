import serial
import math
import time

FORWARD = 1
BACKWARD = 2

SINGLE = 1
DUAL = 2
INTERLEAVE = 3
MICROSTEP = 4

RIGHT = 1
LEFT = 2

DOWN = 1
UP = 2

class Canvas(object):

    def __init__(self, port="/dev/ttyACM0", baudrate=9600, **kwargs):
        ### arduino connection setup
        try:
            self.arduino = serial.Serial(port=port, baudrate=baudrate, **kwargs)
        except serial.SerialException:
            self.arduino = serial.Serial(port="/dev/ttyACM1", baudrate=baudrate, **kwargs)

        ### canvas geometry - constants
        self.length_per_rotation = 4.6 ### cm
        self.full_rotiation = 200.0 ### steps
        self.canvas_offset_x = 0.0
        self.canvas_offset_y = 0.0
        self.motors_apart = 59.0 ### cm

        ### canvas geometry - variables
        self.left = 50
        self.right = 50
        self.position = Vector()

    def runCommand(self, motor, speed, steps, direction, style):
        """send the message to the arduino and return the execution code"""

        direction_tmp = None
        if int(motor) == LEFT:
            direction_tmp = FORWARD if int(direction) == DOWN else BACKWARD
        elif int(motor) == RIGHT:
            direction_tmp = BACKWARD if int(direction) == DOWN else FORWARD

        message = "{0};".format(",".join([str(int(motor)), str(int(speed)), str(int(steps)), str(int(direction_tmp)), str(int(style))]))
        code = self.arduino.write(message)

        self.__updatePositionAfterCommand__(motor, steps, direction)
        return code

    def __updatePositionAfterCommand__(self, motor, steps, direction):
        """recalculate position based on command values"""
        ### calculate the new rope length
        motor = int(motor)
        steps = int(steps)
        direction = int(direction)
        length = (self.length_per_rotation / self.full_rotiation) * steps ### in cm
        if motor == RIGHT and direction == DOWN:
            self.right += length
        elif motor == RIGHT and direction == UP:
            self.right -= length
        elif motor == LEFT and direction == UP:
            self.left -= length
        elif motor == LEFT and direction == DOWN:
            self.left += length

        self.__updatePosition__()

    def __updatePosition__(self):
        """update the current position"""
        ### update the canvas position
        a = self.motors_apart
        b = self.left
        c = self.right

        s = (a+b+c) / 2.0 ### semiperimeter
        self.position.y = (2*(math.sqrt(s*(s-a) * (s-b) * (s-c))))/a
        self.position.x = math.sqrt(self.left**2 - self.position.y**2)

    def updateGeometry(self, left, right, motors_apart):
        self.left = float(left)
        self.right = float(right)
        self.motors_apart = float(motors_apart)
        self.__updatePosition__()

    def moveTo(self, x, y):
        x = float(x)
        y = float(y)
        left = math.sqrt(x**2 + y**2)
        xr = self.motors_apart - x
        right = math.sqrt(xr**2 + y**2)
        self.__moveTo__(new_left=left, new_right=right)

    def __moveTo__(self, new_left, new_right):
        cm_per_step = self.length_per_rotation / self.full_rotiation
        left_steps = int((new_left - self.left) / cm_per_step)
        right_steps = int((new_right - self.right) / cm_per_step)

        motor_left_direction = FORWARD if left_steps < 0 else BACKWARD
        motor_right_direction = FORWARD if right_steps > 0 else BACKWARD

        step_size = 10
        speed = 10
        if left_steps < right_steps:
            right_factor = float(right_steps)/left_steps;
            for x in xrange(left_steps/step_size):
                self.runCommand(motor=RIGHT, speed=speed, steps=abs(step_size*right_factor), direction=motor_right_direction, style=INTERLEAVE)
                self.runCommand(motor=LEFT, speed=speed, steps=abs(step_size), direction=motor_left_direction, style=INTERLEAVE)
                time.sleep(0.1)
        else:
            left_factor = float(left_steps)/right_steps;
            for x in xrange(right_steps/step_size):
                self.runCommand(motor=RIGHT, speed=speed, steps=abs(step_size), direction=motor_right_direction, style=INTERLEAVE)
                self.runCommand(motor=LEFT, speed=speed, steps=abs(step_size*left_factor), direction=motor_left_direction, style=INTERLEAVE)
                time.sleep(0.1)


class Vector(object):

    def __init__(self, x=0, y=0):
        self.x = 0
        self.y = 0

    def __repr__(self):
        return "({0}; {1})".format(self.x, self.y)