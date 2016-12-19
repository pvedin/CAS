from tkinter import * # import GUI module
from random import randint #import randint function

##
## TODO:
## - Fix positioning hiccup when reseting projectile
## - Update scores when reseting projectile
## - Add screen showing who won when a player gets 10 points
##

class Pong(Tk):
    global p1Up,p2Up,p1Down,p2Down,MoveProjectile,ProjectileCollisionCheck,CheckFlags,StartRound,InitRound
    
    def __init__(self,parent):

        Tk.__init__(self,parent)

        self.parent = parent
        self.initialize()


    def initialize(self): # main loop
        global player1,player1_ypos,player2,player2_ypos,projectile_properties,projectile,res
        global p1Flags,p2Flags
        global ProjectileCollisionCheck,MoveProjectile,CheckFlags,StartRound,new_round,new_game,round_start
        global canvas
            
        res = [800,600] # screen resolution, width x height
        new_game = True # used on program startup 
        new_round = False
        round_start = False
        canvas =  Canvas(width=res[0], height=res[1])
        canvas.pack()

        self.resizable(False,False) #resizing the window is not allowed
        self.geometry(str(res[0]) + "x" + str(res[1])) # sets resolution

        background = canvas.create_rectangle(0,0,res[0],res[1],fill="black")
        
                       #(x1,y1,x2,y2)
        top_border =    canvas.create_line(res[0]*0.1, 15       , res[0]*0.9, 15       , fill="white", width=30)
        divider =       canvas.create_line(res[0]/2  , 30       , res[0]/2  , res[1]   , fill="white", width=10, dash=(100,80))
        bottom_border = canvas.create_line(res[0]*0.1, res[1]-15, res[0]*0.9, res[1]-15, fill="white", width=30)

        #height = 80 pixels (ypos +- 40)
        player1_ypos= res[1]*0.5
        player2_ypos= res[1]*0.5

        player1 = canvas.create_line(res[0]*0.1+10,player1_ypos-40,res[0]*0.1+10,player1_ypos+40, fill="white", width=20)
        player2 = canvas.create_line(res[0]*0.9-10,player2_ypos-40,res[0]*0.9-10,player2_ypos+40, fill="white", width=20)

        #used for movement [up,down]
        p1Flags = [False,False]
        p2Flags = [False,False]

        player1_score_label = canvas.create_text(340,60, fill="white", text="0", font="Courier 50 bold")
        player2_score_label = canvas.create_text(460,60, fill="white", text="0", font="Courier 50 bold")

        projectile_properties = {
            "size": 20,
            "xpos": res[0]/2-10,
            "ypos": res[1]/2-10,
            "xvelocity": 5,#31 = max
            "yvelocity": 7,
            "lastPlayerCollision": None
            }

        projectile = canvas.create_rectangle(projectile_properties["xpos"],projectile_properties["ypos"],
                                             projectile_properties["xpos"]+projectile_properties["size"],
                                             projectile_properties["ypos"]+projectile_properties["size"],
                                             fill="white")

        StartRound()


    def StartRound():
        global new_round, new_game, round_start,projectile_properties
        if new_round:
                new_round = False
                canvas.after(int(2000),InitRound) #projectile starts moving after 2s
        if new_game: #only runs once
                new_game = False
                new_round = True
        if round_start:
            ProjectileCollisionCheck()
            MoveProjectile()
            CheckFlags()

        canvas.after(int(1000/60),StartRound)


    def InitRound():
        global round_start
        round_start = True
        pass

    def ProjectileCollisionCheck():
        global projectile, projectile_properties,player1_ypos,player2_ypos,new_round, round_start
        #collisions with top/bottom borders
        if (projectile_properties["ypos"] <= 15 + projectile_properties["size"] - 5 or
            projectile_properties["ypos"] >= res[1]-15 - projectile_properties["size"] - 15):
            projectile_properties["yvelocity"] *= -1

        #collisions with players 1 and 2 respectively , will generate new and random x and y velocities
        if (projectile_properties["xpos"] + 20 >= res[0]*0.1+10 and projectile_properties["xpos"] -10<= res[0]*0.1+10 and
            projectile_properties["ypos"] >= player1_ypos - 50 and projectile_properties["ypos"] <= player1_ypos + 50 and
            projectile_properties["lastPlayerCollision"]!= 1):
            projectile_properties["xvelocity"] = randint(60,80)/10 #positive = right
            if projectile_properties["yvelocity"] > 0:
                projectile_properties["yvelocity"] = randint(50,80)/10
            else:
                projectile_properties["yvelocity"] = randint(-80,-50)/10
            projectile_properties["lastPlayerCollision"] = 1
            
        if (projectile_properties["xpos"] + 30 >= res[0]*0.9-10 and projectile_properties["xpos"] +10 <= res[0]*0.9-10 and
            projectile_properties["ypos"] >= player2_ypos - 50 and projectile_properties["ypos"] <= player2_ypos + 50 and
            projectile_properties["lastPlayerCollision"] != 2):
            projectile_properties["xvelocity"] = randint(-80,-60)/10 #negative = left
            projectile_properties["yvelocity"] = randint(30,100)/10
            if randint(1,2) == 2: # change direction of yvelocity
                projectile_properties["yvelocity"] *= -1
                
            projectile_properties["lastPlayerCollision"] = 2


        if projectile_properties["xpos"] < 0: # player 2 scores
            #update scores
            # .....

            projectile_properties = {  #reset projectile properties
                    "size": 20,
                    "xpos": res[0]/2-10,
                    "ypos": res[1]/2-10,
                    "xvelocity": 5,#31 = max (will go through players if above 31)
                    "yvelocity": 7, #no apparent limit
                    "lastPlayerCollision": None
                    }

            round_start= False
            new_round = True

        if projectile_properties["xpos"] > res[0]: # player 1 scores
            #update scores
            # .....

            projectile_properties = {  #reset projectile properties
                    "size": 20,
                    "xpos": res[0]/2-10,
                    "ypos": res[1]/2-10,
                    "xvelocity": 5,#31 = max (will go through players if above 31)
                    "yvelocity": 7, #no apparent limit
                    "lastPlayerCollision": None
                    }

            round_start= False
            new_round = True

        
    def MoveProjectile():
        global projectile, projectile_properties
        projectile_properties["xpos"] += projectile_properties["xvelocity"]
        projectile_properties["ypos"] += projectile_properties["yvelocity"]

        canvas.coords(projectile,(projectile_properties["xpos"],projectile_properties["ypos"],
                                  projectile_properties["xpos"]+projectile_properties["size"],
                                  projectile_properties["ypos"]+projectile_properties["size"]))
        

    def p1UpFlagSet(self, event):
        global p1Flags
        p1Flags[0] = True

    def p1UpFlagRemove(self, event):
        global p1Flags
        p1Flags[0] = False

    def p2UpFlagSet(self, event):
        global p2Flags
        p2Flags[0] = True
        
    def p2UpFlagRemove(self, event):
        global p2Flags
        p2Flags[0] = False

    def p1DownFlagSet(self, event):
        global p1Flags
        p1Flags[1] = True

    def p1DownFlagRemove(self, event):
        global p1Flags
        p1Flags[1] = False

    def p2DownFlagSet(self, event):
        global p2Flags
        p2Flags[1] = True
        
    def p2DownFlagRemove(self, event):
        global p2Flags
        p2Flags[1] = False
        
    def p1Up():
        global player1_ypos,player1,res
        if player1_ypos - 40 > 35: #below top_border
            player1_ypos -= 10
            canvas.coords(player1,(res[0]*0.1+10,player1_ypos-40,res[0]*0.1+10,player1_ypos+40))

    def p1Down():
        global player1,player1_ypos,res
        if player1_ypos + 40 < res[1]-15 - 20: #above bottom_border
            player1_ypos += 10
            canvas.coords(player1,(res[0]*0.1+10,player1_ypos-40,res[0]*0.1+10,player1_ypos+40))
            
    def p2Up():
        global player2_ypos,player2,res
        if player2_ypos - 40 > 35: #below top_border
            player2_ypos -= 10
            canvas.coords(player2,(res[0]*0.9-10,player2_ypos-40,res[0]*0.9-10,player2_ypos+40))

    def p2Down():
        global player2,player2_ypos,res
        if player2_ypos + 40 < res[1]-15 - 20: #above bottom_border
            player2_ypos += 10
            canvas.coords(player2,(res[0]*0.9-10,player2_ypos-40,res[0]*0.9-10,player2_ypos+40))

    def CheckFlags(): #update movement
        global p1Flags,p2Flags
        if p1Flags[0]:
            p1Up()
        elif p1Flags[1]:
            p1Down()

        if p2Flags[0]:
            p2Up()
        elif p2Flags[1]:
            p2Down()

if __name__ == "__main__":

    app = Pong(None)
    app.bind("<w>",app.p1UpFlagSet)
    app.bind("<KeyRelease-w>",app.p1UpFlagRemove)
    app.bind("<s>",app.p1DownFlagSet)
    app.bind("<KeyRelease-s>",app.p1DownFlagRemove)
    
    app.bind("<Up>",app.p2UpFlagSet)
    app.bind("<KeyRelease-Up>",app.p2UpFlagRemove)
    app.bind("<Down>",app.p2DownFlagSet)
    app.bind("<KeyRelease-Down>",app.p2DownFlagRemove)

    
    app.title('Pong')
    app.mainloop()

