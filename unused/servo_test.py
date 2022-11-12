import RPi.GPIO as GPIO
import time

pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)


pwm=GPIO.PWM(pin, 50)
pwm.start(0)

time.sleep(1)

def SetAngle(angle):
    duty = (angle/18) + 2.5
    print("turning to angle")
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.stop()

    
SetAngle(90)

