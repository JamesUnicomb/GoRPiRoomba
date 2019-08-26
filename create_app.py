from flask import Flask
from create2_driver import Create2Driver
from create2 import *
import time

app    = Flask(__name__)
create = Create2Driver(serial_port = '/dev/serial0',
                       brc_pin     = 17)
create.start()
create.full()

@app.route('/start', methods=['GET'])
def _startRoomba():
    create.start()
    return 'srarting roomba ...'

@app.route('/stop', methods=['GET'])
def _stopRoomba():
    create.stop()
    return 'stopping roomba ...'

@app.route('/reset', methods=['GET'])
def _restart():
    create.reset()
    return 'restarting roomba ...'

@app.route('/power', methods=['GET'])
def _power():
    create.power()
    return 'powering down ...'

@app.route('/cleanRoom', methods=['GET'])
def _cleanRoom():
    create.safe()
    time.sleep(0.5)
    create.clean()
    return 'cleaning room ...'

@app.route('/dock', methods=['GET'])
def _dockRoomba():
    create.seek_dock()
    time.sleep(2.0)
    create.seek_dock()
    return 'going to charge dock ...'

@app.route('/drive', methods=['GET'])
def _driveRoomba():
    create.full()
    time.sleep(0.4)
    create.drive_direct(100,100)
    time.sleep(2.0)
    create.drive_direct(0,0)
    return 'driving ...'

if __name__ == '__main__':    
   app.run(debug=True, host='0.0.0.0', port=8000)
