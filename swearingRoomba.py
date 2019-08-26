from flask import Flask, Response
from threading import Thread
import time

import numpy as np

from create2_driver import Create2Driver
from create2 import *
from Sounds import playSound

app = Flask(__name__)
stop_run = False

create = Create2Driver(serial_port = '/dev/serial0',
                       brc_pin     = 17)
create.start()
create.full()

import atexit
def closeDown():
    create.drive_direct(0,0)
    create.stop()
    print 'shutting down ...'
atexit.register(closeDown)

def drive_and_swear(velocity_ = 0.3,
                    turn_     = 0.0,
                    sigma     = 0.025,
                    kappa     = 0.05,
                    ):
    global stop_run
    
    while not stop_run:
        leftWheel, rightWheel, leftBumper, rightBumper = create.getBumpsAndWheelDrops()
        
        velocity = velocity_
        turn     = turn_
        
        currentTime = time.time()
        time.sleep(0.02)
    
        while (not (leftBumper | rightBumper)) and (not stop_run):
            leftWheel, rightWheel, leftBumper, rightBumper = create.getBumpsAndWheelDrops()
            
            dt = time.time() - currentTime
            currentTime = time.time()
            
            turn += 1.0 / np.sqrt(dt) * sigma * np.random.randn() - kappa * turn
            turn  = np.clip(turn, -4.0, 4.0)
            
            create.set_velocity(velocity_, turn)
            
        velocity = 0.0; turn = 0.0
        create.set_velocity(velocity, turn)
        
        currentTime = time.time()
        while (not stop_run) and (time.time() - currentTime < 0.5):
            playSound()
            print 'sound played'
        
        currentTime = time.time()
        while (not stop_run) and (time.time() - currentTime < 0.25):
            velocity = -0.2; turn = 0.0
            create.set_velocity(velocity, turn)

        currentTime = time.time()
        turnTime = 0.001*np.random.randint(330, 2094)
        while (not stop_run) and (time.time() - currentTime < turnTime):
            velocity = 0.0; turn = 2.0
            create.set_velocity(velocity, turn)

        velocity = 0.0; turn = 0.0
        create.set_velocity(velocity, turn)
        time.sleep(0.5)
            

def manual_run():
    thread = Thread(target=drive_and_swear)
    thread.start()
    return 'Drive and Swear!!!'

@app.route('/stop', methods=['GET'])
def stop_run():
    global stop_run
    stop_run = True
    return 'Killing Roomba!!!'

@app.route('/driveAndSwear', methods=['GET'])
def run_process():
    global stop_run
    stop_run = False
    return Response(manual_run(), mimetype='text/html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000)
