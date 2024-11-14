import time

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


    def rotate(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def fwd(self, speed=0.3):
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
def main():
    conf = {
        "M1A": 8,
        "M1B": 9,
        "M2A": 10,
        "M2B": 11,
        "left": 2,
        "right": 3,
    }
    b = bot(**conf)

    while True:
        left, right = b.read_line()
        print("Left: {}, Right: {}".format(left, right))
        time.sleep(1)

try:
    main()
except Exception as e:
    conf = {
        "M1A": 8,
        "M1B": 9,
        "M2A": 10,
        "M2B": 11,
        "left": 2,
        "right": 3,
    }
    b = bot(**conf)
    print("Emergency stop.")
    raise(e)
