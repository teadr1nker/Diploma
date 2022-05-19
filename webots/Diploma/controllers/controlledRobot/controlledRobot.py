"""controlledRobot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard
import math, socket, time

maxSpeed = 6.42
wheelRadius = .02
HOST = '127.0.0.1'
PORT = 2048
#ENDC = '\033[0m'
GREEN = '\033[92m'

def printg(s):
    print(GREEN + s)

def controlled():
    # create the Robot instance.
    robot = Robot()
    keyboard = Keyboard()
    # get the time step of the current world.
    timestep = 64
    leftMotor = robot.getDevice('motor1')
    rightMotor = robot.getDevice('motor2')
    keyboard.enable(timestep)

    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))

    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)

    odometer1 = robot.getPositionSensor('ps1')
    odometer2 = robot.getPositionSensor('ps2')

    odometer1.enable(timestep)
    odometer2.enable(timestep)
    wheelCircum = 2 * math.pi * wheelRadius
    encoderUnit = wheelRadius
    distanceBetweenWheels = .1
    encoderValues = [0., 0.]
    lastEncoderValues = [0., 0.]
    distance = [0., 0.]
    robotPosition = [0., 1., 0.]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(.1)
    s.connect((HOST, PORT))
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        data = f'{round(robotPosition[0], 2)}:{round(robotPosition[1], 2)}'
        s.send(bytes(data, 'UTF-8'))

        encoderValues = [odometer1.getValue(), odometer2.getValue()]
        for i in range(2):
            difference = encoderValues[i] - lastEncoderValues[i]
            if difference < .001:
                difference = 0.
                encoderValues[i] = lastEncoderValues[i]
            distance[i] = difference * encoderUnit

        v = (distance[0] + distance[1]) / 2.
        w = (distance[0] - distance[1]) / distanceBetweenWheels

        dt = 1.
        robotPosition[2] += w * dt

        vx = v * math.cos(robotPosition[2])
        vy = v * math.sin(robotPosition[2])

        robotPosition[0] += vx * dt
        robotPosition[1] += vy * dt
        printg('Leader position: ')
        printg(f'x: {round(robotPosition[0] * 100, 3)} cm')
        printg(f'y: {round(robotPosition[1] * 100, 3)} cm')
        printg(f'alpha: {round(robotPosition[2], 3)} rad')

        lastEncoderValues = encoderValues

        key = keyboard.getKey()
        leftSpeed = .0
        rightSpeed = .0

        if key == ord('W'):
            leftSpeed = maxSpeed
            rightSpeed = maxSpeed
            printg('Moving forwards!')

        if key == ord('S'):
            leftSpeed = -maxSpeed
            rightSpeed = -maxSpeed
            printg('Moving backwards!')

        if key == ord('A'):
            leftSpeed = .25 * maxSpeed
            rightSpeed = maxSpeed
            printg('Turning Left!')

        if key == ord('D'):
            leftSpeed = maxSpeed
            rightSpeed = .25 * maxSpeed
            printg('Turning Right!')

        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)

        if key == ord('Q'):
            s.close()
            leftMotor.setVelocity(0.)
            rightMotor.setVelocity(0.)
            quit(0)

# Enter here exit cleanup code.
controlled()
