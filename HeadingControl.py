import tkinter as tk
from tkinter import *
import pymavlink
from pymavlink import mavutil
from pymavlink.dialects.v20 import common as mavlink
import struct
import array
import time
import os
import sys
import math

mav = mavutil.mavlink_connection('udp::14540')
print(mav.address)
mav.wait_heartbeat()
print('heartbeat from system (system %u component %u)' %(mav.target_system, mav.target_component))
print('')
print('Enter all three fields in the user interface and press send')
print('Open the PX4 shell and type \'commander takeoff\' to launch the drone')

# Running bool is used to make sure the entry bar only takes data when the
# user tells it to
running = False

# Wait bool is used to stop the drone from sending a heading of 0 when the
# program starts
wait = True

global h
h = "0"
global alt
alt = "0"
global vel
vel = "0"
# initialize position parameters
global x
x = 0
global y
y = 0

def Send():
    global running
    if running:
        global h
        if heading.get() != "":
            h = heading.get()
        global alt
        if altitude.get() != "":
            alt = altitude.get()
        global vel
        if velocity.get() != "":
            vel = velocity.get()

        # Clear entry spaces
        heading.set("")
        altitude.set("")
        velocity.set("")

        running = False

    if float(alt) > 100:
        alt = 100
    if float(alt) < 0:
        alt = 0
    if float(vel) > 10:
        vel = 10
    if float(vel) < 0:
        h = float(h) + 180
        if float(vel) <-10:
            vel = -10
        vel = float(vel)*-1

    while float(h) < 0:
        h = float(h)+360
    while float(h) > 360:
        h = float(h)-360

    dir = float(h)*3.14159/180
    a = float(alt)
    v = float(vel)

    global wait
    if not wait:
        if dir >= 0:
            mav.mav.manual_control_send(
                mav.target_system, # target_system
                int(dir*1000),  # Heading in radians * 1000
                int(a*1000),    # Altitude in meters * 1000
                int(v*1000),    # Velocity in m/s * 1000
                int(0), # r
                int(0)  # buttons
            )
    else:
        mav.mav.manual_control_send(
            mav.target_system, # target_system
            int(0), # x
            int(0), # y
            int(0), # z
            int(0), # r
            int(0)  # buttons
        )
    root.after(5, Send)

#Set running to true and wait to false.
#This function runs when the send heading button is pressed
#Running is set to true so the main loop knows to repeatedly send the heading
#and  wait is set to false so the widget knows to grab whatever is
#in the entry bar
def start():
    global running
    running = True
    global wait
    wait = False
# Define the GUI
root = tk.Tk()
root.title("PX4 Heading Control")
root.geometry('300x85')

#Define the input
heading = tk.StringVar()
altitude = tk.StringVar()
velocity = tk.StringVar()

#Add widgets to the GUI
heading_label = tk.Label(root, text='Heading', font=('calibre',10,'bold'))
heading_entry = tk.Entry(root, textvariable=heading, font=('calibre',10,'normal'))
altitude_label = tk.Label(root, text='Altitude', font=('calibre',10,'bold'))
altitude_entry = tk.Entry(root, textvariable=altitude, font=('calibre',10,'normal'))
velocity_label = tk.Label(root, text='Velocity', font=('calibre',10,'bold'))
velocity_entry = tk.Entry(root, textvariable=velocity, font=('calibre',10,'normal'))
submit_btn = tk.Button(root, text='Send', command = start)

#Adjust the layout
heading_label.grid(row = 1, column = 0)
heading_entry.grid(row = 1, column = 1)
altitude_label.grid(row = 2, column = 0)
altitude_entry.grid(row = 2, column = 1)
velocity_label.grid(row = 3, column = 0)
velocity_entry.grid(row = 3, column = 1)
submit_btn.grid(row = 2, column = 2)

#Run the GUI
root.after(20, Send)
root.mainloop()
