import RPi.GPIO as GPIO
import time
import pyttsx3

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

#text-to-speech setup
engine = pyttsx3.init()
#engine.setProperty('rate', 125)     #change rate of speech, uncomment if needed
#engine.setProperty('volume',1.0)    #change volume of speech, uncomment if needed

#setting miscellaneous stuff
servo_open_position = 90
servo_closed_position = 0

#setServoAngle in degrees (2.5 duty cycle is 0 position)
def setServoAngle(angle):
    duty = (angle/18) + 2.5
    print("turning to angle")
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    pwm.ChangeDutyCycle((servo_closed_position/18) + 2.5)
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

# grants access to individual named "name";
# turns on green LED, runs servo to open position, and says "Access granted"
# turns LEDs off and runs servo to closed position 1 second later
def grantAccess(name):
    print("Granting access to " + name)
    LED_power([False, True])
    engine.say("Access granted, ligma balls")
    engine.runAndWait()
    setServoAngle(servo_open_position) #this statement has a 1 second delay builtin
    LED_power([False, False])
    
grantAccess("Ligma")