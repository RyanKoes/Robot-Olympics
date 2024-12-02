import machine
import neopixel
import time

# Pin configuration
LED_PIN = 8           # GPIO pin connected to the LED strip data line
NUM_LEDS = 14         # Number of LEDs on the strip

# Initialize the NeoPixel strip
pin = machine.Pin(LED_PIN)
strip = neopixel.NeoPixel(pin, NUM_LEDS)

# Function to set all LEDs to a specific color
def set_color(color):
    for i in range(NUM_LEDS):
        strip[i] = color
    strip.write()

# Function to turn off all LEDs
def clear_strip():
    set_color((0, 0, 0))

# Example: Cycle through red, green, and blue
def color_cycle():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
    while True:
        for color in colors:
            set_color(color)
            time.sleep(0.5)  # Wait 0.5 seconds

# Function to create a running light effect
def running_light(color, delay=0.1):
    for i in range(NUM_LEDS):
        clear_strip()
        strip[i] = color
        strip.write()
        time.sleep(delay)

# Main function
def main():
    try:
        print("Starting LED control...")
        clear_strip()  # Ensure LEDs are off initially

        # Example light effects
        print("Cycling colors...")
        color_cycle()
        # Or use another effect:
        # running_light((255, 255, 0))  # Yellow running light
    except KeyboardInterrupt:
        print("Stopping...")
        clear_strip()

# Run the main function
if __name__ == "__main__":
    main()
