import machine
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
                {'00':'no_wall',     '01':'straight',      '10':'straight', '11':'straight'},
            'no_wall':
                {'00':'right'},
            'right':
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
}
bot = bot(**conf)

brain = Brain()  # Moved outside the loop

while True:
    # using the FSM to control the robot
    left, right = bot.read_line()
    Antenna = str(left) + str(right)
    
    # Advance the FSM and get the action
    action = brain.advance(Antenna)  # Use the existing `brain` object
    print(action)
    
    if action == 'F':
        bot.fwd()
    elif action == 'TR':
        bot.rotate()
    else:
        bot.brake()