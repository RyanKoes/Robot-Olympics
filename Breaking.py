from machine import Pin, PWM
from time import sleep_ms
import asyncio

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
    "C5", "P", "D5", "P", "G4", "P"
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
    500, 167, 500, 167, 500, 1000
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

def play_mc():
    for i in range(len(minecraft)):
        note = minecraft[i]
        duration = minecraft_duration[i]
        
        if note == "P":
            bequiet()
        else:
            playtone(tones[note])
        
        # Add a small gap between notes (30% of the note duration)
        pause = int(duration * 1.3)
        sleep_ms(pause)
        bequiet()

def play_rickroll():
    for i in range(len(melody)):
        note = melody[i]
        duration = durations[i]
        
        if note == "P":
            bequiet()
        else:
            playtone(tones[note])
        
        # Add a small gap between notes (30% of the note duration)
        pause = int(duration * 1.3)
        sleep_ms(pause)
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


    def rotate(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)

    def turnleft(self, amount_u16 = 0x2000):
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

    def turnright(self, amount_u16 = 0x2000):
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

conf = {
    "M1A": 8,
    "M1B": 9,
    "M2A": 10,
    "M2B": 11,
    "left": 26,
    "right": 27,
}
bot = bot(**conf)

async def main():
    # Perform Minecraft dance
    play_mc()
    bot.rotate(speed=0.2)  # Spin in place
    await asyncio.sleep(2)  # Use await and asyncio.sleep for async delays
    bot.fwd(speed=0.3)
    await asyncio.sleep(2)
    bot.turnleft(amount_u16=0x4000)
    await asyncio.sleep(0.5)
    bot.turnright(amount_u16=0x4000)
    await asyncio.sleep(0.5)
    bot.brake()

    # Pause before Rickroll
    await asyncio.sleep(0.5)

    # Perform Rickroll dance
    play_rickroll()
    bot.reverse(speed=0.3)  # Reverse to the beat
    await asyncio.sleep(2)
    bot.rotate(speed=0.4)   # Spin
    await asyncio.sleep(2)
    bot.fwd(speed=0.5)
    await asyncio.sleep(2)
    bot.brake()

# Start the event loop for the async function
asyncio.run(main())
