from machine import Pin, PWM
from time import sleep_ms
import uasyncio as asyncio
import neopixel


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

    def rotate_right(self, speed=0.3):
        self.M1A.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M1B.duty_u16(int(speed * 65535))
        self.M2A.duty_u16(int(speed * 65535))
        self.M2B.duty_u16(0)
    def rotate_left(self, speed=0.3):
        self.M1A.duty_u16(int(speed * 65535))
        self.M1B.duty_u16(0)     # Duty Cycle must be between 0 and 65535
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(int(speed * 65535))

        
    def turnleft(self, amount_u16 = 0x800):
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

    def turnright(self, amount_u16 = 0x800):
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


    def read_line(self):
        return self.left.value(), self.right.value()
    
    
class FiniteStateMachine:
    def __init__(self):
        self.transitions = None
        self.current_state = 'initial'

    def process_input(self, input):
        print(f"Current state: {self.current_state}, input: {input}", end=", ")
        self.current_state = self.transitions[self.current_state][input]
        print(f"Next state: {self.current_state}!")
        return self.current_state

    def is_accepted(self):
        return self.current_state == 'final'
    
    
class Brain(FiniteStateMachine):
       
    def __init__(self):
        super().__init__()           
        self.current_state = 'Idle' 
        self.transitions = {
            'Idle': 
                {'00':'Idle',     '01':'straight',      '10':'straight', '11':'straight'},

            'straight':
                {'00':'right',     '01':'straight',      '10':'left', '11':'straight'},
            'right':
                {'00':'straight',     '01':'straight',      '10':'straight', '11':'straight'},
            'left':
                {'00':'no_wall',     '01':'right',      '10':'straight', '11':'straight'},
            'no_wall':
                {'00':'no_wall',     '01':'straight',      '10':'straight', '11':'straight'},
        }        
        

        # DO CHANGE THIS! This is your output table! The format is:
        # 'state name':'output'
        # The output is what you want the ant to do when it is in that state.
        # The supported outputs are:    
        # 'F' -- Go Forward
        # 'TR' -- Turn Right
        # 'TL' -- Turn Left
        # ''   -- do nothing (its an empty text string)    
        self.outputs = {
                'Idle':'',
                'straight':'F',
                'no_wall':'F',
                'right':'TR',

        }
    
    ###### You shouldn't have to edit anything below this (Unless you name your default state something other than "Idle"
    def reset(self):
        self.current_state = 'Idle'

    ##### There is nothing to edit here
    def advance(self, Antenna):
        # this processes the input and moves the FSM to the next state
        # then returns the output for that (new) state, the action will be taken
        # and the FSM will be advanced on the next call
        return self.outputs[self.process_input(Antenna)]
    
# Create a bot object
conf = {
    "M1A": 8,
    "M1B": 9,
    "M2A": 10,
    "M2B": 11,
    "left": 3,
    "right": 2,
     "A": 20,
}
bot = bot(**conf)

brain = Brain()  # Moved outside the loop

# while True:
#     # using the FSM to control the robot
#     left, right = bot.read_line()
#     Antenna = str(left) + str(right)
    
#     # Advance the FSM and get the action
#     action = brain.advance(Antenna)  # Use the existing `brain` object
#     print(action)
    
#     if action == 'F':
#         bot.fwd()
#     elif action == 'TR':
#         bot.rotate()
#     else:
#         bot.brake()

# while True:
#     left, right = bot.read_line()
#     # bot.fwd()

#     if left == 0 and right == 0:
#         bot.fwd()
#     elif left == 1 and right == 0:
#         bot.turnleft()
#     elif left == 0 and right == 1:
#         bot.turnright()
#     elif left == 1 and right == 1:
#         bot.brake()
#     else:
#         bot.fwd()

# wait for the button to be pressed
async def button_on_press():
    while True:
        if bot.A.value() == 0:
            break
        await asyncio.sleep_ms(100)


async def main():
    await button_on_press()
    while True:
        left, right = bot.read_line()
        # bot.fwd()

        if left == 0 and right == 0:
            bot.fwd()
        elif left == 1 and right == 0:
            bot.rotate_left()
        elif left == 0 and right == 1:
            bot.rotate_right()
        elif left == 1 and right == 1:
            bot.brake()
        else:
            bot.fwd()

        await asyncio.sleep_ms(100)

# call main
asyncio.run(main())
