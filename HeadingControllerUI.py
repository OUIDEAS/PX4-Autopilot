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

mav = mavutil.mavlink_connection('udp::14540')
print(mav.address)
mav.wait_heartbeat()
print('heartbeat from system (system %u component %u)' %(mav.target_system, mav.target_system))

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

    dir = int(float(h)*100)
    a = int(float(alt)*1000)
    v = int(float(vel)*100)
    # send controller input to bypass the failsafe
    mav.mav.manual_control_send(
        mav.target_system, # target_system
        int(0), # x
        int(0), # y
        int(0), # z
        int(0), # r
        int(0)  # buttons
    )
    global wait
    if not wait:
        if dir >= 0:
            mav.mav.adsb_vehicle_send(
                int(37), #ICAO address
                int(0),#lat * 1e7),
                int(0),#lng*1e7),
                mavutil.mavlink.ADSB_ALTITUDE_TYPE_PRESSURE_QNH,
                int(a),#here.alt*1000+10000),
                int(dir), #heading in degrees
                int(v), #horizontal velocity
                int(0), #vertical velocity
                "bob".encode("ascii"),
                mavutil.mavlink.ADSB_EMITTER_TYPE_LIGHT,
                int(1), #time since last communication
                int(4),
                int(2002)
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
