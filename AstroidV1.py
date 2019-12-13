from tkinter import Tk, Canvas, PhotoImage
import time
import random
import pandas
Playername = input("Please enter a Name: ")
def windowDimensions(w,h):
    global window, sw, sh
    window = Tk()#Creates window labelled astroid shooter
    window.title("Astroid")
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = (sw/2) - (w/2)
    y = (sh/2) - (h/2)
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))#Places window at the cenre of the screen
    return window
#changes the direction variable to the chosen direction.
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
#Moves the Users sprite depending on the direction variable chosen.
def Moveuser():
    global direction
    if userstate != "Game Over" and paused == "false" :
    #And statement stops user from moving off the screen.
        if direction == "left" and canvasG.coords(User)[0]>= 40 :
            canvasG.move(User, -25, 0)
            direction = ""
        elif direction == "right" and canvasG.coords(User)[0]<= (width-30):
            canvasG.move(User, 25, 0)
            direction = ""
        elif direction == "up" and canvasG.coords(User)[1]>= 20:
            canvasG.move(User, 0, -10)
            direction = ""
        elif direction == "down" and canvasG.coords(User)[1] <= (height-130):
            canvasG.move(User, 0, 10)
            direction = ""

    window.after(8, Moveuser)
#Creates astroids at random positions of x on the canvas and adds them to astroid field list
def astroidField1():
    if userstate != "Game Over" and paused == "false" :
        randcoordsX = random.randint(40,width-30)
        field.append(canvasG.create_oval(randcoordsX , 0, (randcoordsX + 100), 100, outline="white", fill="black"))
    canvasG.after(2000, astroidField1)
def astroidField2():
    if userstate != "Game Over" and paused == "false" :
        if score > 50:
            randcoordsX1 = random.randint(40,width-30)
            field.append(canvasG.create_oval(randcoordsX1 , 0, (randcoordsX1 + 150), 150, outline="white", fill="black"))
    canvasG.after(random.randint(1300,1800), astroidField2)
def astroidField3():
    if userstate != "Game Over" and paused == "false" :
        if score > 100:
            randcoordsX2 = random.randint(40,width-30)
            field.append(canvasG.create_oval(randcoordsX2 , 0, (randcoordsX2 + 200), 200, outline="white", fill="black"))
    canvasG.after(random.randint(1200,1600), astroidField3)
#Moves the all the astroids in the field by the current speed value
def astroidFieldMove():
    if userstate != "Game Over" and paused == "false" :
        for x in field:
            canvasG.move(x, 0 ,speed )
            if canvasG.bbox(x)[1] >= 1000:
                canvasG.delete(x)
                field.remove(x)
    window.after(50, astroidFieldMove)
#Increases Game difficulty by incrementally increasing the speed of the field
def Fieldspeed():
    global speed
    if score > 150:
        speed += 2
    window.after(2000, Fieldspeed)
#if the users coordinates are within the coordinates of the astroids end game state is triggered.
def collisionUser():
#Checks if users coordinates are in the bbox of any of the active astroids in the field if True end game is triggered
    global userstate
    global finalscore
    userbboxX = list(range(canvasG.bbox(User)[0],canvasG.bbox(User)[2]))
    userbboxY = list(range(canvasG.bbox(User)[1],canvasG.bbox(User)[3]))
    for x in userbboxX:
        for y in field:
            if x in range(canvasG.bbox(y)[0],canvasG.bbox(y)[2]):
                for z in userbboxY :
                    if z in range(canvasG.bbox(y)[1],canvasG.bbox(y)[3]):
                        userstate = "Game Over"
                        finalscore = score # stores the users final score at time of collision
                        time.sleep(0.5)
                        canvasG.delete(*canvasG.find_all())
                        endGame()
    window.after(1, collisionUser)

def collisionShot():
    if len(shots) > 0 :
        for x in shots:
            for y in field:
                shotsXcoords = range(canvasG.bbox(x)[0], canvasG.bbox(x)[2])
                shotsYcoords = range(canvasG.bbox(x)[1], canvasG.bbox(x)[3])
                for z in shotsXcoords:
                    for w in shotsYcoords:
                        if z in range(canvasG.bbox(y)[0],canvasG.bbox(y)[2]):
                            if w in range(canvasG.bbox(y)[1],canvasG.bbox(y)[3]):
                                print ("hit")
                                #canvasG.delete(x)
                                #shots.remove(x)
    window.after(30, collisionShot)

def scorer():
    global score
    endTime= time.time()
    elapsedTime = endTime - startTime
    multiplier = int(elapsedTime/3)
    score =  multiplier * 10
    score_txt = "Score: " + str(score)
    canvasG.itemconfig(score_display, text = score_txt)
    window.after(10, scorer)
def endGame():
    #Changes the canvas to the end game screen
    canvasG.create_text(600, 300, fill = "White", font = "Arial 40 bold", text = ("Game Over YOU LOSE!!!") )
    canvasG.config(bg="grey")
    canvasG.create_text(600, 300, fill = "White", font = "Arial 40 bold", text = ('\n\n\n' + Playername + " Score: " + str(finalscore)) )
    #Adds Players name and score to leaderboard
    #fn = open("Names.txt", "a")
    #fn.write('\n' + Playername)
    #fn.close()
    #fs = open("Scores.txt", "a")
    #fs.write('\n' + str(finalscore))
    #fs.close()
    #Displays LeaderBoard in with scores displayed in descending order
    fn = open("Names.txt", "r")
    namelist =  [line.rstrip('\n') for line in fn]
    fn.close()
    fs = open("Scores.txt", "r")
    scorelist = [line.rstrip('\n') for line in fs]
    data = pandas.DataFrame({'Name': namelist,
                        'Score' : scorelist})
    data = data.sort_values(by='Score', ascending= False) # Displays scores in a table format and then sorts in descending order
    canvasG.create_text(600, 400, fill = "White", font = "Arial 40 bold", text ="LeaderBoard")
    canvasG.create_text(600, 600, fill = "White", font = "Arial 40 bold", text = data)
def fire(event):
#Allows user to fire 3 shots by pressing space bar.
    if userstate != "Game Over" and paused == "false" :
        x1 = (canvasG.bbox(User)[0] + canvasG.bbox(User)[2])/2
        y1 = canvasG.bbox(User)[1]
        if len(shots) < 3 :
            shots.append(canvasG.create_rectangle((x1 - 3),(y1 + 15), (x1 + 1 ), y1, fill="white" ))
def shotmove():
    if userstate != "Game Over" and paused == "false" :
        for x in shots:
            canvasG.move(x, 0 , -speed*2 )
            if canvasG.bbox(x)[1] <= 0:
                canvasG.delete(x)
                shots.remove(x)
    window.after(30, shotmove)

def pause(event):
    #If <p> is pressed the game is paused then unpauses game if presssed again
    global pausecount
    global paused
    pausecount += 1
    print(pausecount)
    if pausecount % 2 == 1:
        paused = "true"
        print (paused)
    else :
        paused = "false"

def bossKey(event):
    bosskeyimg = PhotoImage(file= "BossKeyImage.png")
    if pausecount % 2 == 1:
        canvasG.config(bg= bosskeyimg)
    else:
        canvasG.config(bg= "black")

userstate = "Active"
width = 1200
height = 1200
windowDimensions(width,height)
canvasG = Canvas(window , bg="black", width= width, height= height)
playerAvatar = PhotoImage(file="UserSprite.png")
User = canvasG.create_image(600, 600, image=playerAvatar)
direction = "up"
field = []
shots = []
speed = 10
pausecount = 0
paused = "false"



#Binds the event of pressing an arrow key with a function that causes an action
canvasG.bind("<KeyPress-Left>", leftKey)
canvasG.bind("<KeyPress-Right>", rightKey)
canvasG.bind("<KeyPress-Up>", upKey)
canvasG.bind("<KeyPress-Down>", downKey)
canvasG.bind("<space>", fire)
canvasG.bind("<p>", pause)
canvasG.focus_set()

score_display = canvasG.create_text(60, 15, fill = "White", font = "Arial 20 bold", text ="Score: ")
startTime = time.time()




Moveuser()
canvasG.pack()
scorer()
Fieldspeed()
astroidField1()
astroidField2()
astroidField3()
astroidFieldMove()
shotmove()
collisionUser()
collisionShot()
window.mainloop()
