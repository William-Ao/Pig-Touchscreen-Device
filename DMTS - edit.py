import tkinter as tk  # for GUI
from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image
#import RPi.GPIO as GPIO  # For inputs/outputs
from threading import Timer  # for periodic loops
import random  # for random number selection
from time import perf_counter  # for calculating latencies/timers
import time

# Outputs:
pellet = 17
# Inputs:
hopper_beam = 18

# Setup I/Os.
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(pellet, GPIO.OUT)
#GPIO.setup(hopper_beam, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Global Variables
response = 0
trial = 0
stage_1_start_time = 0
stage_2_start_time = 0
VI_list = [10, 12, 12, 15, 15, 15, 17, 17, 20]

active_list = [1, 2]
stim = 0
# Recorded Data
stage_2_correct = 0
stage_2_incorrect = 0

# Settings Variables able to be modified
Blackout = 0.01 # timer in min
ReinfAmt = 1


#def on(variable):
 #   GPIO.output(variable, GPIO.LOW)
#def off(variable):
 #   GPIO.output(variable, GPIO.HIGH)
# Turns off all outputs at start of a program
#def all_off_start():
 #   off(pellet)
#all_off_start()


# Defines response to Tkinter button sets variable = to that response
def press(var):
    global response
    response = var


# Basic reinf/punishment functions
def reinforcement():
    reinforcers = 0
    #def reinf_off():
        #off(pellet)
    while True:
        #on(pellet)
        pellet_timer = Timer(0.25)#, reinf_off)  # timer 0.25s delay for pellet cycle
        pellet_timer.start()
        pellet_timer.join()
        reinforcers += 1
        if reinforcers >= ReinfAmt:
            break

# Main program loop
def stage_1_setup():
    global trial, stage_1_start_time
    time.sleep(random.choice(VI_list)/2)
    trial += 1
    print("trials:" + str(trial))
    stage_1_start_time = perf_counter()
    global stim, correct
    stim = random.choice(img_list)
    print(stim)
    correct = random.choice(stim)
    print(correct)
    sample_btn1 = Button(gui, image=stim)
    time.sleep(0.1)
    sample_btn1.place(relheight=0.4, rely=0.3, relwidth=0.3, relx=0.65, anchor="ne")
    stage_1()

def stage_1():  # sample presentation
    def stage_1_reloop():
        global response, stage_1_start_time
        stage_1_timer.cancel()
        if response != 0:
            response = 0
            sample_btn1.place_forget()
            stage_2_setup()
        else:
            stage_1_loop()

    increment = 0.01
    stage_1_timer = Timer(increment, stage_1_reloop)
    stage_1_timer.start()
def stage_1_loop():
    stage_1()


def stage_2_setup():  # discrimination of two squares
    global trial, stage_2_start_time, stim
    time.sleep(random.choice(VI_list)/2)
    choice_btn1.configure(image=stim[1])
    choice_btn2.configure(image=stim[0])
    choice_btn1.place(relheight=0.355, relwidth=0.2, rely=0.35, relx=0.3, anchor="ne")
    choice_btn2.place(relheight=0.355, relwidth=0.2, rely=0.35, relx=0.9, anchor="ne")
    stage_2_start_time = perf_counter()
    stage_2()

def stage_2():
    def stage_2_reloop():
        global response, stage_2_start_time, stage_2_correct, stage_2_incorrect, stim, correct

        def incorrect():
            global stage_2_incorrect
            stage_2_incorrect += 1
            quit_button.config(bg="white")
            inc_label.place(relheight=1, relwidth=1, relx=1, rely=0, anchor="ne")
            time.sleep(5)
            quit_button.config(bg="black")
            inc_label.place_forget()
            stage_1_setup()

        stage_2_timer.cancel()
        if response != 0:
            choice_btn1.place_forget()
            choice_btn2.place_forget()
            left_response = stim[0]
            right_response = stim[1]
            print("Correct: " + str(correct))
            print("Response: " + str(response))
            print("Left: " + str(left_response))
            print("Right: " + str(right_response))
            if response == 1:
                response = 0
                if left_response == correct:
                    stage_2_correct += 1
                    print("Reinforcers:" + str(stage_2_correct))
                    reinforcement()
                    stage_1_setup()
                else:
                    incorrect()
            if response == 2:
                response = 0
                if right_response == correct:
                    stage_2_correct += 1
                    print("Reinforcers:" + str(stage_2_correct))
                    reinforcement()
                    stage_1_setup()
                else:
                    incorrect()
        else:
            stage_2_loop()
    increment = 0.01
    stage_2_timer = Timer(increment, stage_2_reloop)
    stage_2_timer.start()
def stage_2_loop():
    stage_2()


def exit_program():
    if sample_btn1.winfo_exists() or choice_btn1.winfo_exists():
        end_program()
    report()
def report():
    gui.destroy()
def end_program():
    global stage_1_timer, stage_2_timer, stage_3_timer
    #def outputs_off():
        #off(pellet)
    def gui_destroy():
        sample_btn1.destroy()
        choice_btn1.destroy()
        choice_btn2.destroy()
    try:
        stage_1_timer.cancel()
        stage_2_timer.cancel()
        outputs_off()
        gui.destroy()
    except NameError:
        outputs_off()
        gui_destroy()


def start():
    start_button.destroy()
    blackout_timer = Timer(Blackout * 60, stage_1_setup)
    blackout_timer.start()

# GUI for pig interface
gui = tk.Tk()
gui.configure(bg="black", cursor="none")
gui.state('zoomed')

screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()

start_button = tk.Button(gui, text="START", font=("bold", "40"), command=lambda: start())
start_button.place(relheight=1, relwidth=1, relx=1, rely=0, anchor="ne")

sample_btn1 = tk.Button(gui, bg="white", activebackground="white", command=lambda: press(1))
choice_btn1 = tk.Button(gui, bg="white", activebackground="white", command=lambda: press(1))
choice_btn2 = tk.Button(gui, bg="white", activebackground="white", command=lambda: press(2))
inc_label = tk.Label(gui, bg="white")

#img1 = Image.open("shape1.tif")
#img1 = img1.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)

img1 = Image.open("shape1.jpg")
img1 = img1.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(img1)

img2 = Image.open("shape2.jpg")
img2 = img2.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img2)

img3 = Image.open("shape3.jpg")
img3 = img3.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(img3)

img4 = Image.open("shape4.jpg")
img4 = img4.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img4 = ImageTk.PhotoImage(img4)

img5 = Image.open("shape5.jpg")
img5 = img5.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img5 = ImageTk.PhotoImage(img5)

img6 = Image.open("shape6.jpg")
img6 = img6.resize((int(screen_width*0.17), int(screen_height*0.3)), Image.ANTIALIAS)
img6 = ImageTk.PhotoImage(img6)

img_list = [(img1, img2), (img1, img3), (img1, img4), (img1, img5), (img1, img6),
            (img2, img3), (img2, img4), (img2, img5), (img2, img6),
            (img3, img4), (img3, img5), (img3, img6),
            (img4, img5), (img4, img6),
            (img5, img6)]

quit_button = tk.Button(gui, bg="black", bd=0, highlightthickness=0, command=lambda: exit_program())
quit_button.place(relheight=.15, relwidth=.1, relx=1, rely=.85, anchor="ne")
print('yo')
stage_1_setup()
print('dayo')
gui.overrideredirect(True)
gui.overrideredirect(False)
gui.attributes('-fullscreen', True)
gui.bind("<Control-q>", lambda x: exit_program())
gui.mainloop()
