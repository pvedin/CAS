from tkinter import * # import GUI module

class Pong(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)

        self.parent = parent
        self.initialize()


    def initialize(self): # main loop
        res = [800,600] # screen resolution, width x height
        canvas =  Canvas(width=res[0], height=res[1])
        canvas.pack()

        self.resizable(False,False)
        self.geometry("800x600")

        background = canvas.create_rectangle(0,0,res[0],res[1],fill="black")
        
        top_border =       canvas.create_line(res[0]*0.1   , 15           , res[0]*0.9, 15           , fill="white", width=30)
        divider =              canvas.create_line(res[0]/2       ,30           , res[0]/2   , res[1]      , fill="white", width=10, dash=(100,80))
        bottom_border = canvas.create_line(res[0]*0.1   , res[1]-15, res[0]*0.9, res[1]-15, fill="white", width=30)

       #projectile =def later

        #height = 80 pixels (ypos +- 40)
        player1_ypos= res[1]*0.5
        player2_ypos= res[1]*0.5

        player1 = canvas.create_line(res[0]*0.1+10,player1_ypos-40,res[0]*0.1+10,player1_ypos+40, fill="white", width=20)
        player2 = canvas.create_line(res[0]*0.9-10,player2_ypos-40,res[0]*0.9-10,player2_ypos+40, fill="white", width=20)

        player1_score_label = canvas.create_text(340,60, fill="white", text="10", font="Courier 50 bold")
        player2_score_label = canvas.create_text(460,60, fill="white", text="10", font="Courier 50 bold")

if __name__ == "__main__":

    app = Pong(None)
    app.title('Pong')
    app.mainloop()
