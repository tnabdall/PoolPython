from tkinter import *
import Ball
from Ball import principleRadianAngle, BALL_RADIUS
import Table
from Table import TABLE_HEIGHT, TABLE_WIDTH
from numpy import arange, sqrt, pi

table = Table.Table()
gameGUI = Tk()
canvas = Canvas(gameGUI, width=400, height=200, background="spring green")
ballsCanvas = []
ballcoords = []

def drawBalls():
    for i in arange(len(table.balls)):  # Every ball but white
        canvas.coords(str(i + 1), table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                      table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS))
    canvas.coords("w", table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
                  table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS))
    canvas.pack()


def animate():
    if len(ballcoords) == 0:
        return
    else:
        if ballcoords[0][0] == -1:
            canvas.coords("w", ballcoords[0][1] - BALL_RADIUS, TABLE_HEIGHT - (ballcoords[0][2] - BALL_RADIUS),
                          ballcoords[0][1] + BALL_RADIUS, TABLE_HEIGHT - (ballcoords[0][2] + BALL_RADIUS))
        else:
            canvas.coords(str(ballcoords[0][0] + 1), ballcoords[0][1] - BALL_RADIUS,
                          TABLE_HEIGHT - (ballcoords[0][2] - BALL_RADIUS),
                          ballcoords[0][1] + BALL_RADIUS, TABLE_HEIGHT - (ballcoords[0][2] + BALL_RADIUS))
        ballcoords.pop(0)
    gameGUI.after(int(5), animate)

def shoot(power, angle):
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
            if (table.balls[i].speed > 0.08):
                ballcoords.append([i, table.balls[i].x, table.balls[i].y])
            # canvas.move(str(i+1),table.balls[i].speedX()*table.balls[i].timeDelta,(-1)*table.balls[i].speedY()*table.balls[i].timeDelta)
        table.whiteBall.updatePosition()
        if (table.whiteBall.speed > 0.08):
            ballcoords.append([-1, table.whiteBall.x, table.whiteBall.y])




def shootClickWhiteBall(event):
    shoot(20, 0)
    gameGUI.after(int(0), animate)
    # drawBalls()

def main():

    for i in arange(len(table.balls)):
        if type(table.balls[i]) is Ball.Stripes:
            # print ("Stripes")
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   tag=str(i + 1), fill=table.balls[i].color, dash=(1, 4)))
            # print(table.balls[i].x-BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y, # make stripes
            #             table.balls[i].x+BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y)
            # canvas.create_line(table.balls[i].x-BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y, # make stripes
            #                    table.balls[i].x+BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y,
            #                    fill = "white", width = 2, tag = "s"+str(i+1))
        else:
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   tag=str(i + 1), fill=table.balls[i].color))  # add all Pool Balls
    ballsCanvas.append(
        canvas.create_oval(table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
                           table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS),
                           tag="w", fill="white"))  # add whiteBall

    canvas.tag_bind("w", "<Double-1>", shootClickWhiteBall)

    canvas.pack()

    print("done")
    # drawBalls()
    # ballsCanvas.append(  # testing for whiteball collision
    #     canvas.create_oval(table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
    #                        table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS),
    #                        tag="w2"))



    gameGUI.mainloop()


if __name__ == "__main__":
    main()
