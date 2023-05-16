from time import sleep
import RPi.GPIO as gp
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import serial

gp.cleanup()
gp.setmode(gp.BCM)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

chan0 = AnalogIn(ads, ADS.P0)
chan3 = AnalogIn(ads, ADS.P3)


gp.setup(13,gp.OUT)
gp.setup(12,gp.OUT)
gp.setup(1, gp.OUT)

pwm1 = gp.PWM(13, 100)
pwm2 = gp.PWM(12, 100)
pwm3 = gp.PWM(1, 100)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)

while True:
    chan0perc = 100* (chan0.value - 26000) / (40 - 26000 )
    chan0lightint = (100 - chan0perc)
    chan3moist = 100* (chan3.value - 32000) / (15400 - 31500)
    print('LDR VAL0: ', chan0.value)
    print('LDR PERCENT0: ', chan0perc)
    print('CHAN0LIGHT INTENSITY', chan0lightint)
    print('CHAN3 WETRAW', chan3.value)
    print('CHAN3 PERC', chan3moist)
   
    pwm3.ChangeDutyCycle(100)

    if chan0lightint > 20:
        pwm1.ChangeDutyCycle(chan0lightint)
        pwm2.ChangeDutyCycle(chan0lightint)

    else:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
    sleep(1)

pwm1.stop()
pwm2.stop()
gp.cleanup()
