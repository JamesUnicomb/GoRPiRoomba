from flask import Flask
from create2_driver import Create2Driver
from create2 import *
import time

#
# run a web server that takes in commands (a webhook)
# from the google home mini.
#
app    = Flask(__name__)

#
# create is a a class that uses the serial port
# on the raspberry pi to communicate.
#
create = Create2Driver(serial_port = '/dev/serial0',
                       brc_pin     = 17)
create.start()
create.full()


@app.route('/start', methods=['GET'])
def _startRoomba():
    #
    #   puts the roomba into start mode.
    #
    create.start()
    return 'srarting roomba ...'


@app.route('/stop', methods=['GET'])
def _stopRoomba():
    #
    #    stops the roomba from cleaning.
    #
    create.stop()
    return 'stopping roomba ...'


@app.route('/reset', methods=['GET'])
def _restart():
    #
    #   resets the roomba.
    #   this has the same effect as removing
    #   and reinserting the battery from the roomba.
    #
    create.reset()
    return 'restarting roomba ...'

@app.route('/power', methods=['GET'])
def _power():
    #
    # powers down the roomba.
    #
    create.power()
    return 'powering down ...'

@app.route('/cleanRoom', methods=['GET'])
def _cleanRoom():
    #
    # puts the roomba into cleaning mode.
    #
    create.safe()
    time.sleep(0.5)
    create.clean()
    return 'cleaning room ...'

@app.route('/dock', methods=['GET'])
def _dockRoomba():
    #
    # roomba searches for dock and begins
    # charging.
    #
    create.seek_dock()
    return 'going to charge dock ...'

if __name__ == '__main__':    
   app.run(debug=True, host='0.0.0.0', port=8000)
