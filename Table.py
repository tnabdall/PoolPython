import numpy as np
import Ball
import math
from Ball import BALL_RADIUS, Stripes, Solids, BlackBall
from numpy import pi, sqrt
TABLE_WIDTH = 400
TABLE_HEIGHT = 200


def getReferenceAngleRadians(angle):  # Gives reference angle in radians given radian angle
    angle = Ball.principleRadianAngle(angle)
    referenceAngle = 0
    if (angle > np.pi * 3 / 2):
        # referenceAngle = 2*pi-angle
        referenceAngle = angle - pi
    elif angle > pi:
        referenceAngle = angle - pi
    elif angle > pi / 2:
        # referenceAngle = pi-angle
        referenceAngle = angle
    else:
        referenceAngle = angle
    return referenceAngle

def setRandomBalls():
    width = TABLE_WIDTH
    height = TABLE_HEIGHT
    firstPos = [300 / 400 * TABLE_WIDTH, 100 / 200 * TABLE_HEIGHT]  # first ball standardized by table dimensions
    spacing = 0.1 * BALL_RADIUS  # times the Radius, vertical spacing between balls
    positions = []
    positions.append(firstPos)  # first column
    positions.append(
        [firstPos[0] + sqrt(3) * BALL_RADIUS + spacing, firstPos[1] + BALL_RADIUS])  # second column
    positions.append([firstPos[0] + sqrt(3) * BALL_RADIUS + spacing, firstPos[1] - BALL_RADIUS])
    positions.append([positions[1][0] + sqrt(3) * BALL_RADIUS + spacing,
                      positions[1][1] + sqrt(1) * BALL_RADIUS + spacing])  # third column
    positions.append([positions[1][0] + sqrt(3) * BALL_RADIUS + spacing, positions[1][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[1][0] + sqrt(3) * BALL_RADIUS + spacing, positions[2][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[3][0] + sqrt(3) * BALL_RADIUS + spacing,
                      positions[3][1] + sqrt(1) * BALL_RADIUS])  # fourth column
    positions.append([positions[3][0] + sqrt(3) * BALL_RADIUS + spacing, positions[3][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[3][0] + sqrt(3) * BALL_RADIUS + spacing, positions[5][1] + sqrt(1) * BALL_RADIUS])
    positions.append([positions[3][0] + sqrt(3) * BALL_RADIUS + spacing, positions[5][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[6][0] + sqrt(3) * BALL_RADIUS + spacing,
                      positions[6][1] + sqrt(1) * BALL_RADIUS])  # fifth column
    positions.append([positions[6][0] + sqrt(3) * BALL_RADIUS + spacing, positions[6][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[6][0] + sqrt(3) * BALL_RADIUS + spacing, positions[8][1] + sqrt(1) * BALL_RADIUS])
    positions.append([positions[6][0] + sqrt(3) * BALL_RADIUS + spacing, positions[8][1] - sqrt(1) * BALL_RADIUS])
    positions.append([positions[6][0] + sqrt(3) * BALL_RADIUS + spacing, positions[9][1] - sqrt(1) * BALL_RADIUS])

    randomizer = np.arange(1, 15)  # 1-14 (1-7 are stripes, 8-14 are solids (1-7))
    np.random.shuffle(randomizer)

    balls = []
    for i in np.arange(0, 14):
        id = randomizer[i]
        j = i
        if (i > 4):
            j = i + 1
        if (id < 8):
            balls.append(Stripes(positions[j][0], positions[j][1], id))
        else:
            balls.append(Solids(positions[j][0], positions[j][1], id))

    balls.append(BlackBall(positions[5][0], positions[5][1], 8))

    return balls


class Table:
    width = TABLE_WIDTH
    height = TABLE_HEIGHT
    balls = setRandomBalls()

    def __init__(self):
        pass

    def checkCollision2Balls(self, b1, b2):
        distance = np.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)

        if distance <= 2 * BALL_RADIUS and (
                b1.speed > 0.08 or b2.speed > 0.08):  # Checks if collided and whether the balls are going at a huge speed that would make them overlap
            collisionAngle = math.atan2(b2.y - b1.y, b2.x - b1.x)
            vx1 = math.cos(collisionAngle) * (b2.speed * math.cos(b2.angle - collisionAngle)) - math.sin(
                collisionAngle) * (b1.speed * math.sin(b1.angle - collisionAngle))
            vy1 = math.sin(collisionAngle) * (b2.speed * math.cos(b2.angle - collisionAngle)) + math.cos(
                collisionAngle) * (b1.speed * math.sin(b1.angle - collisionAngle))
            vx2 = math.cos(collisionAngle) * (b1.speed * math.cos(b1.angle - collisionAngle)) - math.sin(
                collisionAngle) * (b2.speed * math.sin(b2.angle - collisionAngle))
            vy2 = math.sin(collisionAngle) * (b1.speed * math.cos(b1.angle - collisionAngle)) + math.cos(
                collisionAngle) * (b2.speed * math.sin(b2.angle - collisionAngle))
            print("Collision Angle: " + str(collisionAngle * 180 / pi))
            print(vx1, vy1, vx2, vy2)
            b1.speed = math.sqrt(vx1 ** 2 + vy1 ** 2)
            b1.angle = Ball.principleRadianAngle(math.atan2(vy1, vx1))
            b2.speed = math.sqrt(vx2 ** 2 + vy2 ** 2)
            b2.angle = Ball.principleRadianAngle(math.atan2(vy2, vx2))
            print(b1.speed, b1.angle * 180 / pi, b2.speed, b2.angle * 180 / pi)

            while (distance <= 2 * BALL_RADIUS):  # To split up the two balls
                x1 = b1.x
                y1 = b1.y
                x2 = b2.x
                y2 = b2.y
                b1.updatePosition()
                b2.updatePosition()
                distance = np.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)
                print(b1.id, b1.x, b1.y, b2.id, b2.x, b2.y)
                if b1.distance(Ball.Ball(x1, y1, -5)) / b1.timeDelta < 0.1 and b2.distance(
                        Ball.Ball(x2, y2, -5)) / b2.timeDelta < 0.1:
                    break
        # elif distance <= 2 * BALL_RADIUS and (b1.speed>0.02 or b2.speed>0.02):
        #     if b1.speed>0.02:
        #         movingBall = b1
        #         ball2 = b2
        #     else:
        #         movingBall = b2
        #         ball2 = b1
        #
        #     angleNormal = Ball.principleRadianAngle(math.atan2((ball2.y - movingBall.y), (ball2.x - movingBall.x)))
        #     angleTangent = 0.0
        #     totalSpeedSquared = movingBall.speed ** 2 + ball2.speed ** 2
        #     if movingBall.angle > angleNormal:
        #         angleTangent = angleNormal + math.pi / 2
        #     else:
        #         angleTangent = angleNormal - math.pi / 2
        #     angleTangent = Ball.principleRadianAngle(angleTangent)
        #     # print(self.speed)
        #     if (math.fabs(movingBall.speed * math.cos(angleTangent - movingBall.angle) + ball2.speed * math.cos(
        #             angleTangent - ball2.angle)) < movingBall.speed):
        #         movingBall.speed = math.fabs(movingBall.speed * math.cos(angleTangent - movingBall.angle) + ball2.speed * math.cos(
        #             angleTangent - ball2.angle))
        #     # print(self.speed)
        #     ball2.speed = math.fabs(math.sqrt(totalSpeedSquared - movingBall.speed ** 2))
        #     movingBall.angle = angleTangent
        #     ball2.angle = angleNormal
        #     while (distance <= 2 * BALL_RADIUS):
        #         b1.updatePosition()
        #         b2.updatePosition()
        #         distance = np.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)







def main():
    t = Table()
    for i in np.arange(15):
        print(t.balls[i], t.balls[i].x, t.balls[i].y, t.balls[i].id)

    t.balls[0].shoot(10, math.pi /6)

    while (any(ball.speed >= 0.02 for ball in t.balls)):
        for i in np.arange(15):
            for j in np.arange(i + 1, 15):
                t.checkCollision2Balls(t.balls[i], t.balls[j])
                # print(i,j)
            t.balls[i].updatePosition()
            #print(i,t.balls[i].speed)

    print("\n")

    for i in np.arange(15):
        # print(type(t.balls[i]) is Ball.Stripes) # checks to see if stripes
        print(t.balls[i], t.balls[i].x, t.balls[i].y, t.balls[i].id)


def main2():
    t = Table()
    normalFactor = 5 / 0.12
    t.balls[0].x = 0
    t.balls[0].y = 0
    t.balls[1].x = 0
    t.balls[1].y = normalFactor * 1
    v0x = normalFactor * 0
    v0y = normalFactor * 2
    v1x = normalFactor * 0
    v1y = normalFactor * 0
    v0 = np.sqrt(v0x ** 2 + v0y ** 2)
    v1 = np.sqrt(v1x ** 2 + v1y ** 2)
    angle0 = Ball.principleRadianAngle(np.arctan2(v0y, v0x))
    angle1 = Ball.principleRadianAngle(np.arctan2(v1y, v1x))
    t.balls[0].shoot(v0, angle0)
    t.balls[1].shoot(v1, angle1)
    print(t.balls[0].speed, t.balls[0].angle * 180 / pi)
    print(t.balls[1].speed, t.balls[1].angle * 180 / pi)
    while (t.balls[0].speed > 0.02 or t.balls[1].speed > 0.02):
        t.checkCollision2Balls(t.balls[0], t.balls[1])
        t.balls[0].updatePosition()
        t.balls[1].updatePosition()
        # print(t.balls[0].x, t.balls[0].y, t.balls[1].x, t.balls[1].y)
    print(t.balls[0].speed, Ball.principleRadianAngle(t.balls[0].angle) * 180 / pi)
    print(t.balls[1].speed, Ball.principleRadianAngle(t.balls[1].angle) * 180 / pi)
    print(t.balls[0].x, t.balls[0].y, t.balls[1].x, t.balls[1].y)


def main3():
    t = Table()
    for i in np.arange(len(t.balls)):
        for j in np.arange(i, len(t.balls)):
            print(i, j, t.balls[i].distance(t.balls[j]))

if __name__ == "__main__":
    main()
