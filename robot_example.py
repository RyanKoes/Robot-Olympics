import utime
from Bot import bot



# Create a bot object
conf = {
    "M1A": 8,
    "M1B": 9,
    "M2A": 10,
    "M2B": 11
}
bot = bot(**conf)

while True:
    # Example motor control loop without distance sensor logic
    bot.fwd()
    print("Moving forward")
    
    utime.sleep(2)

    bot.reverse()
    print("Reversing")
    
    utime.sleep(2)
    
    bot.brake()
    print("Stopped")
    
    utime.sleep(0.2)
