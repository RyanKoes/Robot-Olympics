import uasyncio as asyncio
from machine import Pin, ADC, time_pulse_us
import utime


import machine

class bot:
    def __init__(self, **kwargs):
        print(kwargs)

        # Setup DC Motor pins
        self.M1A = machine.PWM(machine.Pin(kwargs["M1A"]))
        self.M1B = machine.PWM(machine.Pin(kwargs["M1B"]))
        self.M2A = machine.PWM(machine.Pin(kwargs["M2A"]))
        self.M2B = machine.PWM(machine.Pin(kwargs["M2B"]))
        self.M1A.freq(50)
        self.M1B.freq(50)
        self.M2A.freq(50)
        self.M2B.freq(50)

        self.left = machine.Pin(kwargs["left"], machine.Pin.IN)
        self.right = machine.Pin(kwargs["right"], machine.Pin.IN)
        
        self.A = machine.Pin(kwargs["A"], machine.Pin.IN)
        
        self.trigPin = machine.Pin(kwargs["trigPin"], machine.Pin.OUT)
        self.echoPin = machine.Pin(kwargs["echoPin"], machine.Pin.IN)


    def rotate(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)
        
    def turnleft(self, amount_u16 = 0x3000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.
        self.M1A.duty_u16(self.M1A.duty_u16())     # Duty Cycle must be between 0 until 65535
        self.M1B.duty_u16(self.M1B.duty_u16())

        if self.M2B.duty_u16() == 0:
            # reverse
            self.M2A.duty_u16(min(0xffff,self.M2A.duty_u16() + amount_u16))
            self.M2B.duty_u16(0)
        else:
            # forward
            self.M2A.duty_u16(self.M2A.duty_u16())
            self.M2B.duty_u16(max(0,self.M2B.duty_u16() - amount_u16))

    def turnright(self, amount_u16 = 0x3000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.

        if self.M1B.duty_u16() == 0:
            # reverse
            self.M1A.duty_u16(min(0xffff,self.M1A.duty_u16() + amount_u16))
            self.M1B.duty_u16(0)
        else:
            # forward
            self.M1A.duty_u16(self.M1A.duty_u16())     # Duty Cycle must be between 0 until 65535
            self.M1B.duty_u16(max(0,self.M1B.duty_u16() - amount_u16))

        self.M2A.duty_u16(self.M2A.duty_u16())
        self.M2B.duty_u16(self.M2B.duty_u16())

    def fwd(self, speed=0.4):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))

    def reverse(self, speed=0.3):
        self.M1A.duty_u16(int(speed * 65535))
        self.M1B.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def brake(self):
        self.M1A.duty_u16(65535)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(65535)
        self.M2A.duty_u16(65535)
        self.M2B.duty_u16(65535)

    def read_line(self):
        return self.left.value(), self.right.value()
    
    def read_distance(self):
        self.trigPin.low()
        utime.sleep_us(2)
        self.trigPin.high()
        utime.sleep_us(5)
        self.trigPin.low()
        pulse = machine.time_pulse_us(self.echoPin, 1, 10000)
        distance = 1 / 58.0 * pulse
        return distance

conf = {
        "M1A": 8,
        "M1B": 9,
        "M2A": 10,
        "M2B": 11,
        "left": 3,
        "right": 2,
        "A": 20,
        "trigPin": 27,
        "echoPin": 26,
}
bot = bot(**conf)

async def button_on_press():
    while True:
        if bot.A.value() == 0:
            break
        await asyncio.sleep_ms(100)

async def main():
    await button_on_press()
    stop = False
    start_time = utime.ticks_ms()
    while True:
        left, right = bot.read_line()
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 15000:
            distance = bot.read_distance()
            # print("Distance = ", distance, "cm")
            if distance < 30:
                stop = True
            elif distance >= 30:
                stop = False

        if stop:
            bot.brake()
        else:
            if left == 0 and right == 0:
                bot.fwd()
            elif left == 1 and right == 0:
                bot.turnleft()
            elif left == 0 and right == 1:
                bot.turnright()
            elif left == 1 and right == 1:
                bot.brake()
        await asyncio.sleep_ms(100)

# call main
asyncio.run(main())
