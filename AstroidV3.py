from tkinter import Tk, Canvas, PhotoImage, Button, ALL, Entry, StringVar
import pandas
import random
import time
import sys
from os import path

Playername = input("Please enter a player name: ")


def windowDimensions(w, h):
    global window, sw, sh
    window = Tk()
# Creates window labelled astroid shooter
    window.title("Astroid")
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw/2) - (w/2)
    y = (sh/2) - (h/2)
# Places window at the cenre of the screen
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))
    return window


# Displays the instructions file to the user explaining how to play.
# User can use buttons to navigate between pages.
def Instructions():
    canvasG.delete(ALL)
    InstructionsButton.place(x=-10000, y=0)
    PlayGameButton.place(x=330, y=605)
    LeaderBoardButton.place(x=100, y=890)
    LoadButton.place(x=250, y=730)
    f = open("Instructions.txt", "r")
    InstTxt = f.read()
    f.close()
    canvasG.create_text(600, 320, fill="White", font="Arial 32  bold",
                        text=InstTxt)


# Displays LeaderBoard to the user
# User can use buttons to navigate between pages.
def LeaderBoard():
    canvasG.delete(ALL)
    LeaderBoardButton.place(x=-10000, y=800)
    InstructionsButton.place(x=215, y=900)
    LoadButton.place(x=250, y=730)
    PlayGameButton.place(x=330, y=595)
    fn = open("Names.txt", "r")
    namelist = [line.rstrip('\n') for line in fn]
    fn.close()
    fs = open("Scores.txt", "r")
    scorelist = [line.rstrip('\n') for line in fs]
    data = pandas.DataFrame({'Name': namelist,
                            'Score': scorelist})
    data = data.sort_values(by='Score', ascending=False)
# Displays scores in a table format and then sorts in descending order
    canvasG.create_text(600, 100, fill="White", font="Arial 40 bold",
                        text="LeaderBoard")
    canvasG.create_text(600, 200, fill="White", font="Arial 40 bold",
                        text=data)


# This function intitates the game by setting userstate to play
def playgame():
    global playerAvatar, userstate, User, startTime, score_display
    canvasG.delete(ALL)
    LeaderBoardButton.destroy()
    InstructionsButton.destroy()
    PlayGameButton.destroy()
    LoadButton.destroy()

    userstate = "Play"
    gameover = "no"
# Creates the users sprite
    playerAvatar = PhotoImage(file="UserSprite.png")
    User = canvasG.create_image(600, 600, image=playerAvatar)
    score_display = canvasG.create_text(60, 15, fill="White",
                                        font="Arial 20 bold", text="Score: ")


# changes the direction variable to the chosen direction.
def leftKey(event):
    global direction
    direction = "left"


def rightKey(event):
    global direction
    direction = "right"


def upKey(event):
    global direction
    direction = "up"


def downKey(event):
    global direction
    direction = "down"


# Moves the Users sprite depending on the direction variable chosen.
def Moveuser():
    global direction
    if userstate == "Play" and paused == "false" and gameover != "yes":
        # And statement stops user from moving off the screen.
        if direction == "left" and canvasG.coords(User)[0] >= 40:
            canvasG.move(User, -25, 0)
            direction = ""
        elif direction == "right" and canvasG.coords(User)[0] <= (width-30):
            canvasG.move(User, 25, 0)
            direction = ""
        elif direction == "up" and canvasG.coords(User)[1] >= 20:
            canvasG.move(User, 0, -10)
            direction = ""
        elif direction == "down" and canvasG.coords(User)[1] <= (height-130):
            canvasG.move(User, 0, 10)
            direction = ""
    window.after(8, Moveuser)


# Creates astroids at random positions of x on the canvas and adds them to
# astroid field list
def astroidField1():
    if userstate == "Play" and paused == "false" and gameover != "yes":
        randcoordsX = random.randint(40, width-30)
        field.append(canvasG.create_oval(randcoordsX, 0, (randcoordsX + 100),
                                         100, outline="white", fill="black"))
    canvasG.after(2000, astroidField1)


def astroidField2():
    if userstate == "Play" and paused == "false" and gameover != "yes":
        if score > 50:
            randcoordsX1 = random.randint(40, width-30)
            field.append(canvasG.create_oval(randcoordsX1, 0,
                                             (randcoordsX1 + 150), 150,
                                             outline="white", fill="black"))
    canvasG.after(random.randint(1300, 1800), astroidField2)


def astroidField3():
    if userstate == "Play" and paused == "false" and gameover != "yes":
        if score > 100:
            randcoordsX2 = random.randint(40, width-30)
            field.append(canvasG.create_oval(randcoordsX2, 0,
                                             (randcoordsX2 + 200),
                                             200, outline="white",
                                             fill="black"))
    canvasG.after(random.randint(1200, 1600), astroidField3)


# Moves the all the astroids in the field by the current speed value
def astroidFieldMove():
    if userstate == "Play" and paused == "false" and gameover != "yes":
        for x in field:
            canvasG.move(x, 0, speed)
            if canvasG.bbox(x)[1] >= 1000:
                canvasG.delete(x)
                field.remove(x)
    window.after(50, astroidFieldMove)


# Increases Game difficulty by incrementally increasing the speed of the field
def Fieldspeed():
    global speed
    if userstate == "Play" and paused == "false":
        if score > 150:
            speed += 1
    window.after(15000, Fieldspeed)


def displayScore():
    if userstate == "Play" and paused == "false":
        global score
        score_txt = "Score: " + str(score)
        canvasG.itemconfig(score_display, text=score_txt)
    window.after(10, displayScore)


def scorer():
    global score
    if userstate == "Play" and paused != "true":
        score += 10
    window.after(10000, scorer)


def collisionUser():
    global cheatcode, finalscore, gameover
    if userstate == "Play" and paused == "false" and cheatcode != "Active":
        # Checks if users coordinates are in the bbox of any of the
        # active astroids in the field if True end game is triggered
        userbboxX = list(range(canvasG.bbox(User)[0], canvasG.bbox(User)[2]))
        userbboxY = list(range(canvasG.bbox(User)[1], canvasG.bbox(User)[3]))
        for x in userbboxX:
            for y in field:
                if x in range(canvasG.bbox(y)[0], canvasG.bbox(y)[2]):
                    for z in userbboxY:
                        if z in range(canvasG.bbox(y)[1], canvasG.bbox(y)[3]):
                            gameover = "yes"
                            finalscore = score
                            # stores the users final score at time of collision
                            time.sleep(0.5)
                            canvasG.delete(*canvasG.find_all())
                            endGame()
    window.after(1, collisionUser)


def endGame():
    # Changes the canvas to the end game screen
    canvasG.create_text(600, 200, fill="White", font="Arial 40 bold",
                        text=("Game Over YOU LOSE!!!"))
    canvasG.config(bg="black")
    canvasG.create_text(600, 200, fill="White", font="Arial 40 bold",
                        text=('\n\n\n' + Playername +
                              " Score: " + str(finalscore)))
    # Adds Players name and score to leaderboard
    fn = open("Names.txt", "a")
    fn.write('\n' + Playername)
    fn.close()
    fs = open("Scores.txt", "a")
    fs.write('\n' + str(finalscore))
    fs.close()
    # Displays LeaderBoard in with scores displayed in descending order
    fn = open("Names.txt", "r")
    namelist = [line.rstrip('\n') for line in fn]
    fn.close()
    fs = open("Scores.txt", "r")
    scorelist = [line.rstrip('\n') for line in fs]
    data = pandas.DataFrame({'Name': namelist,
                            'Score': scorelist})
    data = data.sort_values(by='Score', ascending=False)
    # Displays scores in a table format and then sorts in descending order.
    canvasG.create_text(600, 300, fill="White", font="Arial 40 bold",
                        text="LeaderBoard")
    canvasG.create_text(600, 400, fill="White", font="Arial 40 bold",
                        text=data)
# Buttons allow the user to restart the game or quit the game.
    PlayAgain = Button(window, image=buttonPlayAgain,
                       command=lambda: restartProgram())
    PlayAgain.place(x=360, y=800)
    QuitGame = Button(window, image=quitgameimg, command=lambda: sys.exit())
    QuitGame.place(x=300, y=950)


def fire(event):
    global shotNo
    # Allows user to fire 1 shots by pressing space bar.
    if userstate == "Play" and paused == "false" and gameover != "yes":
        x1 = (canvasG.bbox(User)[0] + canvasG.bbox(User)[2])/2
        y1 = canvasG.bbox(User)[1]
        if len(shots) < shotNo:
            shots.append(canvasG.create_rectangle((x1 - 3), (y1 + 15),
                                                  (x1 + 1), y1, fill="white"))


# Function that moves the active shots
def shotmove():
    if userstate == "Play" and paused == "false" and gameover != "yes":
        for x in shots:
            canvasG.move(x, 0, -speed*2)
            if canvasG.bbox(x)[1] <= 0:
                canvasG.delete(x)
                shots.remove(x)
    window.after(30, shotmove)


# Collision detection for shots and astroids
# If the bbox of the 2 objects intersect both objects are deleted.
def collisionShot():
    global score
    if len(shots) > 0:
        for x in shots:
            for y in field:
                shotsXcoords = range(canvasG.bbox(x)[0], canvasG.bbox(x)[2])
                shotsYcoord = canvasG.bbox(x)[1]
                astroidXcoords = range(canvasG.bbox(y)[0], canvasG.bbox(y)[2])
                astroidYcoords = range(canvasG.bbox(y)[1], canvasG.bbox(y)[3])
                for z in shotsXcoords:
                    if z in astroidXcoords:
                        if shotsYcoord in astroidYcoords:
                            canvasG.move(x, 0, -10000000)
                            canvasG.move(y, 0, 10000000)
                            score += 1
    window.after(100, collisionShot)


def pause(event):
    # If <p> is pressed the game is paused then unpauses game if presssed again
    # Button enables user to save and quit game.
    global pausecount, paused, countdown3, countdown2, countdown1, saveAndQuit
    pausecount += 1
    print(pausecount)
    if pausecount % 2 == 1:
        paused = "true"
        print(paused)
        saveAndQuit = Button(window, image=saveandquitgameimg,
                             command=lambda: [saveGame(), sys.exit()])
        saveAndQuit.place(x=250, y=900)
    else:
        time.sleep(1)
        saveAndQuit.destroy()
        paused = "false"


# Saves the users current setings in a text file to reused later on.
def saveGame():
    global Playername, score, speed
    f = open(str(Playername), "w")
    f.write(str(Playername) + "\n" + str(score) + "\n" + str(speed))
    f.close()


# Function resatrts the program
def restartProgram():
    R = sys.executable
    os.execl(R, R, * sys.argv)


# Boss key function triggered by presing b
# Displays a work like image on the canvas.
# Pressing b a second time turns boss key off and resumes game.
def bossKey(event):
    global pausecount, paused, bk
    pausecount += 1
    if pausecount % 2 == 1:
        paused = "true"
        window.title("Outlook")
        window.geometry("1375x800")
        bk = canvasG.create_image(600, 400, image=bosskeyimg)
        canvasG.config(width=1540, height=800)
    else:
        window.title("Astroid")
        window.geometry("1200x1200")
        canvasG.delete(bk)
        canvasG.config(width=width, height=height)
        paused = "false"


# First key to intiate cheat code sequence
def cheatcodeImmuneC1(event):
    global cheat
    if userstate == "Play" and paused == "false" and gameover != "yes":
        cheatcodetimer()
        if cheat == 0:
            cheat += 1
            print(cheat)
        else:
            cheat = 0
            print(cheat)


def cheatcodeImmuneC2(event):
    global cheat
    if cheat == 1:
        cheat += 1
        print(cheat)
    else:
        cheat = 0
        print(cheat)


def cheatcodeImmuneC3(event):
    global cheat
    if cheat == 2:
        cheat += 1
        print(cheat)
    else:
        cheat = 0
        print(cheat)


def cheatcodeImmuneC4(event):
    global cheat
    if cheat == 3:
        cheat += 1
        print(cheat)
    else:
        cheat = 0
        print(cheat)


def cheatcodeImmuneC5(event):
    global cheat, cheatcode
    if cheat == 4:
        cheat += 1
        print(cheat)
        cheatcode = "Active"
        print(cheatcode)
        cheatcodeActivator()
    else:
        cheat = 0
        print(cheat)


# Creates a timer. cheat code must be entered within 7 seconds
def cheatcodetimer():
    global cheat
    cheat = 0
    multishot = 0
    print("cheat reset")
    window.after(7000, cheatcodetimer)


# Activates cheat codes and de activates after 20 seconds
# activates codes by changeing the variables
def cheatcodeActivator():
    global immunitycount, cheatcode, shotNo, doubleshotcount
    if userstate == "Play" and paused == "false" and gameover != "yes":
        if cheatcode == "Active":
            immunitycount += 1
        if immunitycount == 2:
            cheatcode = "Disabled"
            print(cheatcode)
        if shotNo == 2:
            doubleshotcount += 1
        if doubleshotcount == 2:
            shotNo = 1
            print("shot no. reset")
        window.after(20000, cheatcodeActivator)


# First key to intiate cheay code sequence
def cheatcodeMultishotC1(event):
    global multishot
    if userstate == "Play" and paused == "false" and gameover != "yes":
        cheatcodetimer()
        if multishot == 0:
            multishot += 1
            print(multishot)
        else:
            multishot = 0
            print(multishot)


def cheatcodeMultishotC2(event):
    global multishot
    if multishot == 1:
        multishot += 1
        print(multishot)
    else:
        multishot = 0
        print(multishot)


def cheatcodeMultishotC3(event):
    global multishot
    if multishot == 2:
        multishot += 1
        print(multishot)
    else:
        multishot = 0
        print(multishot)


def cheatcodeMultishotC4(event):
    global multishot
    if multishot == 3:
        multishot += 1
        print(multishot)
    else:
        multishot = 0
        print(multishot)


def cheatcodeMultishotC5(event):
    global multishot, shotNo
    if multishot == 4:
        multishot += 1
        print(multishot)
        shotNo = 2
        print(shotNo)
        cheatcodeActivator()
    else:
        multishot = 0
        print(multishot)


# Creates a second window to allow user to enter their previous Playername.
# button stores text box entry as playername.
def gameloader():
    global Playername, name, canvasE, entrybox, window2
    window2 = Tk()
    window2.geometry("600x300+300+300")
    window2.title("Load Game")
    canvasE = Canvas(window2, bg="black", width=600, height=300)
    canvasE.pack()
    s = "Please enter your Playername \n        from the previous game"
    displaytxt = canvasE.create_text(300, 50, fill="white",
                                     font="Arial 20  bold",  text=s)
    entrybox = Entry(canvasE, width=30)
    entrybox.place(x=200, y=100)
    LoadButton2 = Button(window2, text="load game",
                         command=lambda: restartGame())
    LoadButton2.place(x=250, y=150)
    canvasE.mainloop()


# Checks if player has a saved file if so game restarts.
# Changes the initial settings to the users previous ones.
# Thus reloading the game.
def restartGame():
    global Playername, canvasE, entrybox, score, speed, window2
    Playername = entrybox.get()
    canvasE.create_text(300, 250, fill="Red", font="Arial 20  bold",
                        text="Player name is not found. Enter again")
    while path.exists(str(Playername)):
        sGame = open(str(Playername), "r")
        Playersettings = [line.rstrip('\n') for line in sGame]
        score = int(Playersettings[1])
        speed = int(Playersettings[2])
        sGame.close()
        window2.destroy()
        playgame()
        break


# Pre-game variables
userstate = "Active"
paused = "false"
direction = "up"
gameover = "no"
again = "not yet"
cheatcode = "Disabled"
width = 1200
height = 1200
speed = 10
pausecount = 0
score = 0
shotNo = 1
cheat = 0
immunitycount = 0
doubleshotcount = 0
multishot = 0

# Arrays which contain the dynamic shape elements of the game
field = []
shots = []


windowDimensions(width, height)
# Retrieves all the images used storing them in variables as follows:
canvasG = Canvas(window, bg="black", width=width, height=height)
buttonInst = PhotoImage(file="ButttonInstructions.png")
buttonPlayGame = PhotoImage(file="ButtonPlayGame.png")
buttonLeaderboard = PhotoImage(file="ButttonLeaderBoard.png")
buttonPlayAgain = PhotoImage(file="ButttonPlayAgain.png")
bosskeyimg = PhotoImage(file="BossKeyImage.png")
quitgameimg = PhotoImage(file="ButtonQuitGame.png")
saveandquitgameimg = PhotoImage(file="ButttonSaveAndQuit.png")
loadgameimg = PhotoImage(file="ButttonLoadGame.png")

# Creates title page design.
canvasG.create_oval(600, 500, 1500, 1400, outline="white", fill="black")
canvasG.create_oval(50, 500, 450, 900, outline="white", fill="black")
canvasG.create_oval(250, 30, 650, 430, outline="white", fill="black")
title = canvasG.create_text(600, 200, fill="White", font="Arial 42  bold",
                            text="Astroid")

# Creates the buttons on the menu screen
buttonInst = PhotoImage(file="ButttonInstructions.png")
buttonPlayGame = PhotoImage(file="ButtonPlayGame.png")
buttonLeaderboard = PhotoImage(file="ButttonLeaderBoard.png")
PlayGameButton = Button(window, image=buttonPlayGame,
                        command=lambda: playgame())
PlayGameButton.place(x=330, y=360)
InstructionsButton = Button(window, image=buttonInst,
                            command=lambda: Instructions())
InstructionsButton.place(x=215, y=670)
LeaderBoardButton = Button(window, image=buttonLeaderboard,
                           command=lambda: LeaderBoard())
LeaderBoardButton.place(x=120, y=850)
LoadButton = Button(window, image=loadgameimg,
                    command=lambda: gameloader())
LoadButton.place(x=250, y=500)

# Binds the event of pressing an arrow key
# with a function that causes an action
canvasG.bind("<KeyPress-Left>", leftKey)
canvasG.bind("<KeyPress-Right>", rightKey)
canvasG.bind("<KeyPress-Up>", upKey)
canvasG.bind("<KeyPress-Down>", downKey)
canvasG.bind("<space>", fire)
canvasG.bind("<p>", pause)
canvasG.bind("<b>", bossKey)

# Cheatcode key binds
canvasG.bind("<c>", cheatcodeImmuneC1)
canvasG.bind("<h>", cheatcodeImmuneC2)
canvasG.bind("<e>", cheatcodeImmuneC3)
canvasG.bind("<a>", cheatcodeImmuneC4)
canvasG.bind("<t>", cheatcodeImmuneC5)

canvasG.bind("<d>", cheatcodeMultishotC1)
canvasG.bind("<o>", cheatcodeMultishotC2)
canvasG.bind("<u>", cheatcodeMultishotC3)
canvasG.bind("<v>", cheatcodeMultishotC4)
canvasG.bind("<l>", cheatcodeMultishotC5)

# calls the functions of the game
canvasG.focus_set()
canvasG.pack()
displayScore()
Moveuser()
Fieldspeed()
astroidField1()
astroidField2()
astroidField3()
astroidFieldMove()
shotmove()
collisionUser()
collisionShot()
scorer()
window.mainloop()
