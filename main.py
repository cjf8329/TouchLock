from fingerprint_module import fingerprint_sensor
from email_module import Emailer
from servo_module import Servo
from LED_module import LEDs
from picamera import PiCamera
import time
import pyttsx3


class TouchLock:

    def __init__(self):
        print("initializing")
		# initializing fingerprint scanner
        self.scanner = fingerprint_sensor()
        
        # initializing picamera, starting early since this can take a few seconds
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.start_preview()
        

        # creating email sender
        email_address = "touchlock.biolock@gmail.com"
        password = "igxvftioggpjopgg"
        self.recipient = "cjf8329@nyu.edu" #for proof-of-concept
        self.emailer = Emailer(email_address, password)

        # creating servo
        self.servo_open_position = 90
        self.servo_timing = 3
        servo_pin = 17
        frequency = 50
        servo_closed_position = 0
        self.servo = Servo(servo_pin, frequency, servo_closed_position)

        # creating LED module (NOTE: these are the standalone LED bulbs, not the builtin LEDs inside of the fingerprint scanner
        red_LED_pin = 27
        green_LED_pin = 22
        self.LEDs = LEDs(red_LED_pin, green_LED_pin)

        # text-to-speech setup
        self.engine = pyttsx3.init()
        #engine.setProperty('rate', 125)     #change rate of speech, uncomment if needed
        #engine.setProperty('volume',1.0)    #change volume of speech, uncomment if needed

    # grants access to individual named "name";
    # turns on green LED, runs servo to open position, and tts says "Access granted"
    # turns LEDs off and runs servo to closed position 3 seconds later
    def grantAccess(self, name):
        print("Granting access to " + name)
        self.emailer.create_email(f"{name} has been authorized by TouchLock", self.recipient) # TODO: Take picture with picamera and attach here using optional argument "attachment"
        self.LEDs.LED_power([False, True])
        self.engine.say(f"Access granted, {name}")
        self.engine.runAndWait()
        self.servo.set_angle(self.servo_open_position, self.servo_timing)
        self.LEDs.LED_power([False, False])

    # denies access to user
    # turns on red LED, servo stays closed, and tts says "Access denied"
    # turns LEDs off 3 seconds later
    def denyAccess(self):
        print("Denying access")
        self.camera.capture("unauthorized.png")
        self.emailer.create_email("Unauthorized TouchLock user", self.recipient, attachment="unauthorized.png") # TODO: Take picture with picamera and attach here using optional argument "attachment"
        self.LEDs.LED_power([True, False])
        self.engine.say("Access denied")
        self.engine.runAndWait()
        self.emailer.send_email()
        time.sleep(self.servo_timing)
        self.LEDs.LED_power([False, False])

    # main loop
    def main_loop(self):
        while True:
            if not(self.scanner.in_use()):
                continue
            id = self.scanner.get_fingerprint_supress()
            if (not(id)):
                self.denyAccess()
                continue
            else:
                name = self.scanner.names[id]
                self.grantAccess(name)


mainTouchLock = TouchLock()
mainTouchLock.main_loop()
