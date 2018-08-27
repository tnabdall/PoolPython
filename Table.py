import numpy as np
import Ball
import math
from Ball import BALL_RADIUS, Stripes, Solids, BlackBall
from numpy import pi, sqrt
TABLE_WIDTH = 400
TABLE_HEIGHT = 200

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
        if (i > 3):
            j = i + 1
        if (id < 8):
            balls.append(Stripes(positions[j][0], positions[j][1], id))
        else:
            balls.append(Solids(positions[j][0], positions[j][1], id))

    balls.append(BlackBall(positions[4][0], positions[4][1], 8))

    return balls


class Table:
    width = TABLE_WIDTH
    height = TABLE_HEIGHT
    balls = setRandomBalls()  # randomly ordered except for blackBall which is balls[4]
    whiteBall = Ball.WhiteBall(TABLE_WIDTH / 4, TABLE_HEIGHT / 2)
    pockets = [
        [BALL_RADIUS, BALL_RADIUS],
        [TABLE_WIDTH / 2, BALL_RADIUS],
        [TABLE_WIDTH - BALL_RADIUS, BALL_RADIUS],
        [BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS],
        [TABLE_WIDTH / 2, TABLE_HEIGHT - BALL_RADIUS],
        [TABLE_WIDTH - BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS],
    ]

    # blackBall = balls[5]

    def __init__(self):
        pass

    def checkPocketed(self, ball):
        for i in np.arange(len(self.pockets)):
            if sqrt((self.pockets[i][0] - ball.x) ** 2 + (self.pockets[i][1] - ball.y) ** 2) < BALL_RADIUS:
                ball.pocketed = True
                ball.x = -10
                ball.y = -10
                ball.speed = 0
                ball.angle = 0

    def checkCollisionWall(self, ball):

        left = ball.x - BALL_RADIUS
        right = ball.x + BALL_RADIUS
        up = ball.y + BALL_RADIUS
        down = ball.y - BALL_RADIUS
        refAngle = 0  # angle of reflection between ball and wall
        if (left <= 0):
            # print("Wall collision LEFT")
            refAngle = pi - ball.angle
            ball.angle = Ball.principleRadianAngle(refAngle)
        elif right >= TABLE_WIDTH:
            # print("Wall collision RIGHT")
            refAngle = 0.0 - ball.angle
            ball.angle = Ball.principleRadianAngle(pi + refAngle)
        elif up >= TABLE_HEIGHT:
            # print("Wall collision UP")
            refAngle = pi / 2.0 - ball.angle
            ball.angle = Ball.principleRadianAngle(3 * pi / 2.0 + refAngle)
        elif down <= 0:
            # print("Wall collision DOWN")
            refAngle = 3 * pi / 2.0 - ball.angle
            ball.angle = Ball.principleRadianAngle(pi / 2.0 + refAngle)

        while (left < 0 or right > TABLE_WIDTH or down < 0 or up > TABLE_HEIGHT):
            x1 = ball.x
            y1 = ball.y
            ball.updatePosition()
            if ball.distance(Ball.Ball(x1, y1, -5)) / ball.timeDelta < 0.1:
                break
            left = ball.x - BALL_RADIUS
            right = ball.x + BALL_RADIUS
            up = ball.y + BALL_RADIUS
            down = ball.y - BALL_RADIUS



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
            # print("Collision Angle: " + str(collisionAngle * 180 / pi))
            # print(vx1, vy1, vx2, vy2)
            b1.speed = math.sqrt(vx1 ** 2 + vy1 ** 2)
            b1.angle = Ball.principleRadianAngle(math.atan2(vy1, vx1))
            b2.speed = math.sqrt(vx2 ** 2 + vy2 ** 2)
            b2.angle = Ball.principleRadianAngle(math.atan2(vy2, vx2))
            # print(b1.speed, b1.angle * 180 / pi, b2.speed, b2.angle * 180 / pi)

            while (distance <= 2 * BALL_RADIUS):  # To split up the two balls
                x1 = b1.x
                y1 = b1.y
                x2 = b2.x
                y2 = b2.y
                b1.updatePosition()
                b2.updatePosition()
                distance = np.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)
                # print(b1.id, b1.x, b1.y, b2.id, b2.x, b2.y)
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

    t.whiteBall.shoot(10, 0)

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


if __name__ == "__main__":
    main()
