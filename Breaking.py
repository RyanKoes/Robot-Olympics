from machine import Pin, PWM
from time import sleep_ms
import uasyncio as asyncio
import neopixel


# Initialize buzzer on pin 22
buzzer = PWM(Pin(22))

# initliaze the sensor pins

trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)



# Note frequencies mapping
tones = {
    "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46,
    "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62, "C2": 65,
    "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93, "G2": 98,
    "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139,
    "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185,
    "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262, "CS4": 277,
    "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415,
    "A4": 440, "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622,
    "E5": 659, "F5": 698, "FS5": 740, "G5": 784, "GS5": 831, "A5": 880, "AS5": 932,
    "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319,
    "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865,
    "B6": 1976, "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637,
    "F7": 2794, "FS7": 2960, "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729,
    "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
}

# Convert frequency to note name
def get_note_name(freq):
    if freq == 0:
        return "P"
    for note, frequency in tones.items():
        if abs(frequency - freq) < 1:
            return note
    return "P"


# Convert the original melody to note names
melody = [
    "A4", "P", "B4", "P", "C5", "P", "A4", "P",
    "D5", "P", "E5", "P", "D5", "P",
    "G4", "A4", "C5", "A4", "E5", "E5", "P",
    "D5", "P",
    "G4", "A4", "C5", "A4", "D5", "D5", "P",
    "C5", "P", "B4", "A4", "P",
    "G4", "A4", "C5", "A4", "C5", "D5", "P",
    "B4", "A4", "G4", "P", "G4", "P", "D5", "P", "C5", "P",
    "G4", "A4", "C5", "A4", "E5", "E5", "P",
    "D5", "P",
    "G4", "A4", "C5", "A4", "G5", "B4", "P",
    "C5", "P", "B4", "A4", "P",
    "G4", "A4", "C5", "A4", "C5", "D5", "P",
    "B4", "A4", "G4", "P", "G4", "P", "D5", "P", "C5", "P",
    "C5", "P", "D5", "P", "G4", "P", "D5", "P", "E5", "P",
    "G5", "F5", "E5", "P",
    
]

# Convert the original durations to milliseconds
durations = [
    125, 125, 125, 125, 125, 125, 125, 250,
    125, 125, 125, 125, 500, 500,
    125, 125, 125, 125, 500, 125, 125,
    500, 125,
    125, 125, 125, 125, 500, 125, 125,
    250, 125, 125, 125, 125,
    125, 125, 125, 125, 500, 125, 125,
    500, 125, 250, 125, 125, 125, 125, 125, 1000, 250,
    125, 125, 125, 125, 500, 125, 125,
    500, 125,
    125, 125, 125, 125, 500, 125, 125,
    500, 125, 125, 125, 125,
    125, 125, 125, 125, 500, 125, 125,
    250, 125, 333, 125, 125, 125, 125, 125, 1000, 250,
    500, 167, 500, 167, 250, 250, 500, 167, 500, 333,
    125, 125, 125, 125,
    
]

minecraft = ["E4", "A5", "B5", "E5", "G5", "B6", "D6", "A7", 
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "A7",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6",
"E4", "A5", "B5", "E5", "G5", "B6", "D6", "G6"
]


minecraft_duration = [125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125,
125, 125, 125, 125, 125, 125, 125, 125
]

def playtone(frequency):
    if frequency == 0:
        bequiet()
    else:
        buzzer.duty_u16(1 << 10)
        buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

async def play_mc():
    for i in range(len(minecraft)):
        note = minecraft[i]
        duration = minecraft_duration[i]
        
        if note == "P":
            bequiet()  # Silence the buzzer
        else:
            playtone(tones[note])  # Play the corresponding tone
        
        # Add a small gap between notes (30% of the note duration)
        pause = duration * 1.3 / 1000  # Convert ms to seconds for asyncio.sleep
        await asyncio.sleep(pause)
        bequiet() 

async def play_rickroll():
    for i in range(len(melody)):
        note = melody[i]
        duration = durations[i]
        
        if note == "P":
            bequiet()
        else:
            playtone(tones[note])
        
        # Add a small gap between notes (30% of the note duration)
        pause = duration * 1.3 / 1000  # Convert ms to seconds for asyncio.sleep
        await asyncio.sleep(pause)
        bequiet() 
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


    async def rotate_right(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)
        await asyncio.sleep(1) # Asynchronous delay
        self.brake()  

    async def rotate_left(self, speed=0.3):
        self.M1A.duty_u16(int(speed * 65535))
        self.M1B.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))
        await asyncio.sleep(1) # Asynchronous delay
        self.brake()  

    async def turnleft(self, amount_u16 = 0x2000):
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

    async def turnright(self, amount_u16 = 0x2000):
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

    async def fwd(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))
        await asyncio.sleep(1) # Asynchronous delay
        self.brake()

    async def reverse(self, speed=0.3):
        self.M1A.duty_u16(int(speed * 65535))
        self.M1B.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)
        await asyncio.sleep(1) # Asynchronous delay
        self.brake()

    def brake(self):
        self.M1A.duty_u16(65535)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(65535)
        self.M2A.duty_u16(65535)
        self.M2B.duty_u16(65535)

    def read_line(self):
        return self.left.value(), self.right.value()

conf = {
    "M1A": 8,
    "M1B": 9,
    "M2A": 10,
    "M2B": 11,
    "left": 3,
    "right": 2,
     "A": 20,
}
async def dance_mc():
    # Spin left and right for a duration of 5 seconds
    await bot.rotate_right(speed=0.5)  # Spin in place
    await asyncio.sleep(.0001)  # Add delay between movements
    await bot.rotate_left(speed=0.5)   # Spin in place
    await asyncio.sleep(.0001)  # Add delay between movements
    await bot.rotate_right(speed=0.5)  # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_left(speed=0.5)   # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_right(speed=0.5)  # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_left(speed=0.5)   # Spin in place
    await asyncio.sleep(.0001)  # Add delay between movements
    await bot.rotate_right(speed=0.5)  # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_left(speed=0.5)   # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_right(speed=0.5)  # Spin in place
    await asyncio.sleep(.0001)
    await bot.rotate_left(speed=0.5)   # Spin in place
    await asyncio.sleep(.0001)
    bot.brake()  # Stop the motors

async def check_boundary():
    while True:
        read = bot.read_line()
        # if solid black line is detected on both sides, reverse the bot for a bit and do a 180 degree turn
        if read[0] == 0 and read[1] == 0:
            await bot.reverse(.4)
            await asyncio.sleep(.001)
            await bot.rotate_right(.5)
            await asyncio.sleep(1)
            bot.brake()
        await asyncio.sleep(.1)
            


async def dance_rickroll():
    # Introduction: Move forward and backward rhythmically
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.25)  # Forward for 2 beats
    bot.brake()
    await asyncio.sleep(0.125)  # Pause for 1 beat
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.25)  # Backward for 2 beats
    bot.brake()
    await asyncio.sleep(0.125)  # Pause for 1 beat
    await bot.rotate_right(speed=0.5)
    await asyncio.sleep(0.25)  # Spin right for 2 beats
    bot.brake()

    # Verse 1: Zig-zag motion with slight turns
    await bot.turnleft(0x2000)
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.25)  # Turn left and forward for 2 beats
    bot.brake()
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.25)  # Reverse for 2 beats

    # Chorus 1: Full spins and rapid movements
    await bot.rotate_right(speed=0.6)
    await asyncio.sleep(0.5)  # Spin in place to the right for 4 beats
    bot.brake()
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats
    bot.brake()
    await bot.rotate_left(speed=0.6)
    await asyncio.sleep(0.5)  # Spin in place to the left for 4 beats
    bot.brake()
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.1)  # Reverse rapidly for 2 beats
    bot.brake()
    await asyncio.sleep(0.5)  # Pause for 4 beats
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats

    # Introduction: Move forward and backward rhythmically
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.25)  # Forward for 2 beats
    bot.brake()
    await asyncio.sleep(0.125)  # Pause for 1 beat
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.25)  # Backward for 2 beats
    bot.brake()
    await asyncio.sleep(0.125)  # Pause for 1 beat
    await bot.rotate_right(speed=0.5)
    await asyncio.sleep(0.25)  # Spin right for 2 beats
    bot.brake()

    # Verse 1: Zig-zag motion with slight turns
    await bot.turnleft(0x2000)
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.25)  # Turn left and forward for 2 beats
    bot.brake()
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.25)  # Reverse for 2 beats

    # Chorus 1: Full spins and rapid movements
    await bot.rotate_right(speed=0.6)
    await asyncio.sleep(0.5)  # Spin in place to the right for 4 beats
    bot.brake()
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats
    bot.brake()
    await bot.rotate_left(speed=0.6)
    await asyncio.sleep(0.5)  # Spin in place to the left for 4 beats
    bot.brake()
    await bot.reverse(speed=0.3)
    await asyncio.sleep(0.1)  # Reverse rapidly for 2 beats
    bot.brake()
    await asyncio.sleep(0.5)  # Pause for 4 beats
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats
    await bot.fwd(speed=0.3)
    await asyncio.sleep(0.1)  # Move forward quickly for 2 beats

    # turn off the lights
    set_color((0, 0, 0))
    # turn music off 
    bequiet()
    # turn off the motors
    bot.brake()
    # run an exception
    raise  Exception("Rickrolled")


# Initialize NeoPixel
# Initialize NeoPixel (adjust pin and LED count as needed)
num_pixels = 2 # Number of LEDs in your strip
led_pin = Pin(18)  # GPIO pin connected to NeoPixel data line
np = neopixel.NeoPixel(led_pin, num_pixels)


def set_color(color):
    for i in range(num_pixels):
        np[i] = color
    np.write()

# Asynchronous function to flash LEDs
async def color_show():
    colors = [ (255, 0, 0), (255, 102, 102), (255, 204, 204),  # Red, Light Red, Lighter Red
    (255, 165, 0),
    (255, 69, 0),   # Red-Orange
    (255, 20, 147), # Deep Pink
    (255, 105, 180) # Hot Pink
    ]
    while True:
        for color in colors:
            set_color(color)  # Set the LED strip to the current color
            await asyncio.sleep(.2)  # Wait before switching to the next color

    


bot = bot(**conf)

# wait for the button to be pressed
async def button_on_press():
    while True:
        if bot.A.value() == 0:
            break
        await asyncio.sleep_ms(100)


async def main():
    await button_on_press()
    # await asyncio.gather(dance_mc(), play_mc())
    await asyncio.gather(dance_rickroll(), play_rickroll(), color_show())
asyncio.run(main())
