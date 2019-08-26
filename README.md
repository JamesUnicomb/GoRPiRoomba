# GoRPiRoomba
## A Google Assitant activated Roomba that swears

## The Finished Product
[![IThe swearing Roomba](https://www.youtube.com/watch?v=o8MG2z378pQ)](https://www.youtube.com/watch?v=o8MG2z378pQ)

## The Parts

### Raspberry Pi
Any model Pi with wi-fi will work. I decided to use the 3 B+ I had spare.

### Shield
A generic Raspberry Pi shield will work.

### DIN Cable
To communicate with the iRobot Create a 7-pin DIN cable can be purchased.

### Buck Converter
A buck converter to step down the voltage to 5V is necessary.

### Logic Converter
The Raspberry Pi needs a logic level converter to

<p float="center">
<img src="https://github.com/JamesUnicomb/GoRPiRoomba/blob/master/parts/RPi_shield_0.JPG" width="240" />
</p>

## The Code
### cleanApp.py
This runs a web server that responds to cleaning and docking commands.

### swearingRoombaApp.py
This runs a web server that enables the Roomba to drive around and swear.

