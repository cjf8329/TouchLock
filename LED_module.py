import RPi.GPIO as GPIO

class LEDs:

    def __init__(self, red_pin, green_pin):
        self.red_LED_pin = red_pin
        self.green_LED_pin = green_pin
        GPIO.setup(self.red_LED_pin, GPIO.OUT)
        GPIO.setup(self.green_LED_pin, GPIO.OUT)

    #changes LED states, state is a list in the format [red_state, green_state],
    #where red_state and green_state are boolean values
    def LED_power(self, state):
        if state[0]:
            GPIO.output(self.red_LED_pin, True)
        else:
            GPIO.output(self.red_LED_pin, False)
        if state[1]:
            GPIO.output(self.green_LED_pin, True)
        else:
            GPIO.output(self.green_LED_pin, False)

