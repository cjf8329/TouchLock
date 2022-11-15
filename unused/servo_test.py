import RPi.GPIO as GPIO
import time

pin = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)

pwm=GPIO.PWM(pin, 50)
pwm.start(0)

time.sleep(1)

def SetAngle(angle):
    duty = (angle/18) + 2.5
    print("turning to angle")
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.stop()

    
SetAngle(90)

