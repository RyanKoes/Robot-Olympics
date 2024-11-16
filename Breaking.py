# from machine import Pin, PWM
# import time

# def play_frequencies_from_file(filename):
#     # Initialize PWM on a pin (change pin number as needed)
#     buzzer = PWM(Pin(22))  # Adjust pin number according to your setup
    
#     try:
#         # Open and read the file
#         with open(filename, 'r') as file:
#             for line in file:
#                 # Skip empty lines
#                 if line.strip():
#                     # Split time and frequency
#                     duration, frequency = line.split('|')
#                     # Convert to float and strip whitespace
#                     duration = float(duration.strip())
#                     frequency = float(frequency.strip())
                    
#                     if frequency > 0:
#                         # Set frequency
#                         buzzer.freq(int(frequency)//2)
#                         # Set duty to 50%
#                         buzzer.duty_u16(1 << 10)  # 50% of 65535
#                         # Wait for the specified duration
#                         time.sleep(duration)
#                         # Turn off sound
#                         buzzer.duty_u16(0)
#                     else:
#                         # If frequency is 0, just wait
#                         time.sleep(duration)
    
#     except OSError as e:
#         print("Error reading file:", e)
#     except ValueError as e:
#         print("Error parsing data:", e)
#     finally:
#         # Clean up
#         buzzer.deinit()



# # Play frequencies from the file
# play_frequencies_from_file('frequencies.txt')

from machine import Pin, PWM
from time import sleep_ms

# Initialize buzzer on pin 22
buzzer = PWM(Pin(22))

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

def playtone(frequency):
    if frequency == 0:
        bequiet()
    else:
        buzzer.duty_u16(1 << 14)
        buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

def play_melody():
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

# Play the melody
while True:
    play_melody()
    sleep_ms(2000)  # Wait 2 seconds before repeating