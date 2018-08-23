import numpy as np
import Ball
from Ball import BALL_RADIUS, Stripes, Solids, BlackBall

TABLE_WIDTH = 400
TABLE_HEIGHT = 200


def setRandomBalls():
    width = TABLE_WIDTH
    height = TABLE_HEIGHT
    firstPos = [250 / 400 * TABLE_WIDTH, 100 / 200 * TABLE_HEIGHT]  # first ball standardized by table dimensions
    spacing = 0.05 * BALL_RADIUS  # times the Radius, vertical spacing between balls
    positions = []
    positions.append(firstPos)  # first column
    positions.append(
        [firstPos[0] + BALL_RADIUS, firstPos[1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])  # second column
    positions.append([firstPos[0] + BALL_RADIUS, firstPos[1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[1][0] + BALL_RADIUS,
                      positions[1][1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])  # third column
    positions.append([positions[1][0] + BALL_RADIUS, positions[1][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[1][0] + BALL_RADIUS, positions[2][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[3][0] + BALL_RADIUS,
                      positions[3][1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])  # fourth column
    positions.append([positions[3][0] + BALL_RADIUS, positions[3][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[3][0] + BALL_RADIUS, positions[5][1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[3][0] + BALL_RADIUS, positions[5][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[6][0] + BALL_RADIUS,
                      positions[6][1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])  # fifth column
    positions.append([positions[6][0] + BALL_RADIUS, positions[6][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[6][0] + BALL_RADIUS, positions[8][1] + 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[6][0] + BALL_RADIUS, positions[8][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])
    positions.append([positions[6][0] + BALL_RADIUS, positions[9][1] - 2 * BALL_RADIUS * np.sin(np.pi / 3) + spacing])

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


def main():
    t = Table()
    for i in np.arange(15):
        print(t.balls[i], t.balls[i].x, t.balls[i].y, t.balls[i].id)

    t.balls[0].shoot(10, 0)

    while (any(ball.speed >= 0.02 for ball in t.balls)):
        for i in np.arange(15):
            for j in np.arange(i + 1, 15):
                t.balls[i].collide(t.balls[j])

    print("\n")

    for i in np.arange(15):
        # print(type(t.balls[i]) is Ball.Stripes) # checks to see if stripes
        print(t.balls[i], t.balls[i].x, t.balls[i].y, t.balls[i].id)


if __name__ == "__main__":
    main()
