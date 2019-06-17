from tkinter import *
import Ball
from Ball import principleRadianAngle, BALL_RADIUS
import Table
from Table import TABLE_HEIGHT, TABLE_WIDTH
from numpy import arange, sqrt, pi, arctan2

table = Table.Table()
gameGUI = Tk()
canvas = Canvas(gameGUI, width=400, height=200, background="spring green")
ballsCanvas = []
ballcoords = []
spring_k = 0.02
shootCoords = []
poolStick = canvas.create_line(0, 0, 1, 1, fill="white", tag="stick")
timer = 0.0
timerDelta = 1/60


def drawStick(event):
    if len(shootCoords) > 0:
        canvas.itemconfig(poolStick, state="normal")
        canvas.coords("stick", shootCoords[0][0], shootCoords[0][1], event.x, event.y)

def shotClick(event):
    shootCoords.append([event.x, event.y])
    # print(event.x, event.y)


def shotRelease(event):
    shootCoords.append([event.x, event.y])
    # print(event.x, event.y)

    if (sqrt((shootCoords[0][1] - shootCoords[1][1]) ** 2 + (shootCoords[0][0] - shootCoords[1][0]) ** 2) > 10):
        ang = arctan2(-shootCoords[0][1] + shootCoords[1][1], shootCoords[0][0] - shootCoords[1][0])
        pow = spring_k / 2 * (
                    (shootCoords[0][1] - shootCoords[1][1]) ** 2 + (shootCoords[0][0] - shootCoords[1][0]) ** 2)
        shoot(min(pow, 20), ang)
        print(pow, ang * 180 / pi)
        gameGUI.after(int(0), animate)

    table.checkScratch()
    table.checkPlayer1Type()
    if table.whiteBall.pocketed == True:
        print("WB pocket")
        table.resetWhiteBall()
        ballcoords.append(["w", table.whiteBall.x, table.whiteBall.y])
        gameGUI.after(int(0), animate)
    shootCoords.clear()
    canvas.itemconfig(poolStick, state="hidden")

    print(table.blackBallSunk())

    if table.blackBallSunk() is True:
        print("Black Ball sunk")
        pocketBall("solid8")
        print("Player " + str(table.GameResult()) + " is the winner!")
        canvas.create_text(20, 100, anchor=W, font="Purisa",
                           text="Player " + str(table.GameResult()) + " is the winner!", state="normal", tag="result")

    table.switchTurn()
    canvas.itemconfig("turn", text="Player " + str(table.playerTurn) + " Turn")
    canvas.itemconfig("turn", state="normal")
    gameGUI.title("Player 1 is " + str(table.player1Type))
    # gameGUI.after(2000, lambda: canvas.itemconfig("turn", state="hidden"))


# def drawBalls():
#     for i in arange(len(table.balls)):  # Every ball but white
#         canvas.coords(str(i + 1), table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
#                       table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS))
#     canvas.coords("w", table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
#                   table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS))
#     canvas.pack()


def animate2():
    if len(ballcoords) == 0:
        return
    else:
        # print(ballcoords[0][0])
        numberToAnimate = 1  # stores coordinates for different balls to animate at the same time
        for i in arange(1, len(ballcoords)):
            brake = False  # to break out of loop
            for j in arange(i):
                if ballcoords[i][0] == ballcoords[j][0]:
                    brake = True
                    break
            if brake is True:
                break
            else:
                numberToAnimate += 1

        for k in arange(numberToAnimate):
            canvas.coords(ballcoords[k][0], ballcoords[k][1] - BALL_RADIUS,
                          TABLE_HEIGHT - (ballcoords[k][2] + BALL_RADIUS),
                          ballcoords[k][1] + BALL_RADIUS, TABLE_HEIGHT - (ballcoords[k][2] - BALL_RADIUS))
            for i in arange(len(table.pockets)):
                if ballcoords[k][0] != "w" and (ballcoords[k][1] == -10 or ballcoords[k][2] == -10):
                    pocketBall(ballcoords[k][0])
                if sqrt((ballcoords[k][1] - table.pockets[i][0]) ** 2 + (
                        ballcoords[k][2] - table.pockets[i][1]) ** 2) < 2 * BALL_RADIUS:
                    pocketBall(ballcoords[k][0])

        for k in arange(numberToAnimate):
            ballcoords.pop(0)
        gameGUI.after(int(2), animate)
        # print(table.solidsPocketedLastTurn)
        # print(table.stripesPocketedLastTurn)

def animate():
    if len(ballcoords) == 0:
        return
    else:
        global timer
        timer+=timerDelta

        while(ballcoords[0][3]<timer):
            canvas.coords(ballcoords[0][0], ballcoords[0][1] - BALL_RADIUS,
                          TABLE_HEIGHT - (ballcoords[0][2] + BALL_RADIUS),
                          ballcoords[0][1] + BALL_RADIUS, TABLE_HEIGHT - (ballcoords[0][2] - BALL_RADIUS))
            ballcoords.pop(0)
            for i in arange(len(table.pockets)):
                if ballcoords[0][0] != "w" and (ballcoords[0][1] == -10 or ballcoords[0][2] == -10):
                    pocketBall(ballcoords[0][0])
                if sqrt((ballcoords[0][1] - table.pockets[i][0]) ** 2 + (
                        ballcoords[0][2] - table.pockets[i][1]) ** 2) < 2 * BALL_RADIUS:
                    pocketBall(ballcoords[0][0])

        gameGUI.after(int(2), animate)

def addCoords(coords, ballData):
    index = len(coords)-1
    if index==-1:
        coords.append(ballData)
        return
    while(index>=0):
        if ballData[3]<coords[index][3]:
            index-=1
        else:
            coords.insert(index+1,ballData)
            break
    if index==-1:
        coords.insert(index+1,ballData)


def pocketBall(tag):
    canvas.itemconfig(tag, state="hidden")

def shoot(power, angle):
    table.whiteBall.shoot(power, angle)
    global timer
    while (any(ball.speed >= 0.08 for ball in table.balls) or table.whiteBall.speed > 0.08):
        table.checkCollisionWall(table.whiteBall)
        for i in arange(15):
            table.checkCollision2Balls(table.whiteBall, table.balls[i])
            table.checkCollisionWall(table.balls[i])
            for j in arange(i + 1, 15):
                table.checkCollision2Balls(table.balls[i], table.balls[j])

                # print(i,j)
            table.balls[i].updatePosition()
            table.checkPocketed(table.balls[i])
            if table.balls[i].pocketed is True and type(table.balls[i]) is (Ball.Solids or Ball.BlackBall):
                addCoords(ballcoords,["solid" + str(table.balls[i].id), -10, -10,table.balls[i].timer])
            elif table.balls[i].pocketed is True:
                addCoords(ballcoords,["stripe" + str(table.balls[i].id), -10, -10,table.balls[i].timer])

                # if type(table.balls[i]) is (Ball.Solids or Ball.BlackBall):
            #     pocketBall("solid" + str(table.balls[i].id))
            # else:
            #     pocketBall("stripe" + str(table.balls[i].id))

            if (table.balls[i].speed > 0.08 and timer>table.balls[i].timer):
                if type(table.balls[i]) is Ball.Solids:
                    addCoords(ballcoords,["solid" + str(table.balls[i].id), table.balls[i].x, table.balls[i].y,table.balls[i].timer])
                elif type(table.balls[i]) is Ball.BlackBall:
                    addCoords(ballcoords,["solid" + str(table.balls[i].id), table.balls[i].x, table.balls[i].y,table.balls[i].timer])
                else:
                    addCoords(ballcoords,["stripe" + str(table.balls[i].id), table.balls[i].x, table.balls[i].y,table.balls[i].timer])
            # canvas.move(str(i+1),table.balls[i].speedX()*table.balls[i].timeDelta,(-1)*table.balls[i].speedY()*table.balls[i].timeDelta)
        table.whiteBall.updatePosition()
        table.checkPocketed(table.whiteBall)
        # pocketBall(table.whiteBall,"w")
        if (table.whiteBall.speed > 0.08 and timer>table.whiteBall.timer):
            addCoords(ballcoords,["w", table.whiteBall.x, table.whiteBall.y,table.whiteBall.timer])
        if (table.whiteBall.pocketed == True):
            addCoords(ballcoords,["w", -10, -10,table.whiteBall.timer])
        timer+=1/59

    addCoords(ballcoords,["w", table.whiteBall.x, table.whiteBall.y,table.whiteBall.timer])
    timer = 0
    for ball in [*table.balls,table.whiteBall]:
        ball.timer=0
    




def shootClickWhiteBall(event):
    shoot(20, 0)
    gameGUI.after(int(0), animate)
    # drawBalls()

def main():
    # Create ball objects and tags
    global timer
    timer = 0
    for i in arange(len(table.balls)):
        if type(table.balls[i]) is Ball.Stripes:
            # print ("Stripes")
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   tag="stripe" + str(table.balls[i].id), fill=table.balls[i].color, outline="white"))
            # print(table.balls[i].x-BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y, # make stripes
            #             table.balls[i].x+BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y)
            # canvas.create_line(table.balls[i].x-BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y, # make stripes
            #                    table.balls[i].x+BALL_RADIUS,TABLE_HEIGHT - table.balls[i].y,
            #                    fill = "white", width = 2, tag = "s"+str(i+1))
        else:
            ballsCanvas.append(
                canvas.create_oval(table.balls[i].x - BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y + BALL_RADIUS),
                                   table.balls[i].x + BALL_RADIUS, TABLE_HEIGHT - (table.balls[i].y - BALL_RADIUS),
                                   tag="solid" + str(table.balls[i].id),
                                   fill=table.balls[i].color))  # add all Pool Balls
    ballsCanvas.append(
        canvas.create_oval(table.whiteBall.x - BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y + BALL_RADIUS),
                           table.whiteBall.x + BALL_RADIUS, TABLE_HEIGHT - (table.whiteBall.y - BALL_RADIUS),
                           tag="w", fill="white"))  # add whiteBall

    # Create pockets
    for i in arange(len(table.pockets)):
        canvas.create_oval(table.pockets[i][0] - 2 * BALL_RADIUS,
                           TABLE_HEIGHT - (table.pockets[i][1] + 2 * BALL_RADIUS),
                           table.pockets[i][0] + 2 * BALL_RADIUS,
                           TABLE_HEIGHT - (table.pockets[i][1] - 2 * BALL_RADIUS),
                           tag="pocket" + str(i + 1),
                           fill="black")

    # Result box
    canvas.create_text(20, 30, anchor=W, font="Purisa",
                       text="Player 1 Turn", state="normal", tag="turn")

        # Add events
    canvas.tag_bind("w", "<Double-1>", shootClickWhiteBall)
    canvas.tag_bind("w", "<Button-1>", shotClick)
    canvas.tag_bind("w", "<ButtonRelease-1>", shotRelease)
    canvas.tag_bind("w", "<Motion>", drawStick)

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
