import rcpy.led as led
from rcpy.led import red, green
blink = led.Blink(green, .5)
blink.stop()