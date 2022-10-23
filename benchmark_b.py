import RPi.GPIO as GPIO
import time

#declaring pins
servo_pin = 11
red_LED_pin = 13
green_LED_pin = 15

#setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(red_LED_pin, GPIO.OUT)
GPIO.setup(green_LED_pin, GPIO.OUT)

#setting up PWM
pwm=GPIO.PWM(servo_pin, 50)
pwm.start(0)


#setServoAngle in degrees (2.5 duty cycle is 0 position)
def setServoAngle(angle):
    duty = (angle/18) + 2.5
    print("turning to angle")
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.stop()

#changes LED states, state is a list in the format [red_state, green_state],
#where red_state and green_state are boolean values
def LED_power(state):
    if (state[0]):
        GPIO.output(red_LED_pin, True)
    else:
        GPIO.output(red_LED_pin, False)
    if (state[1]):
        GPIO.output(green_LED_pin, True)
    else:
        GPIO.output(green_LED_pin, False)

def grantAccess(name):
    print("Granting access to " + name)
    LED_power([False, True])
    setServoAngle(90) #this statement has a 1 second delay builtin
    LED_power([False, False])
    