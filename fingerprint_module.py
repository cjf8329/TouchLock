import time
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial
import pickle

# no parameters are passed on class creation, it is assumed that UART via GPIO is used for sensor communication
class fingerprint_sensor:

    # initial setup, see inner comments for more detail
    def __init__(self):

        # setup sensor LEDs
        self.led = DigitalInOut(board.D13)
        self.led.direction = Direction.OUTPUT

        # setup serial communication over GPIO using UART
        # DONE: Check the adafruit docs to see if these uart values are right for our sensor later (It's 57600)
        self.baud = 57600
        self.uart = serial.Serial("/dev/ttyS0", baudrate=self.baud, timeout=1)

        # create scanner instance
        self.scanner = adafruit_fingerprint.Adafruit_Fingerprint(self.uart)

        # open pickled name list
        with open("names", "rb") as f:
            self.names = pickle.load(f)

        #make sure list of len() 127 has been initialized
        try:
            if (len(self.names) != 127):
                names = [None] * 127
                self.pickle_names()
        except:
            names = [None] * 127
            self.pickle_names()

    # scan fingerprint with detailed output
    def get_fingerprint_verbose(self):
        print("Place finger on scanner")
        while (self.scanner.get_image() == adafruit_fingerprint.NOFINGER):
            pass
        print("Scanning...", end="")
        i = self.scanner.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
        else:
            if i == adafruit_fingerprint.NOFINGER:
                print("No finger detected")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
            else:
                print("Other error")
            return False

        print("Templating...", end="")
        i = self.scanner.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        print("Searching...", end="")
        i = self.scanner.finger_fast_search()


        if i == adafruit_fingerprint.OK:
            print("Found fingerprint!")
            return True
        else:
            if i == adafruit_fingerprint.NOTFOUND:
                print("No match found")
            else:
                print("Other error")
            return False

    # scan fingerprint with simple output
    def get_fingerprint_simple(self):
        print("Place finger on scanner")
        while (self.scanner.get_image() == adafruit_fingerprint.NOFINGER):
            pass
        print("Scanning...", end="")
        i = self.scanner.get_image()
        if i == adafruit_fingerprint.OK:
            print("Image taken")
        else:
            print("Scanning failed")
            return False

        print("Templating...", end="")
        i = self.scanner.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            print("Templating failed")
            return False

        print("Searching...", end="")
        i = self.scanner.finger_fast_search()


        if i == adafruit_fingerprint.OK:
            print("Found fingerprint!")
            return True
        else:
            print("searching failed")
            return False
            
    # scan fingerprint and only return ID without console output
    def get_fingerprint_supress(self):
        while (self.scanner.get_image() == adafruit_fingerprint.NOFINGER):
            pass
        i = self.scanner.get_image()
        if i == adafruit_fingerprint.OK:
            pass
        else:
            return False

        i = self.scanner.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            pass
        else:
            return False

        i = self.scanner.finger_fast_search()


        if i == adafruit_fingerprint.OK:
            print(self.scanner.finger_id)
            return self.scanner.finger_id
        else:
            return False

    # enroll fingerprint with detailed output
    def enroll_finger_verbose(self, location):
        #takes two images of a fingerprint and templates
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                print("Place finger on sensor...", end="")
            else:
                print("Place same finger again...", end="")

            while True:
                i = self.scanner.get_image()
                if i == adafruit_fingerprint.OK:
                    print("Image taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print(".", end="")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    print("Imaging error")
                    return False
                else:
                    print("Other error")
                    return False

            print("Templating...", end="")
            i = self.scanner.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Templated")
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    print("Image too messy")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    print("Could not identify features")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    print("Image invalid")
                else:
                    print("Other error")
                return False

            if fingerimg == 1:
                print("Remove finger")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.scanner.get_image()

        print("Creating model...", end="")
        i = self.scanner.create_model()
        if i == adafruit_fingerprint.OK:
            print("Created")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                print("Prints did not match")
            else:
                print("Other error")
            return False

        print("Storing model #%d..." % location, end="")
        input_name = input("Enter associated name \n>")
        self.names[location] = input_name
        self.pickle_names()
        i = self.scanner.store_model(location)
        if i == adafruit_fingerprint.OK:
            print("Stored")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                print("Bad storage location")
            elif i == adafruit_fingerprint.FLASHERR:
                print("Flash storage error")
            else:
                print("Other error")
            return False

        return True

    # enroll fingerprint with simple output
    def enroll_finger_simple(self, location):
        #takes two images of a fingerprint and templates
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                print("Place finger on sensor...", end="")
            else:
                print("Place same finger again...", end="")

            while True:
                i = self.scanner.get_image()
                if i == adafruit_fingerprint.OK:
                    print("Image taken")
                    break
                elif i == adafruit_fingerprint.NOFINGER:
                    print(".", end="")
                    continue
                return False

            print("Templating...", end="")
            i = self.scanner.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Templated")
            else:
                print("Templating failed")
                return False

            if fingerimg == 1:
                print("Remove finger")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.scanner.get_image()

        print("Modelling...", end="")
        i = self.scanner.create_model()
        if i == adafruit_fingerprint.OK:
            print("Modelled")
        else:
            print("Modelling failed")
            return False

        print("Storing model #%d..." % location, end="")
        input_name = input("Enter associated name \n>")
        self.names[location] = input_name
        self.pickle_names()
        i = self.scanner.store_model(location)
        if i == adafruit_fingerprint.OK:
            print("Stored")
        else:
            print("Storing failed")
            return False

        return True

    def in_use(self):
        if self.scanner.get_image() == adafruit_fingerprint.NOFINGER:
            return False
        else:
            return True

    # remove all stored fingerprints
    def delete_all(self):
        print("Deleting...", end="")
        self.names = [None] * 127
        self.pickle_names()
        for x in range(1,128):
            self.scanner.delete_model(x)
        print("done")

    def pickle_names(self):
        with open("names", "wb") as f:
            pickle.dump(self.names, f)

    # prompt user for number indicating fingerprint storage location
    def get_num(self):
        i = 0
        # Up to 127 fingerprint images may be enrolled at once on fingerprint scanner flash memory
        while (i > 127) or (i < 1):
            try:
                i = int(input("Enter ID # from 1-127: "))
            except ValueError:
                pass
        return i

    # modified official test driver code for enrolling and testing fingerprints/sensor
    def adafruit_test_driver(self):
        print("Running fingerprint sensor setup\n")
        while True:
            print("----------------")
            if self.scanner.read_templates() != adafruit_fingerprint.OK:
                raise RuntimeError("Failed to read templates")
            print("Fingerprint templates:", self.scanner.templates)
            print("d) delete all fingerprints")
            print("e) enroll print")
            print("f) find print")
            print("z) end setup")
            print("----------------")
            c = input("> ")

            # by default, use simple output
            if c == "d":
                self.delete_all()
            if c == "e":
                self.enroll_finger_simple(self.get_num())
            if c == "f":
                if self.get_fingerprint_simple():
                    print("Detected #", self.scanner.finger_id)
                else:
                    print("Detection unsuccessful")
            if c == "z":
                print("ending setup")
                break

            # alternatively, enter ev or fv for verbose output
            if c == "ev":
                self.enroll_finger_verbose(self.get_num())
            if c == "fv":
                if self.get_fingerprint_verbose():
                    print("Detected #", self.scanner.finger_id, "with confidence", self.scanner.confidence)
                else:
                    print("Detection unsuccessful")
