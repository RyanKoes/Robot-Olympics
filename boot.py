from machine import Pin
# initliaze the line sensor
left = Pin(2, Pin.IN)
right = Pin(3, Pin.IN)
left.value(0)
right.value(0)
# motor
Pin(8, Pin.IN)
Pin(9, Pin.IN)
Pin(10, Pin.IN)
Pin(11, Pin.IN)

# init the distance sensor 
trigger = Pin(26, Pin.OUT)
echo = Pin(27, Pin.IN)
trigger.low()
echo.value(0)


