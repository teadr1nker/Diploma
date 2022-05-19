"""follower controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard
import math, socket

maxSpeed = 6.28
wheelRadius = .02
HOST = '127.0.0.1'
PORT = 2048

def follow(d=.15, accuracy=.1):
    robot = Robot()
    keyboard = Keyboard()
    timestep = 64

    keyboard.enable(timestep)
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
    x, y = 0., 0.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f'Connected by {addr}')
    while robot.step(timestep) != -1:
        data = conn.recv(64)
        #print(f'recived {str(data)}')
        if len(data) != 0:
            try:
                data = str(data, 'UTF-8').split(':')
                x = float(data[0])
                y = float(data[1])
            except:
                print('data loss!')
        else:
            print('no data recieved!')        

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

        print(f'Follower Position:')
        print(f'x: {round(robotPosition[0] * 100, 3)} cm')
        print(f'y: {round(robotPosition[1] * 100, 3)} cm')
        print(f'alpha: {round(robotPosition[2], 3)} rad')
        lastEncoderValues = encoderValues

        dx, dy = x - robotPosition[0], y - robotPosition[1]
        delta = math.sqrt(dx ** 2 + dy ** 2)
        alpha = robotPosition[2]
        theta = math.atan2(dy, dx)
        print(f'theta: {round(theta, 3)} rad')
        print(f'delta: {round(delta * 100, 3)} cm')
        print(f'moving to: {round(x * 100, 3)}:{round(y * 100, 3)} cm:cm')

        if delta < d:
            leftSpeed = rightSpeed = 0.
            print('Arrived!')
        else:
            leftSpeed = rightSpeed = maxSpeed
            phi = alpha - theta
            print(f'phi: {phi}')
            sin, cos = math.sin(phi), math.cos(phi)
            p = math.sin(accuracy)
            if sin > p:
                if cos >= 0.:
                    leftSpeed *= .25
                else:
                    leftSpeed = -maxSpeed
            elif sin < -p:
                if cos >= 0.:
                    rightSpeed *= .25
                else:
                    rightSpeed = -maxSpeed

        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)

        key = keyboard.getKey()
        if key == ord('Q'):
            s.close()
            leftMotor.setVelocity(0.)
            rightMotor.setVelocity(0.)
            quit(0)

if __name__ == '__main__':
    follow()
