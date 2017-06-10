from tkinter import * # import GUI module
from random import randint # import randint function
from os import _exit # import exit function

class Pong(Tk):
    global p1Up,p2Up,p1Down,p2Down,MoveProjectile,ProjectileCollisionCheck
    global CheckFlags,StartRound,InitRound,DisplayWinner,CountDown

    def __init__(self,parent):

        Tk.__init__(self,parent)

        self.parent = parent
        self.initialize()


    def initialize(self): # main loop
        global projectile_properties,projectile,res
        global player1_properties,player2_properties
        global ProjectileCollisionCheck,MoveProjectile,CheckFlags,StartRound,new_round,new_game,round_start
        global canvas,seconds_until_difficulty_increase,extra_speed_from_CountDown,extra_speed_added
            
        res = [800,600] # screen resolution, width x height
        seconds_until_difficulty_increase = 10 # makes game more difficult every 10s; resets whenever a player scores
        extra_speed_from_CountDown = 0
        extra_speed_added = False
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

        
        player1_properties = {
            "flags": [False,False], #used for movement [up,down]
            "ypos": res[1] * 0.5,
            "score": 0,
            "xstrength": [60,80], # [min,max]
            "ystrength": [30,100], # [min,max]
            "movementSpeed": 10
            }
        
        player2_properties = {
            "flags": [False,False],
            "ypos": res[1] * 0.5,
            "score": 0,
            "xstrength": [-80,-60], # [min,max]
            "ystrength": [30,100], # [min,max]
            "movementSpeed": 10
            }

        player1 = canvas.create_line(res[0]*0.1+10,player1_properties["ypos"]-40,res[0]*0.1+10,player1_properties["ypos"]+40, fill="white", width=20)
        player2 = canvas.create_line(res[0]*0.9-10,player2_properties["ypos"]-40,res[0]*0.9-10,player2_properties["ypos"]+40, fill="white", width=20)

        player1_properties["player"] = player1
        player1_properties["scoreText"] = canvas.create_text(340,60, fill="white", text=player1_properties["score"], font="Courier 50 bold")
        player2_properties["player"] = player2
        player2_properties["scoreText"] = canvas.create_text(460,60, fill="white", text=player2_properties["score"], font="Courier 50 bold")

        projectile_properties = {
            "size": 20,
            "xpos": res[0]/2-10,
            "ypos": res[1]/2-10,
            "xvelocity": randint(60,80)/10,
            "yvelocity": randint(30,100)/10,
            "lastPlayerCollision": None
            }

        projectile = canvas.create_rectangle(projectile_properties["xpos"],projectile_properties["ypos"],
                                             projectile_properties["xpos"]+projectile_properties["size"],
                                             projectile_properties["ypos"]+projectile_properties["size"],
                                             fill="white")
        projectile_properties["projectile"] = projectile

        StartRound()
        CountDown()


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
        global projectile, projectile_properties,new_round, round_start
        global player1_properties,player2_properties,winner
        global extra_speed_from_CountDown,seconds_until_difficulty_increase,extra_speed_added
        #collisions with top/bottom borders respectively
        if projectile_properties["ypos"] <= 15 + projectile_properties["size"] - 5: # top border
            if projectile_properties["yvelocity"] < 0: # prevent bug where the projectile gets stuck inside the border
                projectile_properties["yvelocity"] *= -1
            
        if projectile_properties["ypos"] >= res[1]-15 - projectile_properties["size"] - 15:
            if projectile_properties["yvelocity"] > 0: # prevent bug
                projectile_properties["yvelocity"] *= -1

        #collisions with players 1 and 2 respectively , will generate new and random x and y velocities
        if (projectile_properties["xpos"] + 20 >= res[0]*0.1+10 and projectile_properties["xpos"] -10<= res[0]*0.1+10 and
            projectile_properties["ypos"] >= player1_properties["ypos"] - 50 and projectile_properties["ypos"] <= player1_properties["ypos"] + 50 and
            projectile_properties["lastPlayerCollision"]!= 1):
            projectile_properties["xvelocity"] = randint(player1_properties["xstrength"][0],player1_properties["xstrength"][1])/10 
            projectile_properties["yvelocity"] = randint(player1_properties["ystrength"][0],player1_properties["xstrength"][1])/10
            if randint(1,2) == 2: # change direction of yvelocity randomly
                projectile_properties["yvelocity"] *= -1 
            projectile_properties["lastPlayerCollision"] = 1
            extra_speed_added = False
            
        if (projectile_properties["xpos"] + 30 >= res[0]*0.9-10 and projectile_properties["xpos"] +10 <= res[0]*0.9-10 and
            projectile_properties["ypos"] >= player2_properties["ypos"] - 50 and projectile_properties["ypos"] <= player2_properties["ypos"] + 50 and
            projectile_properties["lastPlayerCollision"] != 2):
            projectile_properties["xvelocity"] = randint(player2_properties["xstrength"][0],player2_properties["xstrength"][1])/10
            projectile_properties["yvelocity"] = randint(player2_properties["xstrength"][0],player2_properties["xstrength"][1])/10
            if randint(1,2) == 2: # change direction of yvelocity
                projectile_properties["yvelocity"] *= -1
            projectile_properties["lastPlayerCollision"] = 2
            extra_speed_added = False


        if projectile_properties["xpos"] < 0: # player 2 scores
            #update scores and increase difficulty
            player2_properties["score"] += 1
            player1_properties["xstrength"][0] += 2  #increase min horizontal speed of projectile
            player1_properties["xstrength"][1] += 2  #increase max horizontal speed of projectile
            player1_properties["ystrength"][0] += 2  #increase min vertical speed of projectile
            player2_properties["movementSpeed"] += 1 #increase movement speed so projectile won't be impossible to send back
            canvas.itemconfig(player2_properties["scoreText"], text=player2_properties["score"])

            seconds_until_difficulty_increase = 10
            extra_speed_from_CountDown = 0            

            #end game if score == 10
            if player2_properties["score"] == 10:
                round_start = False
                winner = "Player 2" # declare player 2 as winner
                return DisplayWinner() # end game and display winner

            #reset projectile properties
            
            projectile_properties = {  
                    "size": 20,
                    "xpos": res[0]/2-10,
                    "ypos": res[1]/2-10,
                    "xvelocity": randint(50,70)/10, # projectile moves towards player 2 from rest
                    "yvelocity": randint(20,90)/10,
                    "lastPlayerCollision": None
                    }

            round_start= False
            new_round = True

        if projectile_properties["xpos"] > res[0]: # player 1 scores
            #update scores and increase difficulty
            player1_properties["score"] += 1
            player2_properties["xstrength"][0] += 2  #increase min horizontal speed of projectile
            player2_properties["xstrength"][1] += 2  #increase max horizontal speed of projectile
            player2_properties["ystrength"][0] += 2  #increase min vertical speed of projectile
            player1_properties["movementSpeed"] += 1 #increase movement speed so projectile won't be impossible to send back
            canvas.itemconfig(player1_properties["scoreText"], text=player1_properties["score"])

            seconds_until_difficulty_increase = 10
            extra_speed_from_CountDown = 0            


            #end game if score == 10
            if player1_properties["score"] == 10:
                round_start = False
                winner = "Player 1" # declare player 1 as winner
                return DisplayWinner() # end game and display winner
            
            
            #reset projectile properties
            projectile_properties = {  
                    "size": 20,
                    "xpos": res[0]/2-10,
                    "ypos": res[1]/2-10,
                    "xvelocity": randint(50,70)/10 * -1, # projectile moves towards player 1 from rest
                    "yvelocity": randint(20,90)/10,
                    "lastPlayerCollision": None
                    }

            round_start= False
            new_round = True

        
    def MoveProjectile():
        global projectile, projectile_properties,extra_speed_from_CountDown, extra_speed_added

        #increase difficulty the longer a round has been going
        if extra_speed_from_CountDown> 0 and extra_speed_added == False:
            if projectile_properties["xvelocity"] > 0:
                projectile_properties["xvelocity"] += extra_speed_from_CountDown
            else:
                projectile_properties["xvelocity"] -= extra_speed_from_CountDown
                
            if projectile_properties["yvelocity"] > 0:
                projectile_properties["yvelocity"] += extra_speed_from_CountDown
            else:
                projectile_properties["yvelocity"] -= extra_speed_from_CountDown

            extra_speed_added = True
            
        
        projectile_properties["xpos"] += projectile_properties["xvelocity"]
        projectile_properties["ypos"] += projectile_properties["yvelocity"]

        canvas.coords(projectile,(projectile_properties["xpos"],projectile_properties["ypos"],
                                  projectile_properties["xpos"]+projectile_properties["size"],
                                  projectile_properties["ypos"]+projectile_properties["size"]))
        

    def p1UpFlagSet(self, event):
        global player1_properties
        player1_properties["flags"][0] = True

    def p1UpFlagRemove(self, event):
        global player1_properties
        player1_properties["flags"][0] = False

    def p2UpFlagSet(self, event):
        global player2_properties
        player2_properties["flags"][0] = True
        
    def p2UpFlagRemove(self, event):
        global player2_properties
        player2_properties["flags"][0] = False

    def p1DownFlagSet(self, event):
        global player1_properties
        player1_properties["flags"][1] = True

    def p1DownFlagRemove(self, event):
        global player1_properties
        player1_properties["flags"][1] = False

    def p2DownFlagSet(self, event):
        global player2_properties
        player2_properties["flags"][1] = True
        
    def p2DownFlagRemove(self, event):
        global player2_properties
        player2_properties["flags"][1] = False
        
    def p1Up():
        global player1_properties,res
        if player1_properties["ypos"] - 40 > 35: #below top_border
            player1_properties["ypos"] -= player1_properties["movementSpeed"]
            canvas.coords(player1_properties["player"],(res[0]*0.1+10,player1_properties["ypos"]-40,res[0]*0.1+10,player1_properties["ypos"]+40))

    def p1Down():
        global player1_properties,res
        if player1_properties["ypos"] + 40 < res[1]-15 - 20: #above bottom_border
            player1_properties["ypos"] += player1_properties["movementSpeed"]
            canvas.coords(player1_properties["player"],(res[0]*0.1+10,player1_properties["ypos"]-40,res[0]*0.1+10,player1_properties["ypos"]+40))
            
    def p2Up():
        global player2_properties,res
        if player2_properties["ypos"] - 40 > 35: #below top_border
            player2_properties["ypos"] -= player2_properties["movementSpeed"]
            canvas.coords(player2_properties["player"],(res[0]*0.9-10,player2_properties["ypos"]-40,res[0]*0.9-10,player2_properties["ypos"]+40))

    def p2Down():
        global player2_properties,res
        if player2_properties["ypos"] + 40 < res[1]-15 - 20: #above bottom_border
            player2_properties["ypos"] += player2_properties["movementSpeed"]
            canvas.coords(player2_properties["player"],(res[0]*0.9-10,player2_properties["ypos"]-40,res[0]*0.9-10,player2_properties["ypos"]+40))

    def CheckFlags(): #update movement
        global player1_properties,player2_properties
        if player1_properties["flags"][0]:
            p1Up()
        elif player1_properties["flags"][1]:
            p1Down()

        if player2_properties["flags"][0]:
            p2Up()
        elif player2_properties["flags"][1]:
            p2Down()

    def DisplayWinner():
        global winner
        canvas.delete("all") #clear canvas
        
        background = canvas.create_rectangle(0,0,res[0],res[1],fill="black")
        
        text_winner = canvas.create_text(400,60, fill="white", text=winner, font="Courier 80 bold")
        text_won = canvas.create_text(400,160, fill="white", text="won!", font="Courier 70 bold")

        press_enter_to_quit = canvas.create_text(400,350, fill="white", text="Press any key to exit", font="Courier 25 italic")
        
        
        app.bind("<Key>",lambda x: _exit(0)) #closes window when any key is pressed

    def CountDown():
        global seconds_until_difficulty_increase, extra_speed_from_CountDown
        seconds_until_difficulty_increase -= 1

        if seconds_until_difficulty_increase == 0:
            seconds_until_difficulty_increase = 10
            extra_speed_from_CountDown += 2
            

        canvas.after(1000,CountDown)


if __name__ == "__main__":

    app = Pong(None)
    #define controls for player 1 (both lower-case and upper-case W and S)
    app.bind("<w>",app.p1UpFlagSet)
    app.bind("<KeyRelease-w>",app.p1UpFlagRemove)
    app.bind("<s>",app.p1DownFlagSet)
    app.bind("<KeyRelease-s>",app.p1DownFlagRemove)
    app.bind("<W>",app.p1UpFlagSet)
    app.bind("<KeyRelease-W>",app.p1UpFlagRemove)
    app.bind("<S>",app.p1DownFlagSet)
    app.bind("<KeyRelease-S>",app.p1DownFlagRemove)

    #define controls for player 2
    app.bind("<Up>",app.p2UpFlagSet)
    app.bind("<KeyRelease-Up>",app.p2UpFlagRemove)
    app.bind("<Down>",app.p2DownFlagSet)
    app.bind("<KeyRelease-Down>",app.p2DownFlagRemove)

    
    app.title('Pong')
    app.mainloop()
