import time
import RPi.GPIO as GPIO

RUNNING = True
red = 17
green = 18
blue = 27

class LED:
    def __init__(self, pRedPin, pGreenPin, pBluePin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pRedPin, GPIO.OUT)
        GPIO.setup(pGreenPin, GPIO.OUT)
        GPIO.setup(pBluePin, GPIO.OUT)
        Freq = 100 #Hz
        self.red = GPIO.PWM(pRedPin, Freq)
        self.red.start(100)
        self.green = GPIO.PWM(pGreenPin, Freq)
        self.green.start(100)
        self.blue = GPIO.PWM(pBluePin, Freq)
        self.blue.start(100)

    def setColor(self, pR, pG, pB):
        r = 100 - round((pR / 255) * 100)
        g = 100 - round((pG / 255) * 100)
        b = 100 - round((pB / 255) * 100)
        self.red.ChangeDutyCycle(r)
        self.green.ChangeDutyCycle(g)
        self.blue.ChangeDutyCycle(b)

def RGBToHSL(pR, pG, pB):
    r = pR / 255
    g = pG / 255
    b = pB / 255
    minV = min(r, g, b)
    maxV = max(r, g ,b)
    d = maxV - minV
    l = (minV + maxV) / 2

    if d==0:
        h = s = 0
    else:
        s = (d / (maxV + minV)) if (l < .5) else (d / (2 - maxV - minV))
        dr = (((maxV - r) / 6) + (d / 2)) / d
        dg = (((maxV - g) / 6) + (d / 2)) / d
        db = (((maxV - b) / 6) + (d / 2)) / d

        if maxV == r:
            h = db - dg
        elif maxV == g:
            h = (1 / 3) + (dr - db)
        elif maxV == b:
            h = (2 / 3) + dg - dr

        return {'h':h, 's':s, 'l':l}


def HSLToRGB(pH, pS, pL):
    if pS == 0:
        r = pL * 255
        g = pL * 255
        b = pL * 255
    else:
        t2 = (pL * (1 + pS)) if (pL < .5) else ((pL + pS) - (pS * pL))
        t1 = (2 * pL) - t2
        r = 255 * hueToRgb(t1, t2, pH + (1 / 3))
        g = 255 * hueToRgb(t1, t2, pH)
        b = 255 * hueToRgb(t1, t2, pH - (1 / 3))
    return {'r':r, 'g':g, 'b':b}

def hueToRgb(pT1, pT2, pH):
    if pH < 0:
        pH = pH + 1
    elif pH > 1:
        pH = pH - 1
    if ((6 * pH) < 1):
        return (pT1 + (pT2 - pT1) * 6 * pH)
    if ((2 * pH) < 1):
        return pT2
    if ((3 * pH) < 2):
        return (pT1 + (pT2 - pT1) * ((2/3) - pH) * 6)
    return pT1


led = LED(red, green, blue)

hue = 0

try:
    while RUNNING:
        hue = hue + 10
        if hue == 360:
            hue = 0
        c = HSLToRGB(hue / 360, 1, .5)
        led.setColor(c['r'], c['g'], c['b'])
        time.sleep(.1)

except KeyboardInterrupt:
    RUNNING = False
    print("\Quitting")
finally:
    GPIO.cleanup()
