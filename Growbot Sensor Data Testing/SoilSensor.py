import time
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

A1 = 40
A2 = 37
sleep = 38
B2 = 35
B1 = 36
fault = 33
pins = [A1, A2, B1, B2]

# step sequence
step = [(GPIO.HIGH, GPIO.LOW,  GPIO.HIGH, GPIO.LOW),
        (GPIO.LOW,  GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
        (GPIO.LOW,  GPIO.HIGH, GPIO.LOW,  GPIO.HIGH),
        (GPIO.HIGH, GPIO.LOW,  GPIO.LOW,  GPIO.HIGH)]

#home sensor setup
homeSensorPin = 30
GPIO.setup(homeSensorPin, GPIO.IN)

#Soil sensor connection and setup
soilAdr = 0x36
i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, soilAdr)

#number of steps to move sensor down from home
sensorSteps = 100

def read_soil():
    #all of the sensor reading stuff from adafruit
    time.sleep(1)
    touch = ss.moisture_read()
    temp = ss.get_temp()
    time.sleep(1)
    return touch, temp

def sensor_home():
    #motor up until home switch
    homeSensorState = GPIO.input(homeSensorPin)
    while (homeSensorState is True):
        homeSensorState = GPIO.input(homeSensorPin)

    #print("Homing sensor...\n")

def sensor_down():
    #move motor down X (value determined from testing) to go into soil, then read_soil
    sensor_home()

    # enable driver
    GPIO.output(sleep, GPIO.HIGH)

    # start stepping
    for s in range(sensorSteps):
        i = s % 4
        # step motor
        GPIO.output(pins, step[i])
        time.sleep(0.01)

    print("Deploying the sensor...\n")

# while True:
#     print(read_soil())
#     time.sleep(5)