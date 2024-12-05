import machine, neopixel
import utime

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
        
        self.goToggle = machine.Pin(20, machine.Pin.IN)


    def rotate(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def turnleft(self, amount_u16 = 0x1000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(0.35 * 65535)) #right wheel forward
        self.M2A.duty_u16(int(0.3 * 65535)) #left wheel reverse int(0.5 * 65535)
        self.M2B.duty_u16(int(0 * 65535))

    def turnright(self, amount_u16 = 0x1000):
        # turn left by increasing the speed of the right motor and decreasing the speed of the left motor
        # assumes we are going forward.

        self.M1A.duty_u16(int(0.3 * 65535))     # int(0.5 * 65535)
        self.M1B.duty_u16(int(0 * 65535))
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(0.45 * 65535))

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

# Create a bot object
conf = {
    "M1A": 8,
    "M1B": 9,
    "M2A": 10,
    "M2B": 11,
    "left": 3,
    "right": 2
}
bot = bot(**conf)

np = neopixel.NeoPixel(machine.Pin(18), 2)

prev_turn = ""

while True:
    left, right = bot.read_line()

    if left == 0 and right == 0:
        bot.fwd()
        np[0] = (0, 0, 255)
        np[1] = (0, 0, 255)
    elif left == 1 and right == 0:
        bot.turnleft()
        prev_turn = "left"
        np[0] = (255, 0, 0)  # Set the first LED to red
        np[1] = (0, 0, 0)
    elif left == 0 and right == 1:
        bot.turnright()
        prev_turn = "right"
        np[1] = (255, 0, 0)  # Set the first LED to red
        np[0] = (0, 0, 0)
    elif left == 1 and right == 1:
        if prev_turn == "left":
            bot.turnleft()
            np[0] = (255, 0, 0)  # Set the first LED to red
            np[1] = (0, 0, 0)
            prev_turn = "left"
        elif prev_turn == "right":
            bot.turnright()
            np[1] = (255, 0, 0)  # Set the first LED to red
            np[0] = (0, 0, 0)
            prev_turn = "right"
        else:
            bot.brake()
        np[1] = (0, 0, 0)
        np[0] = (0, 0, 0)
    else:
        bot.fwd()
    np.write()
