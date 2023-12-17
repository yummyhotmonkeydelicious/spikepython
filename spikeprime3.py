from hub import light_matrix, port, motion_sensor, button
import runloop, motor_pair, motor, sys, color_sensor, color, time

motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

WHEEL_CIRCUMFERENCE = 17.53 # cm, this is a constant for your robot
def degreesForDistance(distance_cm): # input must be in the same unit as WHEEL_CIRCUMFERENCE
    return int((distance_cm/WHEEL_CIRCUMFERENCE) * 360) # Add multiplier for gear ratio if neede

def is_color_black():
    return color_sensor.color(port.B)is color.BLACK

async def main():
    motion_sensor.reset_yaw(0)
    motor.run(port.E, 200)
    motor.run(port.A, 200)
    while True:
        print(motion_sensor.tilt_angles()[0])
        if motion_sensor.tilt_angles()[0] >= 900:
            motor.stop(port.A, stop=motor.BRAKE)
            motor.stop(port.E, stop=motor.BRAKE)
            break
    print(900-motion_sensor.tilt_angles()[0])

async def turn_180(TURNTYPE):
    if TURNTYPE == "SPIN":
        motion_sensor.reset_yaw(0)
        motor.run(port.E, 200)
        motor.run(port.A, 200)
        while True:
            if motion_sensor.tilt_angles()[0] >= 1800 or motion_sensor.tilt_angles()[0] <= -900:
                motor.stop(port.A, stop=motor.BRAKE)
                motor.stop(port.E, stop=motor.BRAKE)
    if TURNTYPE == "PIVOT":
        motor.run(port.E, 200)
        motion_sensor.reset_yaw(0)
        while True:
            if motion_sensor.tilt_angles()[0] >= 1800 or motion_sensor.tilt_angles()[0] <= -1800:
                motor.stop(port.E, stop=motor.BRAKE)
                motor.stop(port.A, stop=motor.BRAKE)

async def gyro_turn(direction, turn_type):
    way = 0
    if direction == "CLOCKWISE":
        way = -1
    if direction == "COUNTERCLOCKWISE":
        way = 1
    if turn_type == "SPIN":
        motion_sensor.reset_yaw(0)
        motor.run(port.E, 200 * way)
        motor.run(port.A, 200 * way)
        while True:
            if motion_sensor.tilt_angles()[0] >= 900 or motion_sensor.tilt_angles()[0] <= -900:
                motor.stop(port.A, stop=motor.BRAKE)
                motor.stop(port.E, stop=motor.BRAKE)
                break

    if turn_type == "PIVOT":
        if direction == "CLOCKWISE":
            motor.run(port.A, 200 * way)
        if direction == "COUNTERCLOCKWISE":
            motor.run(port.E, 200 * way)
        motion_sensor.reset_yaw(0)
        while True:
            if motion_sensor.tilt_angles()[0] >= 900 or motion_sensor.tilt_angles()[0] <= -900:
                motor.stop(port.E, stop=motor.BRAKE)
                motor.stop(port.A, stop=motor.BRAKE)
                break

    if turn_type == "CURVE":
        motion_sensor.reset_yaw(0)
        if direction == "CLOCKWISE":
            motor.run(port.E, -100 * way)
            motor.run(port.A, 200 * way)
        if direction == "COUNTERCLOCKWISE":
            motor.run(port.E, 200 * way)
            motor.run(port.A, -100 * way)
        while True:
            if motion_sensor.tilt_angles()[0] >= 900 or motion_sensor.tilt_angles()[0] <= -900:
                motor.stop(port.A, stop=motor.BRAKE)
                motor.stop(port.E, stop=motor.BRAKE)
                break

async def gyro_move_straight():
    motion_sensor.reset_yaw(0)
    direction1 = 100
    direction2 = 100
    motor.run(port.E, direction1)
    motor.run(port.A, -direction2)
    if motion_sensor.tilt_angles()[0] >= 10:
        direction2 += 5
    if  motion_sensor.tilt_angles()[0] <= 10:
        direction1 += 5
    if color_sensor.color(port.B) >= 45:
        motor.stop(port.A, stop=motor.BRAKE)
        motor.stop(port.E, stop=motor.BRAKE)

async def line_follow():
    motion_sensor.reset_yaw(0)
    while True:
        if color_sensor.reflection(port.B) <= 50:
            motor_pair.move(motor_pair.PAIR_1, 30, velocity = 100)
        else:
            motor_pair.move(motor_pair.PAIR_1, -30, velocity = 100)
        if color_sensor.reflection(port.F) >= 50:
            break
    motor.stop(port.A, stop=motor.BRAKE)
    motor.stop(port.E, stop=motor.BRAKE)



async def line_follow_opposite():
    motion_sensor.reset_yaw(0)
    while True:
        if color_sensor.reflection(port.F) <= 50:
            motor_pair.move(motor_pair.PAIR_1, 30, velocity = 100)
        else:
            motor_pair.move(motor_pair.PAIR_1, -30, velocity = 100)
        if color_sensor.reflection(port.B) >= 50:
            break
    motor.stop(port.A, stop=motor.BRAKE)
    motor.stop(port.E, stop=motor.BRAKE)
async def x():
    for i in range(1750):
        motor.run(port.E, 150)
        motor.run(port.A, -150)
    motor.stop(port.A, stop=motor.BRAKE)
    motor.stop(port.E, stop=motor.BRAKE)
async def y():
    for i in range(2000):
        motor.run(port.E, 400)
        motor.run(port.A, -400)
    motor.stop(port.A, stop=motor.BRAKE)
    motor.stop(port.E, stop=motor.BRAKE)

def arm_move(direction, speed):
    if direction == "UP":
        motor.run_for_degrees(port.D, -600, speed)
    if direction == "DOWN":
        motor.run_for_degrees(port.D, -600, speed)

async def arm_up():
    motor.run_for_degrees(port.D, 600, 200)


async def arm_down():
    motor.run_for_degrees(port.D, -600, 200)

async def treecowsnot():
    await line_follow()
    await x()
    await gyro_turn("CLOCKWISE", "PIVOT")
    motion_sensor.reset_yaw(0)
    await line_follow()
    await y()
    await gyro_turn("COUNTERCLOCKWISE", "PIVOT")
    await line_follow()
    await arm_up()

async def gyro_forward_move_degrees(degree, speed):
    direction1 = 200
    direction2 = 200
    motor.run_for_degrees(port.A, degree, direction1)
    motor.run_for_degrees(port.E, degree, -direction2)
    while True:
        if motion_sensor.tilt_angles()[0] >= 10:
            direction1 += 5
        elif motion_sensor.tilt_angles()[0] <= -10:
            direction2 += 5



async def line_follow_stop_line(line_follow_sensor, line_stop_sensor, speed, white, black, proportional_gain):
    while True:
        fart = (white - black) / 2
        deviation = color_sensor.reflection(line_follow_sensor) - fart
        turn_rate = proportional_gain * deviation


#runloop.run(line_follow_stop_line(port.C, port.F, 200))
