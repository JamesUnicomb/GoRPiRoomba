#
# Module to control the Create2 using the serial interface
#

import serial
import struct
import time
from create2 import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM); GPIO.setwarnings(False)

class Create2Driver:
    # Class to control the iRobot Create2 robot.
    def __init__(self,
                 serial_port,
                 brc_pin=None,
                 baudrate=115200):
        # Constructor.
        #
        # Args:
        #    serial_port (string): device file for the serial port.
        #    brc_pin (integer): GPIO pin number for the BRC pin used to wake the Create2 up. Use None if not
        #                       connected.
        #
        if brc_pin is not None:
            # Pulse the BRC pin to wake up Create
            GPIO.setup(brc_pin, GPIO.OUT)
            GPIO.output(brc_pin, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(brc_pin, GPIO.LOW)
            time.sleep(0.02)
            GPIO.output(brc_pin, GPIO.HIGH)
            # Wait until ready
            time.sleep(0.4)
        self._connection = serial.Serial(serial_port, baudrate=baudrate, timeout=1.)
        self._buffer = bytes()

    def start(self):
        #
        # This command starts the OI. You must always send the Start command before sending any other commands to the OI.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        # Roomba beeps once to acknowledge it is starting from "off" mode.
        #
        self._send(">B", (Op.Start,))
        time.sleep(0.02)  # wait ~20ms for mode changes

    def reset(self):
        #
        # This command resets the robot, as if you had removed and reinserted the battery.
        #
        # Available in modes: Always available; Changes mode to: Off.
        #
        # You will have to call start() again to re-enter Open Interface mode.
        #
        self._send(">B", (Op.Reset,))

    def stop(self):
        #
        # This command stops the OI. All streams will stop and the robot will no longer respond to commands.
        # Use this command when you are finished working with the robot.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Off. Roomba plays a song to acknowledge it is exiting the OI.
        #
        self._send(">B", (Op.Stop,))
        time.sleep(0.02)  # wait ~20ms for mode changes

    def safe(self):
        #
        # This command puts the OI into Safe mode, enabling user control of Roomba. It turns off all LEDs. The OI
        # can be in Passive, Safe, or Full mode to accept this command. If a safety condition occurs Roomba reverts automatically to Passive mode.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Safe.
        #
        self._send(">B", (Op.Safe,))
        time.sleep(0.02)  # wait ~20ms for mode changes

    def full(self):
        #
        # This command gives you complete control over Roomba by putting the OI into Full mode, and turning off
        # the cliff, wheel-drop and internal charger safety features. That is, in Full mode, Roomba executes any
        # command that you send it, even if the internal charger is plugged in, or command triggers a cliff or wheel
        # drop condition.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Full.
        #
        # Note: Use start() to change the mode to Passive.
        #
        self._send(">B", (Op.Full,))
        time.sleep(0.02)  # wait ~20ms for mode changes

    def power(self):
        #
        # This command powers down Roomba. The OI can be in Passive, Safe, or Full mode to accept this
        # command.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        self._send(">B", (Op.Power,))
        time.sleep(0.02)  # wait ~20ms for mode changes

    def clean(self):
        #
        # This command starts the default cleaning mode. This is the same as pressing Roomba's Clean button,
        # and will pause a cleaning cycle if one is already in progress.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        self._send(">B", (Op.Clean,))

    def max(self):
        #
        # This command starts the Max cleaning mode, which will clean until the battery is dead. This command
        # will pause a cleaning cycle if one is already in progress.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        self._send(">B", (Op.Max,))

    def spot(self):
        #
        # This command starts the Spot cleaning mode. This is the same as pressing Roomba's Spot button, and
        # will pause a cleaning cycle if one is already in progress.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        self._send(">B", (Op.Spot,))

    def seek_dock(self):
        #
        # This command directs Roomba to drive onto the dock the next time it encounters the docking beams.
        # This is the same as pressing Roomba's Dock button, and will pause a cleaning cycle if one is already in
        # progress.
        #
        # Available in modes: Passive, Safe, or Full; Changes mode to: Passive.
        #
        self._send(">B", (Op.SeekDock,))

    def drive(self, velocity_in_mm_per_sec, radius_in_mm):
        #
        # This command controls Roomba's drive wheels.
        #
        # Note: Internal and environmental restrictions may prevent Roomba from accurately carrying out some drive
        # commands. For example, it may not be possible for Roomba to drive at full speed in an arc with a large
        # radius of curvature.
        #
        # Available in modes: Safe or Full; Changes mode to: No Change.
        #
        #Args:
        #    velocity_in_mm_per_sec (integer): -500 - 500 mm/sec. Positive value mean forward and negative backwards.
        #    radius_in_mm (integer): -2000 - 2000 mm.
        #        The radius is measured from the center of the turning circle to the center of Roomba.
        #        Special cases:
        #        * 32768 or 32767: Go straight.
        #        * -1: Turn in place clockwise.
        #        * 1: Turn in place counterclockwise.
        #
        self._send(">Bhh", (Op.Drive, velocity_in_mm_per_sec, radius_in_mm))

    def drive_direct(self, right_wheel_velocity_in_mm_per_sec, left_wheel_velocity_in_mm_per_sec):
        #
        # This command lets you control the forward and backward motion of Roomba's drive wheels
        # independently.
        #
        # Available in modes: Safe or Full; Changes mode to: No Change.
        #
        # Args:
        #    right_wheel_velocity_in_mm_per_sec (integer): -500 - 500 mm.s. Positive means forward.
        #    left_wheel_velocity_in_mm_per_sec (integer): -500 - 500 mm/s. Positive means forward.
        #
        self._send(">Bhh", (Op.DriveDirect, right_wheel_velocity_in_mm_per_sec, left_wheel_velocity_in_mm_per_sec))

    def drive_pwm(self, right_pwm, left_pwm):
        #
        # This command lets you control the raw forward and backward motion of Roomba's drive wheels
        # independently.
        #
        # Available in modes: Safe or Full; Changes mode to: No Change
        #
        # Args:
        #    right_pwm (integer): -500 - 500. Positive means forward.
        #    left_pwm (integer): -500 - 500. Positive means forward.
        #
        self._send(">Bhh", (Op.DrivePwm, right_pwm, left_pwm))

    def motors(self, enable_side_brush, enable_vacuum, enable_main_brush,
               side_brush_clockwise=False, main_brush_outward=False):
        data = (main_brush_outward << 4) \
               | (side_brush_clockwise << 3) \
               | (enable_main_brush << 2) \
               | (enable_vacuum << 1) \
               | (enable_side_brush << 0)
        self._send(">BB", (Op.Motors, data))

    def pwm_motors(self, main_brush_pwm, side_brush_pwm, vacuum_pwm):
        self._send(">Bbbb", (Op.PwmMotors, main_brush_pwm, side_brush_pwm, vacuum_pwm))

    def leds(self, debris, spot, dock, check_robot, power_led_color, power_led_intensity):
        data = (check_robot << 3) \
               | (dock << 2) \
               | (spot << 1) \
               | (debris << 0)
        self._send(">BBBB", (Op.Leds, data, power_led_color, power_led_intensity))

    def digits_leds_ascii(self, data):
        data_all = data + b'    '
        self._send(">Bbbbb", (Op.DigitsLedsAscii, data_all[0], data_all[1], data_all[2], data_all[3]))
        
    def getBumpsAndWheelDrops(self):
        #
        # This function returns an array of bools corresponding to the bumpers being pressed.
        #
        self._connection.write(struct.pack(">Bb", Op.Sensors, Sensor.BumpsAndWheelDrops))
        timeout = time.time()
        while not(self._connection.inWaiting()):
            if time.time() - timeout > 0.2:
                return False
        d, = struct.unpack_from(">B", self._connection.read())
        rightBumper    = bool(d & 0x01)
        leftBumper     = bool(d & 0x02)
        rightWheelDrop = bool(d & 0x04)
        leftWheelDrop  = bool(d & 0x08)
        return leftWheelDrop, rightWheelDrop, leftBumper, rightBumper

    def getLightBumperArray(self):
        #
        # This function returns an array of bools corresponding to the bumpers being pressed.
        #
        self._connection.write(struct.pack(">Bb", Op.Sensors, Sensor.LightBumper))
        timeout = time.time()
        while not(self._connection.inWaiting()):
            if time.time() - timeout > 0.2:
                return False
        d, = struct.unpack_from(">B", self._connection.read())
        sideLeft    = bool(d & 0x01)
        frontLeft   = bool(d & 0x02)
        centerLeft  = bool(d & 0x04)
        centerRight = bool(d & 0x08)
        frontRight  = bool(d & 0x10)
        sideRight   = bool(d & 0x20)
        return sideLeft, frontLeft, centerLeft, centerRight, frontRight, sideRight

    def set_velocity(self, forward, turn, wheelBase = 0.235):
        #
        # A utility function for setting the wheel velocity from forward and angular velocity.
        #
        left_velocity  = forward + turn * wheelBase / 2.0
        right_velocity = forward - turn * wheelBase / 2.0
        self.drive_direct(int(1000*right_velocity), int(1000*left_velocity))

    def _send(self, fmt, data):
            command = struct.pack(fmt, *data)
            self._connection.write(command)
