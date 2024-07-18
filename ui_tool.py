import tkinter as tk
import tkinter.font as tkFont
from subprocess import run
from TheGame.main import DeliveryRobot

SILENT_MODE = False
LAMGUAGE = "fr"
NB_BALLS = 2
CONN_TYPE = "ap"
SERIAL_NUMBER = ""
KP_X = 2.0
KI_X = 0.038
KP_Y = 5.0
KI_Y = 0.038

class UI:
    def __init__(self) -> None:
        pass

    def get_values(self):
        global SILENT_MODE, LAMGUAGE, NB_BALLS, CONN_TYPE, SERIAL_NUMBER, KP_X, KI_X, KP_Y, KI_Y
        LAMGUAGE = self.lang.get()
        if LAMGUAGE == "silent":
            SILENT_MODE = True
        else:
            SILENT_MODE = False
        NB_BALLS = int(self.nb_balls.get())
        CONN_TYPE = self.conn.get()
        SERIAL_NUMBER = self.entry_sn.get()
        KP_X = float(self.kp_x.get())
        KI_X = float(self.ki_x.get())
        KP_Y = float(self.kp_y.get())
        KI_Y = float(self.ki_y.get())
        print("Starting the game with the following parameters:")
        print("KP_X:", KP_X)
        print("KI_X:", KI_X)
        print("KP_Y:", KP_Y)
        print("KI_Y:", KI_Y)
        print("NB_BALLS:", NB_BALLS)
        print("CONN_TYPE:", CONN_TYPE)
        print("SERIAL_NUMBER:", SERIAL_NUMBER)
        print("LAMGUAGE:", LAMGUAGE)
        self.action_start()

    def action_start(self):
        global SILENT_MODE, LAMGUAGE, NB_BALLS, CONN_TYPE, SERIAL_NUMBER, KP_X, KI_X, KP_Y, KI_Y
        #cmd = f'''
        #Set-ExecutionPolicy Unrestricted -Scope Process ; 
        #.\.venv\Scripts\activate ; 
        #python TheGame\main.py --silent {SILENT_MODE} --lang {LAMGUAGE} --nb_balls {NB_BALLS} --conn_type {CONN_TYPE} --serial_number {SERIAL_NUMBER} --kp_x {KP_X} --ki_x {KI_X} --kp_y {KP_Y} --ki_y {KI_Y}
        #'''
        #run(cmd, shell=True)
        robot = DeliveryRobot(silent=SILENT_MODE, lang=LAMGUAGE, nb_balls=NB_BALLS, conn_type=CONN_TYPE, sn=SERIAL_NUMBER)
        robot.ki_x = KI_X
        robot.kp_x = KP_X
        robot.ki_y = KI_Y
        robot.kp_y = KP_Y
        robot.start()
        #robot.close()

    def main(self):
        global SILENT_MODE, LAMGUAGE, NB_BALLS, CONN_TYPE, SERIAL_NUMBER, KP_X, KI_X, KP_Y, KI_Y
        root = tk.Tk()
        root.title("Delivery game")

        width=610
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_362=tk.Label(root)
        GLabel_362["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=14, weight='bold')
        GLabel_362["font"] = ft
        GLabel_362["fg"] = "#333333"
        GLabel_362["justify"] = "center"
        GLabel_362.place(x=0,y=0,width=610,height=60)

        GLabel_362=tk.Label(root)
        GLabel_362["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=14, weight='bold')
        GLabel_362["font"] = ft
        GLabel_362["fg"] = "#333333"
        GLabel_362["justify"] = "center"
        GLabel_362["text"] = "PI tuning parameters"
        GLabel_362.place(x=0,y=60,width=610,height=35)

        ft = tkFont.Font(family='Times',size=12)

        GLabel_kpx=tk.Label(root)
        GLabel_kpx["font"] = ft
        GLabel_kpx["fg"] = "#333333"
        GLabel_kpx["justify"] = "center"
        GLabel_kpx["text"] = "KP_x"
        GLabel_kpx.place(x=5,y=105,width=65,height=18)

        self.kp_x = tk.StringVar(root,value="2.0")
        entry_kpx=tk.Entry(root, textvariable=self.kp_x)
        entry_kpx["borderwidth"] = "1px"
        entry_kpx["font"] = ft
        entry_kpx["fg"] = "#333333"
        entry_kpx["justify"] = "center"
        #entry_kpx["text"] = "KP_x"
        #entry_kpx["relief"] = "groove"
        entry_kpx.place(x=60,y=105,width=65,height=18)

        GLabel_kix=tk.Label(root)
        GLabel_kix["font"] = ft
        GLabel_kix["fg"] = "#333333"
        GLabel_kix["justify"] = "center"
        GLabel_kix["text"] = "KI_x"
        GLabel_kix.place(x=135,y=105,width=65,height=18)

        self.ki_x = tk.StringVar(root,value="0.038")
        entry_kix=tk.Entry(root, textvariable=self.ki_x)
        entry_kix["borderwidth"] = "1px"
        entry_kix["font"] = ft
        entry_kix["fg"] = "#333333"
        entry_kix["justify"] = "center"
        #entry_kix["text"] = "KP_x"
        #entry_kix["relief"] = "groove"
        entry_kix.place(x=190,y=105,width=65,height=18)

        GLabel_kpy=tk.Label(root)
        GLabel_kpy["font"] = ft
        GLabel_kpy["fg"] = "#333333"
        GLabel_kpy["justify"] = "center"
        GLabel_kpy["text"] = "KP_y"
        GLabel_kpy.place(x=265,y=105,width=65,height=18)

        self.kp_y = tk.StringVar(root,value="5.0")
        entry_kpy=tk.Entry(root, textvariable=self.kp_y)
        entry_kpy["borderwidth"] = "1px"
        entry_kpy["font"] = ft
        entry_kpy["fg"] = "#333333"
        entry_kpy["justify"] = "center"
        #entry_kix["text"] = "KI_x"
        #entry_kix["relief"] = "groove"
        entry_kpy.place(x=320,y=105,width=65,height=18)

        GLabel_kpy=tk.Label(root)
        GLabel_kpy["font"] = ft
        GLabel_kpy["fg"] = "#333333"
        GLabel_kpy["justify"] = "center"
        GLabel_kpy["text"] = "KP_y"
        GLabel_kpy.place(x=265,y=105,width=65,height=18)

        self.kp_y = tk.StringVar(root,value="5.0")
        entry_kpy=tk.Entry(root, textvariable=self.kp_y)
        entry_kpy["borderwidth"] = "1px"
        entry_kpy["font"] = ft
        entry_kpy["fg"] = "#333333"
        entry_kpy["justify"] = "center"
        #entry_kpy["text"] = "KP_y"
        #entry_kpy["relief"] = "groove"
        entry_kpy.place(x=320,y=105,width=65,height=18)

        GLabel_kiy=tk.Label(root)
        GLabel_kiy["font"] = ft
        GLabel_kiy["fg"] = "#333333"
        GLabel_kiy["justify"] = "center"
        GLabel_kiy["text"] = "KI_y"
        GLabel_kiy.place(x=395,y=105,width=65,height=18)

        self.ki_y = tk.StringVar(root,value="0.038")
        entry_kiy=tk.Entry(root, textvariable=self.ki_y)
        entry_kiy["borderwidth"] = "1px"
        entry_kiy["font"] = ft
        entry_kiy["fg"] = "#333333"
        entry_kiy["justify"] = "center"
        #entry_kiy["text"] = "KI_y"
        #entry_kiy["relief"] = "groove"
        entry_kiy.place(x=450,y=105,width=65,height=18)

        GLabel_362=tk.Label(root)
        GLabel_362["bg"] = "#ffffff"
        GLabel_362["font"] = ft
        GLabel_362["fg"] = "#333333"
        GLabel_362["justify"] = "center"
        GLabel_362["text"] = "Other options"
        GLabel_362.place(x=0,y=150,width=610,height=22)

        GLabel_lang=tk.Label(root)
        GLabel_lang["font"] = ft
        GLabel_lang["fg"] = "#333333"
        GLabel_lang["justify"] = "left"
        GLabel_lang["text"] = "Audio"
        GLabel_lang.place(x=-20,y=230,width=110,height=18)
        self.lang = tk.StringVar(root)
        self.lang.set("silent")
        Radio_fr = tk.Radiobutton(root, text="FR", variable=self.lang, value="fr")
        Radio_fr.place(x=120, y=230)
        Radio_en = tk.Radiobutton(root, text="EN", variable=self.lang, value="en")
        Radio_en.place(x=170, y=230)
        Radio_silent = tk.Radiobutton(root, text="Silent", variable=self.lang, value="silent")
        Radio_silent.place(x=220, y=230)

        GLabel_balls=tk.Label(root)
        GLabel_balls["font"] = ft
        GLabel_balls["fg"] = "#333333"
        GLabel_balls["justify"] = "left"
        GLabel_balls["text"] = "Number of balls"
        GLabel_balls.place(x=0,y=190,width=130,height=18)

        self.nb_balls = tk.StringVar(root,value="2")
        entry_balls=tk.Entry(root, textvariable=self.nb_balls)
        entry_balls["borderwidth"] = "1px"
        entry_balls["font"] = ft
        entry_balls["fg"] = "#333333"
        entry_balls["justify"] = "left"
        #entry_balls["text"] = "nb_balls"
        #entry_balls["relief"] = "groove"
        entry_balls.place(x=140,y=190,width=65,height=18)

        GLabel_conn=tk.Label(root)
        GLabel_conn["font"] = ft
        GLabel_conn["fg"] = "#333333"
        GLabel_conn["justify"] = "left"
        GLabel_conn["text"] = "Connection type"
        GLabel_conn.place(x=-10 ,y=265,width=150,height=18)
        self.conn = tk.StringVar(root)
        self.conn.set("ap")
        Radio_ap = tk.Radiobutton(root, text="Direct", variable=self.conn, value="ap")
        Radio_ap.place(x=130, y=265)
        Radio_sta = tk.Radiobutton(root, text="Router", variable=self.conn, value="sta")
        Radio_sta.place(x=190, y=265)

        GLabel_sn=tk.Label(root)
        GLabel_sn["font"] = ft
        GLabel_sn["fg"] = "#333333"
        GLabel_sn["justify"] = "left"
        GLabel_sn["text"] = "Robot serial number*"
        GLabel_sn.place(x=15,y=305,width=130,height=18)

        #self.sn = tk.StringVar(root)
        self.entry_sn=tk.Entry(root)
        self.entry_sn["borderwidth"] = "1px"
        self.entry_sn["font"] = ft
        self.entry_sn["fg"] = "#333333"
        self.entry_sn["justify"] = "left"
        #self.entry_balls["text"] = "sn"
        #self.entry_balls["relief"] = "groove"
        self.entry_sn.place(x=150,y=305,width=130,height=18)

        GButton_start=tk.Button(root)
        GButton_start["bg"] = "#efefef"
        GButton_start["font"] = ft
        GButton_start["fg"] = "#000000"
        GButton_start["justify"] = "left"
        GButton_start["text"] = "Start"
        GButton_start.place(x=250,y=335,width=100,height=38)
        GButton_start["command"] = self.get_values
        
        msg = '''
    * When using the router connection, you need to specify the robot's correct serial number. This is generally made up of 14 alphanumeric characters written on the robot.
        '''
    #- The number of balls can be -1 in the case of an infinite loop (not recommended).\n
    # Reminder: If you increase the value of Kp, you gain speed but lose precision. If you increase the value of Ki, you lose precision and stability.  
        GMessage_info=tk.Label(root, wraplength=550)
        GMessage_info["font"] = tkFont.Font(family='Times',size=10, slant='italic')
        GMessage_info["fg"] = "#333333"
        GMessage_info["justify"] = "left"
        GMessage_info["text"] = msg
        GMessage_info.place(x=20,y=380,height=80)

        image = tk.PhotoImage(file="assets/CS.png")
        image_resized = image.subsample(8, 8)  # Les arguments sont les facteurs de réduction pour la largeur et la hauteur
        image_label = tk.Label(root, image=image_resized)
        image_label.place(x=0, y=0)

        image2 = tk.PhotoImage(file="assets/L2S.png")
        image_resized2 = image2.subsample(11, 12)  # Les arguments sont les facteurs de réduction pour la largeur et la hauteur
        image_label2 = tk.Label(root, image=image_resized2)
        image_label2.place(x=465, y=0)

        
        root.mainloop()

if __name__ == "__main__":
    ui = UI()
    ui.main()