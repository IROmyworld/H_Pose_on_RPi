import RPi.GPIO as GPIO
import time

# GPIO Pins available (BOARD numbering)
AvailPins = [12,11,13,15,16,18,29,31,33]

def LEDSetup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(AvailPins, GPIO.OUT, initial=False)
    print('LEDs are setup')

def LEDOutput(Angles,Athres):
    # Control LEDs
    # Athres is a 2 element array with the threshold to trigger the leds.
    GPIO.output(AvailPins, False)
    if Angles is not None:
        Npin = 0
        for a in Angles:
            a = abs(int(a))
            print(a)
            GPIO.output(AvailPins[Npin], True)
            if a > 5: GPIO.output(AvailPins[Npin+1], True)
            if a > 10: GPIO.output(AvailPins[Npin+2], True)
            Npin += 3

def LEDCleanUp():
    GPIO.cleanup()
    print('leds are cleaned up')

if __name__ == "__main__":
    LEDSetup()
    GPIO.output(AvailPins, True)
    RuntimeWarning('This module is not intended to be run as main, available Pins should have turned on')
    time.sleep(10)
    LEDCleanUp()
    

        
            
        
    
    
