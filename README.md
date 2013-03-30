RASM
====

[r]aspberry pi -> [a]rduino -> [s]tepper [m]otors (library to controll the hardware stack)

## Goal
The goal of this repository is it to create a simple plotter - along the lines of [Der Kritzler](http://tinkerlog.com/2011/09/02/der-kritzler/).

## Hardware
* Raspberry Pi (thank you PyCon 2013 for this AWESOME gift :-)
* Arduino Uno
* 1 x Adafruit Motor/Stepper/Servo Shield for Arduino kit (v1.2) [ID:81]
* 2 x Stepper motor - 200 steps/rev, 12V 350mA[ID:324]
* 2 x Aluminum GT2 Timing Pulley - 6mm Belt - 36 Tooth - 5mm Bore[ID:1253]
* & lots of cables

## Communication
The raspberry pi talks via USB to the arduino on a serial connection. At this point all that the arduino understands are simple messages explicetly for the stepper motors. Since I wanted to get a working prototype fast I wrote as little code as possible to get everything working.

message format: <motor>,<speed>,<steps>,<direction>,<step-style>;
e.g.: 1,100,50,1,1;
-> motor 1 moves 50 steps with speed 100 "forward" in "single"-style.

values: 
motor: 1,2
speed: 1 - 250 (for me - above that my arduino has power-issues - might have to put a direct power supply in for the motor shield)
steps: 1 - ∞
direction: 1(forward), 2(backward)
step-style: 1 (single), 2 (double), 3 (interleave), 4 (microsteps)


## top layer
Using pyserial, flask and processing.js I want to build a small webserver that accepts vertor images and then directs the stepper motors to draw the image.
