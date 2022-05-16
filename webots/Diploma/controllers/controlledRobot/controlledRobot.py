"""controlledRobot controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard

maxSpeed = 6
def controlled():
    # create the Robot instance.
    robot = Robot()
    keyboard = Keyboard()
    # get the time step of the current world.
    timestep = 64

    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getDevice('motorname')
    #  ds = robot.getDevice('dsname')
    #  ds.enable(timestep)
    leftMotor = robot.getDevice('motor1')
    rightMotor = robot.getDevice('motor2')
    keyboard.enable(timestep)

    leftMotor.setPosition(float('inf'))
    rightMotor.setPosition(float('inf'))

    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(timestep) != -1:
        key = keyboard.getKey()
        leftSpeed = .0
        rightSpeed = .0

        if key == ord('W'):
            leftSpeed = maxSpeed
            rightSpeed = maxSpeed
            print('Moving forwards!')

        if key == ord('S'):
            leftSpeed = -maxSpeed
            rightSpeed = -maxSpeed
            print('Moving backwards!')

        if key == ord('A'):
            leftSpeed = .25 * maxSpeed
            rightSpeed = maxSpeed
            print('Turning Left!')

        if key == ord('D'):
            leftSpeed = maxSpeed
            rightSpeed = .25 * maxSpeed
            print('Turning Right!')

        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)

# Enter here exit cleanup code.
controlled()
