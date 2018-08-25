from tkinter import *
import Ball
from Ball import principleRadianAngle, BALL_RADIUS
import Table
from Table import TABLE_HEIGHT, TABLE_WIDTH
from numpy import arange, sqrt


def main():
    table = Table.Table()
    gameGUI = Tk()
    canvas = Canvas(gameGUI, width=400, height=200, background="white")
    ballsCanvas = []
    # canvas.pack()

    for i in arange(len(table.balls)):
        ballsCanvas.append(
            canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                               table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                               tag=str(i + 1)))
    canvas.pack()
    table.balls[0].shoot(4, 0)
    while (any(ball.speed >= 0.08 for ball in table.balls)):
        for i in arange(15):
            for j in arange(i + 1, 15):
                table.checkCollision2Balls(table.balls[i], table.balls[j])
                # print(i,j)
            table.balls[i].updatePosition()
    print("done")
    for i in arange(len(table.balls)):
        canvas.coords(str(i + 1), table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                      table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS))
    canvas.pack()

    table.balls[0].shoot(2, 0.7)
    while (any(ball.speed >= 0.08 for ball in table.balls)):
        for i in arange(15):
            for j in arange(i + 1, 15):
                table.checkCollision2Balls(table.balls[i], table.balls[j])
                # print(i,j)
            table.balls[i].updatePosition()
    print("done")
    for i in arange(len(table.balls)):
        canvas.coords(str(i + 1), table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                      table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS))
    canvas.pack()

    gameGUI.mainloop()


if __name__ == "__main__":
    main()
