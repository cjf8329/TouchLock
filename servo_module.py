import RPi.GPIO as GPIO
import time


class Servo:

    def __init__(self, servo_pin, frequency, closed_positon):
        self.pin = servo_pin
        self.servo_closed_position = closed_positon
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, frequency)
        self.pwm.start(0)

    def set_angle(self, angle, servo_timing):
        duty = (angle/18) + 2.5
        print("turning to angle")
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(servo_timing)
        self.pwm.ChangeDutyCycle((self.servo_closed_position/18) + 2.5)
        time.sleep(servo_timing)
        self.pwm.stop()

