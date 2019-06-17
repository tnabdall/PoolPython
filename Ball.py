import math

BALL_RADIUS = 8.0  # m

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
    id = 0
    rad = BALL_RADIUS  # m
    speed = 0.0  # m/s
    angle = 0.0  # rads
    pocketed = False
    timeDelta = 1/60  # s
    friction = 0.3  # (m/s^2)
    color = ""
    timer = 0.0 # s, for controlling animations

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id  # 1-7 are stripes, 8-14 are solids (1-7), blackball is 15

    def determineColor(self):
        if self.id == -1:
            self.color = "white"
        elif self.id == 1:
            self.color = "yellow"
        elif self.id == 2:
            self.color = "blue"
        elif self.id == 3:
            self.color = "red"
        elif self.id == 4:
            self.color = "purple"
        elif self.id == 5:
            self.color = "orange"
        elif self.id == 6:
            self.color = "green"
        elif self.id == 7:
            self.color = "red4"
        pass  # based on ID

    def speedX(self):
        return math.cos(self.angle) * self.speed

    def speedY(self):
        return math.sin(self.angle) * self.speed

    def distance(self, ball2):
        return math.sqrt((self.x - ball2.x) ** 2 + (self.y - ball2.y) ** 2)

    def angleDegree(self):
        return self.angle * 180 / math.pi



    def updatePosition(self):
        if self.speed > 0.02:
            self.x = self.x + self.speed * math.cos(self.angle) * self.timeDelta
            self.y = self.y + self.speed * math.sin(self.angle) * self.timeDelta
            self.speed = self.speed - self.friction * self.timeDelta
            self.timer += self.timeDelta
        else:
            self.speed = 0
            self.timer+=self.timeDelta

class Stripes(Ball):

    def __init__(self, x, y, id):
        Ball.__init__(self, x, y, id)
        self.determineColor()


class Solids(Ball):

    def __init__(self, x, y, id):
        Ball.__init__(self, x, y, id -7)
        self.determineColor()


class BlackBall(Ball):

    def __init__(self, x, y):
        Ball.__init__(self, x, y, 8)
        self.color = "black"

    def __init__(self, x, y, id):
        Ball.__init__(self, x, y, 8)
        self.color = "black"


class WhiteBall(Ball):

    def __init__(self, x, y):
        Ball.__init__(self, x, y, -1)
        self.color = "white"
        self.timer = 0.0

    def shoot(self, power,
              angle):  # power in m/s converted from N because all mass is the same, angle in radians starting from east 0 rads
        self.speed = power
        self.angle = angle

def main():
    b = WhiteBall(20, 0.8, 1)
    c = Ball(20, 14.99,2)
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
