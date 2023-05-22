#!/usr/bin/env python3
from tkinter import *
import tkinter.font as tkfont
import sys
import subprocess
from main import run


def run_main():
    print("ok1")
    terminate_process()  #Terminates subprocess p if p exists.
    global p   #Set p (the subprocess) as a global variable so that it can be terminated elsewhere in the code.
    left = eye_left_key.get()
    right = eye_right_key.get()
    blink = blink_key.get()
    freq_min = minimum_frequency.get()
    freq_max = maximum_frequency.get()
    model = model_selection.get()
    threshold = threshold_val.get()
    wink_threshold = wink_threshold_val.get()
    p = subprocess.Popen(['python','main.py',left,right,blink,freq_min,freq_max,model,threshold,wink_threshold], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("ok2")

def exit_func():
    terminate_process()
    sys.exit()

def terminate_process():
    try:
        p.terminate()
    except:
        pass

root = Tk()
root.title('Eye to Keyboard Setup Panel')
root.config(bg="#7c7c7c")
root.minsize(600,600)


############### TOP FRAME ###############
top_frame = Frame(root,width=600,height=60)
top_frame.pack(fill=BOTH)

title = Label(top_frame, text='Welcome to the Eye to Keyboard Setup Panel!',font=tkfont.Font(size=25))
title.pack(fill=BOTH,expand=True)


############### LEFT FRAME ###############
left_frame = Frame(root,width=295,height=540)
left_frame.pack(side=LEFT)


### Key Bindings ###
key_bindings = Frame(left_frame,width=270,height=200)
key_bindings.place(x=20,y=0)

keybinding_subtitle = Label(key_bindings, text='Key bindings', font=tkfont.Font(size=18))
keybinding_subtitle.place(x=5,y=0)

keybinding_left_eye_movement_label = Label(key_bindings,text='left:')
keybinding_left_eye_movement_label.place(x=20,y=40)

eye_left_key = StringVar()
eye_left_key_textbox = Entry(key_bindings,width=8,textvariable=eye_left_key)
eye_left_key_textbox.insert(0,'left')
eye_left_key_textbox.place(x=70,y=40)

keybinding_right_eye_movement_label = Label(key_bindings,text='right:')
keybinding_right_eye_movement_label.place(x=20,y=80)

eye_right_key = StringVar()
eye_right_key_textbox = Entry(key_bindings,width=8,textvariable=eye_right_key)
eye_right_key_textbox.insert(0,'right')
eye_right_key_textbox.place(x=70,y=80)

keybinding_blink_label = Label(key_bindings,text='blink:')
keybinding_blink_label.place(x=20,y=120)

blink_key = StringVar()
blink_key_textbox = Entry(key_bindings,width=8,textvariable=blink_key)
blink_key_textbox.insert(0,'up')
blink_key_textbox.place(x=70,y=120)


### Filter Settings ###
filter_frame = Frame(left_frame,width=270,height=200)
filter_frame.place(x=20,y=200)

filter_subtitle = Label(filter_frame,text='Filter Settings',font=tkfont.Font(size=18))
filter_subtitle.place(x=5,y=0)

min_freq_label = Label(filter_frame,text='Minimum frequency: ')
min_freq_label.place(x=5,y=40)

minimum_frequency = StringVar()
minimum_frequency_textbox = Entry(filter_frame,width=8,textvariable=minimum_frequency)
minimum_frequency_textbox.insert(0,'0')
minimum_frequency_textbox.place(x=70,y=75)

max_freq_label = Label(filter_frame,text='Maximum frequency: ')
max_freq_label.place(x=5,y=120)

maximum_frequency = StringVar()
maximum_frequency_textbox = Entry(filter_frame,width=8,textvariable=maximum_frequency)
maximum_frequency_textbox.insert(0,'12')
maximum_frequency_textbox.place(x=70,y=150)

############### RIGHT FRAME ###############
right_frame = Frame(root,width=295,height=540)
right_frame.pack(side=RIGHT)

### Model selection ###
model_selection_frame = Frame(right_frame,width=250,height=200)
model_selection_frame.place(x=20,y=0)

model_selection_label = Label(model_selection_frame,text='Classifier model',font=tkfont.Font(size=18))
model_selection_label.place(x=5,y=0)

model_selection = StringVar()
simple_selector = Radiobutton(model_selection_frame, text='Simple',variable=model_selection,value='simple')
simple_selector.place(x=40,y=35)
knn_selector = Radiobutton(model_selection_frame, text='KNN',variable=model_selection,value='knn')
knn_selector.place(x=40,y=70)
svm_selector = Radiobutton(model_selection_frame, text='SVM',variable=model_selection,value='svm')
svm_selector.place(x=40,y=105)
lda_selector = Radiobutton(model_selection_frame, text='LDA',variable=model_selection,value='lda')
lda_selector.place(x=40,y=140)
ann_selector = Radiobutton(model_selection_frame, text='ANN',variable=model_selection,value='ann')
ann_selector.place(x=40,y=175)

simple_selector.select()


### Set Threshold ###
set_threshold_frame = Frame(right_frame, width=300,height=200)
set_threshold_frame.place(x=20,y=215)

set_threshold_subtitle = Label(set_threshold_frame, text='Set Threshold (for simple model)', font=tkfont.Font(size=18))
set_threshold_subtitle.place(x=0,y=0)

set_threshold_label = Label(set_threshold_frame,text='Normal eye movement threshold: ')
set_threshold_label.place(x=5,y=40)

threshold_val = StringVar()
set_threshold_textbox = Entry(set_threshold_frame,width=8,textvariable=threshold_val)
set_threshold_textbox.insert(0,'30')
set_threshold_textbox.place(x=70,y=75)

set_wink_threshold_label = Label(set_threshold_frame,text='Wink threshold: ')
set_wink_threshold_label.place(x=5,y=120)

wink_threshold_val = StringVar()
set_wink_threshold_textbox = Entry(set_threshold_frame,width=8,textvariable=wink_threshold_val)
set_wink_threshold_textbox.insert(0,'150')
set_wink_threshold_textbox.place(x=70,y=150)


### Buttons ###
buttons_frame = Frame(right_frame,width=295,height=70)
buttons_frame.place(x=0, y=500)

runButton = Button(buttons_frame,text='Run!',command=run_main)
runButton.place(x=30,y=0)

stopButton = Button(buttons_frame, text='Terminate',command=terminate_process)
stopButton.place(x=100,y=0)

quitButton = Button(buttons_frame,text='Quit',command=exit_func)
quitButton.place(x=210,y=0)


root.mainloop()
