import tkinter as tk  # for GUI
import glob, os, random, sys  # glob is for packing together file names, sys is for exiting cleanly
from PIL import ImageTk, Image
# import RPi.GPIO as GPIO  # For inputs/outputs
from time import perf_counter
from threading import Timer  # for periodic loops
from functools import partial  # for passing arguments to events handled within commands (e.g. Bind() or Button())

# Global Variables
# ---------------------
VI_list = [10, 12, 12, 15, 15, 15, 17, 17, 20]  # varying break intervals (VI: variable interval)


# ---------------------


# Setup I/Os.
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(pellet, GPIO.OUT)
# GPIO.setup(hopper_beam, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# def on(variable):
#   GPIO.output(variable, GPIO.LOW)
# def off(variable):
#   GPIO.output(variable, GPIO.HIGH)
# Turns off all outputs at start of a program
# def all_off_start():
#   off(pellet)
# all_off_start()


# Basic reinf/punishment functions
def reinforcement():
    # Outputs:
    pellet = 17
    # Inputs:
    hopper_beam = 18
    ReinfAmt = 1
    reinforcers = 0
    # def reinf_off():
    # off(pellet)
    while reinforcers >= ReinfAmt:
        # on(pellet)
        pellet_timer = Timer(0.25, reinf_off)  # timer 0.25s delay for pellet cycle
        pellet_timer.start()
        pellet_timer.join()
        reinforcers += 1


# BEGIN PROGRAM
# -------------

def stage1():
    global trial, stim, correct
    ###
    # initalize trial number counter, i don't think this segment is necessary currently so it's commented out
    # trial = 0
    # trial += 1
    # print("Trial:" + str(trial))
    ###

    # stopwatch for stage1
    start_time1 = perf_counter()
    # using random, choose a random img from the imglist which will be the correct image for stage 2
    correct = random.choice(imglist)
    # Initial cue image presented and waits for response
    # when response is recieved, move on to stage2
    sample_btn1 = tk.Button(gui, image=correct, command=stage2())
    sample_btn1.place(relheight=0.4, rely=0.3, relwidth=0.3, relx=0.65, anchor="ne")


def stage2():
    print('bunted')


if __name__ == '__main__':
    # GUI Initialization
    gui = tk.Tk()
    gui.state('zoomed')

    # get screen info
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()

    # assembling of images
    imgfilenames = glob.glob("*.jpg")
    imglist = []

    for file in imgfilenames:
        # for every file in the list of imgs, open and resize then append the resized img object to imglist
        imgtemp = Image.open(file).resize((int(screen_width * 0.17), int(screen_height * 0.3)), Image.ANTIALIAS)
        # converts the image into a compatible tkinter image
        imglist.append(ImageTk.PhotoImage(imgtemp))

    # local variation of the press function to handle pushes of the start and stop button in the main menu

    def press(btn):
        if btn == "START":
            stage1()
            main_menu_destroy()
        else:
            gui.destroy()
            sys.exit()

    def main_menu_destroy():
        start_button.destroy()
        quit_button.destroy()

    # upon push of start, call this function to remove the start and quit buttons

    # THESE ARE GLOBAL SO THE press(btn) FUNCTION IS ABLE TO HANDLE BUTTON PRESSES
    # this press(btn) function is specific to this segment of code because it is only handling
    # main menu inputs
    global start_button, quit_button
    # creates and places a button with the text START which begins stage1()
    start_button = tk.Button(gui, text="START", font=("bold", "40"), command=partial(press, "START")) \
        .place(relheight=0.5, relwidth=0.5, relx=1, rely=0, anchor="ne")

    # creates and places a button with the text QUIT which destroys the gui and exits the program
    quit_button = tk.Button(gui, text="QUIT", font=("bold", "40"), command=partial(press, "QUIT")) \
        .place(relheight=.15, relwidth=.1, relx=1, rely=.85, anchor="ne")




    gui.mainloop()
