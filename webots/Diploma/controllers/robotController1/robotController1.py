"""robotController1 controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import math, socket

maxSpeed = 6.28
wheelRadius = .02
HOST = '127.0.0.1'
PORT = 2048

def straightDrive():
    # create the Robot instance.
    robot = Robot()

    # get the time step of the current world.
    timestep = 64

    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getDevice('motorname')
    #  ds = robot.getDevice('dsname')
    #  ds.enable(timestep)
    leftMotor = robot.getDevice('motor1')
    rightMotor = robot.getDevice('motor2')

    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))

    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        leftSpeed = .5 * maxSpeed
        rightSpeed = .5 * maxSpeed

        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)
        # Read the sensors:
        # Enter here functions to read sensor data, like:
        #  val = ds.getValue()

        # Process sensor data here.

        # Enter here functions to send actuator commands, like:
        #  motor.setPosition(10.0)
        #pass

    # Enter here exit cleanup code.

def doughnuts():
    robot = Robot()
    timestep = 64

    leftMotor = robot.getDevice('motor1')
    rightMotor = robot.getDevice('motor2')
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

    encoderValues = [0., 0.]
    lastEncoderValues = [0., 0.]

    distance = [0., 0.]
    robotPosition = [0., 0., 0.]           #x, y, alpha
    distanceBetweenWheels = .1

    while robot.step(timestep) != -1:
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

        if robotPosition[2] >= math.pi * 2:
            robotPosition[2] -= 2 * math.pi
        elif robotPosition[2] < math.pi * -2:
            robotPosition[2] += 2 * math.pi

        vx = v * math.cos(robotPosition[2])
        vy = v * math.sin(robotPosition[2])

        robotPosition[0] += vx * dt
        robotPosition[1] += vy * dt

        leftSpeed = .75 * maxSpeed
        rightSpeed = .75 * maxSpeed

        print(f'Follower Position:')
        print(f'x: {round(robotPosition[0] * 100, 3)} cm')
        print(f'y: {round(robotPosition[1] * 100, 3)} cm')
        print(f'alpha: {round(robotPosition[2], 3)} rad')

        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)

        lastEncoderValues = encoderValues

def goto(x=0, y=0, d=.05, accuracy=.05):
    robot = Robot()
    timestep = 64

    leftMotor = robot.getDevice('motor1')
    rightMotor = robot.getDevice('motor2')
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

    encoderValues = [0., 0.]
    lastEncoderValues = [0., 0.]

    distance = [0., 0.]
    robotPosition = [0., 0., 0.]           #x, y, alpha
    distanceBetweenWheels = .1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f'Connected by {addr}')
    while robot.step(timestep) != -1:
        data = conn.recv(64)
        print(f'recived {str(data)}')
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

        if robotPosition[2] >= math.pi * 2:
            robotPosition[2] -= 2 * math.pi
        elif robotPosition[2] < math.pi * -2:
            robotPosition[2] += 2 * math.pi

        vx = v * math.cos(robotPosition[2])
        vy = v * math.sin(robotPosition[2])

        robotPosition[0] += vx * dt
        robotPosition[1] += vy * dt

        print(f'Robot Position:')
        print(f'x: {round(robotPosition[0] * 100, 3)} cm')
        print(f'y: {round(robotPosition[1] * 100, 3)} cm')
        print(f'alpha: {round(robotPosition[2], 3)} rad')
        lastEncoderValues = encoderValues

        dx, dy = x - robotPosition[0], y - robotPosition[1]
        delta = math.sqrt(dx ** 2 + dy ** 2)
        alpha = robotPosition[2]
        theta = -(math.atan2(dx, dy) - math.pi / 2.)
        print(f'theta: {round(theta, 3)} rad')
        print(f'delta: {round(delta * 100, 3)} cm')
        print(f'moving to: {round(x * 100, 3)}:{round(y * 100, 3)} cm:cm')

        if delta < d:
            leftSpeed = rightSpeed = 0.
            print('Arrived!')
        else:
            leftSpeed = rightSpeed = maxSpeed

            phi = alpha - theta
            print(f'adjusting: {round(phi, 3)} rad')
            if phi > accuracy:
                leftSpeed *= .25

            elif phi < -accuracy:
                rightSpeed *= .25


        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)

if __name__ == '__main__':
    #straightDrive()
    #doughnuts()
    goto(1, 1)
