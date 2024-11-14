from Bot import bot
import time



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
