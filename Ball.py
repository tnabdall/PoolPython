import math, numpy as np, scipy as sp
import scipy.optimize as opt


def principleRadianAngle(angle):
    if angle > 2 * math.pi:
        while (angle > 2 * math.pi):
            angle = angle - 2 * math.pi
        return angle
    elif angle < 0:
        while (angle < 0):
            angle = angle + 2 * math.pi
        return angle
    else:
        return angle

class Ball:
    x = 0.0
    y = 0.0
    rad = 5.0  # m
    speed = 0.0  # m/s
    angle = 0.0  # rads
    pocketed = False
    collisionSpeedX = 0.0
    collisionSpeedY = 0.0
    timeDelta = 0.01  # s
    friction = 0.009  # (m/s^2)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def speedX(self):
        return math.cos(self.angle) * self.speed

    def speedY(self):
        return math.sin(self.angle) * self.speed

    def angleDegree(self):
        return self.angle * 180 / math.pi

    def shoot(self, power,
              angle):  # power in m/s converted from N because all mass is the same, angle in radians starting from east 0 rads
        self.speed = power
        self.angle = angle

    def updatePosition(self):
        if self.speed > 0.02:
            self.x = self.x + self.speed * math.cos(self.angle) * self.timeDelta
            self.y = self.y + self.speed * math.sin(self.angle) * self.timeDelta
            self.speed = self.speed - self.friction * self.timeDelta

    def collide(self, ball2):
        distance = math.sqrt((self.x - ball2.x) ** 2 + (self.y - ball2.y) ** 2)
        if distance <= 2 * self.rad:
            angleNormal = principleRadianAngle(math.atan2((ball2.y - self.y), (ball2.x - self.x)))
            angleTangent = 0.0
            totalSpeedSquared = self.speed ** 2 + ball2.speed ** 2
            if self.angle > angleNormal:
                angleTangent = angleNormal + math.pi / 2
            else:
                angleTangent = angleNormal - math.pi / 2
            angleTangent = principleRadianAngle(angleTangent)
            self.speed = math.fabs(self.speed * math.cos(angleTangent - self.angle) + ball2.speed * math.cos(
                angleTangent - ball2.angle))
            ball2.speed = math.fabs(math.sqrt(totalSpeedSquared - self.speed ** 2))
            self.angle = angleTangent
            ball2.angle = angleNormal
            self.updatePosition()
            ball2.updatePosition()
        # distance = math.sqrt((self.x - ball2.x) ** 2 + (self.y - ball2.y) ** 2)
        # if distance <= 2 * self.rad:
        #     self.collisionSpeedX = self.speed*math.cos(self.angle)+ball2.speed*math.cos(ball2.angle)
        #     self.collisionSpeedY = self.speed*math.sin(self.angle)+ball2.speed*math.sin(ball2.angle)
        #     cons = ({'type': 'ineq', 'fun': lambda x: (x[1]-ball2.speed)**2},
        #             {'type': 'ineq', 'fun': lambda x: (x[2]-self.angle)**2-0.00001},
        #             {'type': 'ineq', 'fun': lambda x: (self.speed-x[0])**2-1e-2},
        #             {'type': 'ineq', 'fun': lambda x: (self.speed-x[1])**2-1e-2},
        #             {'type': 'ineq', 'fun': lambda x: x[2]},
        #             {'type': 'ineq', 'fun': lambda x: math.pi/2-x[2]})
        #     s =opt.minimize(self.solveCollision, np.array([0,0,0]),method='COBYLA',constraints=cons,tol=1e-15)
        #     print(s.x)
        #     self.speed = s.x[0]
        #     self.angle = s.x[2]
        #     ball2.speed = s.x[1]
        #     ball2.angle = s.x[2] - math.pi/2

    def solveCollision(self, parameters):  # parameters = [finalSpeed1, finalSpeed2, finalAngle1]
        if parameters[0] == self.speed:
            return 1e7
        momentumXResidual = math.fabs(
            self.collisionSpeedX - parameters[0] * math.cos(parameters[2]) - parameters[1] * math.cos(
                parameters[2] - math.pi / 2))
        momentumYResidual = math.fabs(
            self.collisionSpeedY - parameters[0] * math.sin(parameters[2]) - parameters[1] * math.sin(
                parameters[2] - math.pi / 2))
        keResidual = math.fabs(
            self.collisionSpeedX ** 2 + self.collisionSpeedY ** 2 - parameters[0] ** 2 - parameters[1] ** 2)
        print(momentumXResidual, momentumYResidual, keResidual)
        return momentumXResidual ** 2 + momentumYResidual ** 2 + keResidual


class Stripes(Ball):

    def __init__(self, x, y):
        Ball.__init__(self, x, y)


class Solids(Ball):

    def __init__(self, x, y):
        Ball.__init__(self, x, y)


class BlackBall(Ball):

    def __init__(self, x, y):
        Ball.__init__(self, x, y)


def main():
    b = Ball(20, 0.8)
    c = Ball(20, 14.99)
    b.shoot(10, math.pi * 1 / 2)
    print("Initial Ball Speeds.")
    print(b.speed, b.angleDegree())
    print(c.speed, c.angleDegree())
    while math.sqrt((b.x - c.x) ** 2 + (b.y - c.y) ** 2) > 2 * b.rad:
        b.updatePosition()
    print("Before collision.")
    print(b.speed, b.angleDegree())
    print(c.speed, c.angleDegree())
    b.collide(c)
    print("After collision")
    print(b.speed, b.angleDegree())
    print(c.speed, c.angleDegree())


if __name__ == "__main__":
    main()
