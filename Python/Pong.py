from tkinter import * # import GUI module

class Pong(Tk):
    global p1Up,p2Up,p1Down,p2Down,MoveProjectile,ProjectileCollisionCheck,CheckFlags
    
    def __init__(self,parent):
        Tk.__init__(self,parent)

        self.parent = parent
        self.initialize()


    def initialize(self): # main loop
        global player1,player1_ypos,player2,player2_ypos,projectile_properties,projectile,res
        global p1Flags,p2Flags
        global ProjectileCollisionCheck,MoveProjectile,CheckFlags
        global canvas
            
        res = [800,600] # screen resolution, width x height
        canvas =  Canvas(width=res[0], height=res[1])
        canvas.pack()

        self.resizable(False,False)
        self.geometry("800x600")

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

        player1_score_label = canvas.create_text(340,60, fill="white", text="10", font="Courier 50 bold")
        player2_score_label = canvas.create_text(460,60, fill="white", text="10", font="Courier 50 bold")

        projectile_properties = {
            "size": 20,
            "xpos": res[0]/2-10,
            "ypos": res[1]/2-10,
            "xvelocity": 2,#31 = max
            "yvelocity": 0,
            "lastPlayerCollision": None
            }

        projectile = canvas.create_rectangle(projectile_properties["xpos"],projectile_properties["ypos"],
                                             projectile_properties["xpos"]+projectile_properties["size"],
                                             projectile_properties["ypos"]+projectile_properties["size"],
                                             fill="white")

        ProjectileCollisionCheck()
        MoveProjectile()
        CheckFlags()

    def ProjectileCollisionCheck():
        global projectile, projectile_properties,player1_ypos,player2_ypos
        #collisions with top/bottom borders
        if (projectile_properties["ypos"] <= 15 + projectile_properties["size"] - 5 or
            projectile_properties["ypos"] >= res[1]-15 - projectile_properties["size"] - 15):
            projectile_properties["yvelocity"] *= -1

        #collisions with players 1 and 2 respectively
        if (projectile_properties["xpos"] + 20 >= res[0]*0.1+10 and projectile_properties["xpos"] -10<= res[0]*0.1+10 and
            projectile_properties["ypos"] >= player1_ypos - 50 and projectile_properties["ypos"] <= player1_ypos + 50 and
            projectile_properties["lastPlayerCollision"]!= 1):
            projectile_properties["xvelocity"] *= -1
            projectile_properties["lastPlayerCollision"] = 1
            
        if (projectile_properties["xpos"] + 30 >= res[0]*0.9-10 and projectile_properties["xpos"] +10 <= res[0]*0.9-10 and
            projectile_properties["ypos"] >= player2_ypos - 50 and projectile_properties["ypos"] <= player2_ypos + 50 and
            projectile_properties["lastPlayerCollision"] != 2):
            projectile_properties["xvelocity"] *= -1
            projectile_properties["lastPlayerCollision"] = 2
            
        canvas.after(int(1000/60),ProjectileCollisionCheck) #check approx. 60 times/sec

        
    def MoveProjectile():
        global projectile, projectile_properties
        projectile_properties["xpos"] += projectile_properties["xvelocity"]
        projectile_properties["ypos"] += projectile_properties["yvelocity"]

        canvas.coords(projectile,(projectile_properties["xpos"],projectile_properties["ypos"],
                                  projectile_properties["xpos"]+projectile_properties["size"],
                                  projectile_properties["ypos"]+projectile_properties["size"]))

        canvas.after(int(1000/60),MoveProjectile) #approx. 60fps

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

        canvas.after(int(1000/60),CheckFlags)

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
