from tkinter import *
import Ball
from Ball import principleRadianAngle, BALL_RADIUS
import Table
from Table import TABLE_HEIGHT, TABLE_WIDTH
from numpy import arange, sqrt, pi


def drawBalls(canvas, table):
    for i in arange(len(table.balls)):  # Every ball but white
        canvas.coords(str(i + 1), table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                      table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS))
    canvas.coords("w", table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
                  table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS))
    canvas.pack()


def shoot(table, power, angle):
    table.whiteBall.shoot(power, angle)
    while (any(ball.speed >= 0.08 for ball in table.balls) or table.whiteBall.speed > 0.08):
        table.checkCollisionWall(table.whiteBall)
        for i in arange(15):
            table.checkCollision2Balls(table.whiteBall, table.balls[i])
            table.checkCollisionWall(table.balls[i])
            for j in arange(i + 1, 15):
                table.checkCollision2Balls(table.balls[i], table.balls[j])

                # print(i,j)
            table.balls[i].updatePosition()
        table.whiteBall.updatePosition()

def main():
    table = Table.Table()
    gameGUI = Tk()
    canvas = Canvas(gameGUI, width=400, height=200, background="spring green")
    ballsCanvas = []
    # canvas.pack()

    for i in arange(len(table.balls)):
        if type(table.balls[i]) is Ball.Stripes:
            # print ("Stripes")
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   tag=str(i + 1), fill=table.balls[i].color, dash=(1, 4)))
        else:
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   tag=str(i + 1), fill=table.balls[i].color))  # add all Pool Balls
    ballsCanvas.append(
        canvas.create_oval(table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
                           table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS),
                           tag="w", fill="white"))  # add whiteBall
    canvas.pack()
    shoot(table, 5, 0)

    print("done")
    drawBalls(canvas, table)
    # ballsCanvas.append(  # testing for whiteball collision
    #     canvas.create_oval(table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
    #                        table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS),
    #                        tag="w2"))



    gameGUI.mainloop()


if __name__ == "__main__":
    main()
