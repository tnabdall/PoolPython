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
    playerTurn = 1
    player1Type = None
    winner = None
    scratch = False
    firstCollide = None  # see what whiteball collides with first
    numberPocketed = 0
    numberPocketedLastTurn = 0
    solidsPocketedLastTurn = 0
    stripesPocketedLastTurn = 0
    ballsPocketedThisTurn = []

    width = TABLE_WIDTH
    height = TABLE_HEIGHT
    balls = setRandomBalls()  # randomly ordered except for blackBall which is balls[14]
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

    def checkPlayer1Type(self):
        if self.player1Type is None:
            if self.checkScratch() is False and len(self.ballsPocketedThisTurn) > 0:
                lastBallCollided = self.ballsPocketedThisTurn[len(self.ballsPocketedThisTurn) - 1]
                if type(lastBallCollided) is Solids:
                    self.player1Type = "Solids"
                    print("Player is solids")
                elif type(lastBallCollided) is Stripes:
                    self.player1Type = "Stripes"
                    print("Player is stripes")


    def checkPocketed(self, ball):
        if (ball.x > 0 or ball.y > 0):
            for i in np.arange(len(self.pockets)):
                if sqrt((self.pockets[i][0] - ball.x) ** 2 + (self.pockets[i][1] - ball.y) ** 2) < 2 * BALL_RADIUS:
                    ball.pocketed = True
                    ball.x = -10
                    ball.y = -10
                    ball.speed = 0
                    ball.angle = 0
                    self.numberPocketed += 1
                    self.ballsPocketedThisTurn.append(ball)
                    print(type(ball))

                    if type(ball) is Ball.Stripes:
                        self.lastPocketed = "Stripes"
                    elif type(ball) is Ball.BlackBall:
                        self.lastPocketed = "BlackBall"
                        print("BlackBall pocketed")
                    elif type(ball) is Ball.Solids:
                        self.lastPocketed = "Solids"
                    else:
                        self.lastPocketed = "WhiteBall"


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

    def switchTurn(self):
        if self.playerTurn == 1:
            self.playerTurn = 2
        else:
            self.playerTurn = 1

        if (self.whiteBall.pocketed == True):
            self.resetWhiteBall()

        self.numberPocketedLastTurn = self.numberPocketed
        self.solidsPocketedLastTurn = self.numberSolidsPocketed()
        self.stripesPocketedLastTurn = self.numberStripesPocketed()
        self.ballsPocketedThisTurn.clear()
        self.firstCollide = None

    def checkCollision2Balls(self, b1, b2):
        distance = np.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)
        if b1.x == -10 or b2.x == -10 or b1.y == -10 or b2.y == -10 or (b1.speed == 0 and b2.speed == 0):
            pass
        elif distance <= 2 * BALL_RADIUS and (
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

            if self.firstCollide is None and (type(b1) is Ball.WhiteBall or type(b2) is Ball.WhiteBall):
                if type(b1) is Ball.WhiteBall:
                    self.firstCollide = type(b2)
                else:
                    self.firstCollide = type(b1)

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

    def numberStripesPocketed(self):
        x = 0
        for i in np.arange(len(self.ballsPocketedThisTurn)):
            if type(self.ballsPocketedThisTurn[i] is Ball.Stripes):
                x += 1
        return x

    def numberSolidsPocketed(self):
        x = 0
        for i in np.arange(len(self.ballsPocketedThisTurn)):
            if type(self.ballsPocketedThisTurn[i] is Ball.Solids):
                x += 1
        return x

    def resetWhiteBall(self):
        self.whiteBall.pocketed = False
        self.whiteBall.x, self.whiteBall.y = TABLE_WIDTH / 4, TABLE_HEIGHT / 2

    def checkScratch(self):
        blackBallPocketed = self.blackBallSunk()
        stripesPocketed = None
        solidsPocketed = None
        if self.numberStripesPocketed() - self.stripesPocketedLastTurn > 0:
            stripesPocketed = True
        else:
            stripesPocketed = False

        if self.numberSolidsPocketed() - self.solidsPocketedLastTurn > 0:
            solidsPocketed = True
        else:
            solidsPocketed = False

        typeToSink = None
        if self.playerTurn == 1:
            typeToSink = self.player1Type
        else:
            if self.player1Type == "Solids":
                typeToSink = "Stripes"
            elif self.player1Type == "Stripes":
                typeToSink = "Solids"

        print(typeToSink)

        if self.whiteBall.pocketed is True:  # First check
            print("Scratch whiteball pocketed")
            return True

        if self.firstCollide is None:
            print("Scratch nothing hit")
            return True

        if self.firstCollide is BlackBall:
            if typeToSink == "Stripes":
                if self.numberStripesPocketed() < 7:
                    print("Scratch hit blackball w/o sinking all stripes")
                    return True
            elif typeToSink == "Solids":
                if self.numberSolidsPocketed() < 7:
                    print("Scratch hit blackball w/o sinking all solids")
                    return True

        if self.firstCollide is Stripes:
            if typeToSink == "Solids":
                print("scratch, hit a stripe when you should have hit a solid")
                return True

        if self.firstCollide is Solids:
            if typeToSink == "Stripes":
                print("scratch, hit a solid when you should have hit a stripe")
                return True

        if typeToSink == "Solids":
            if self.numberStripesPocketed() - self.stripesPocketedLastTurn > 0:
                print("Scratch, sunk a stripe when you are solids")
                return True

        if typeToSink == "Stripes":
            if self.numberSolidsPocketed() - self.solidsPocketedLastTurn > 0:
                print("Scratch, sunk a solid when you are stripes")
                return True

        if self.player1Type is None and self.numberPocketed - self.numberPocketedLastTurn > 1:
            ballType = type(self.ballsPocketedThisTurn[0])
            for i in np.arange(len(self.ballsPocketedThisTurn)):
                if ballType != type(self.ballsPocketedThisTurn[i]):
                    print("Scratch, not all ball types sunk were the same")
                    return True
            if self.playerTurn == 1 and ballType is Ball.Solids:
                self.player1Type = "Solids"
                print("1Solids")
            elif self.playerTurn == 2 and ballType is Ball.Solids:
                self.player1Type = "Stripes"
                print("2Stripes")
            elif self.playerTurn == 1 and ballType is Ball.Stripes:
                self.player1Type = "Stripes"
                print("1Stripes")
            elif self.playerTurn == 2 and ballType is Ball.Stripes:
                self.player1Type = "Solids"
                print("2Solids")

        else:
            print("No scratch")
            return False


            # else: # Not a scratch, so assign the type
            #     if self.playerTurn == 1 and ballType is Ball.Solids:
            #         self.player1Type = "Solids"
            #     elif self.playerTurn == 2 and ballType is Ball.Solids:
            #         self.player1Type = "Stripes"
            #     elif self.playerTurn == 1 and ballType is Ball.Stripes:
            #         self.player1Type = "Stripes"
            #     elif self.playerTurn == 2 and ballType is Ball.Stripes:
            #         self.player1Type = "Solids"

    def blackBallSunk(self):
        return self.balls[14].pocketed

    def GameResult(self):  # Called when black ball is sunk to see who wins.
        # if self.blackBallSunk():
        if self.checkScratch() is True:
            if self.playerTurn == 1:
                return 2
            else:
                return 1
        else:
            if self.playerTurn == 1:
                if self.player1Type == "Solids":
                    if self.numberSolidsPocketed() == 7:
                        return 1
                    else:
                        return 2
                elif self.player1Type == "Stripes":
                    if self.numberStripesPocketed() == 7:
                        return 1
                    else:
                        return 2
                else:
                    print("Player had no type.")
                    return 2
            else:
                player2Type = None
                if self.player1Type == "Solids":
                    player2Type = "Stripes"
                elif self.player1Type == "Stripes":
                    player2Type = "Solids"

                if player2Type == "Stripes":
                    if self.numberStripesPocketed() == 7:
                        return 2
                    else:
                        return 1
                elif player2Type == "Solids":
                    if self.numberSolidsPocketed() == 7:
                        return 2
                    else:
                        return 1
                else:
                    print("Player had no type.")
                    return 1




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
