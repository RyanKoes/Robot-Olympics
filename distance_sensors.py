import asyncio
import math
from machine import Pin, ADC, time_pulse_us
import time

trigPin = Pin(5, Pin.OUT)
echoPin = Pin(4, Pin.IN)


async def collect_sensors():
    global red_led_period, yellow_led_period, green_led_period
    while True:
        # Distance sensor
        trigPin.off()
        time.sleep_us(2)
        trigPin.on()
        time.sleep_us(10)
        trigPin.off()
        duration = time_pulse_us(echoPin, 1)
        distance = (duration * 0.034) / 2

        if distance > 500:
            distance = 0
            
        print('Distance:', distance)

        await asyncio.sleep_ms(500)

async def main():

    loop = asyncio.get_event_loop()
    loop.create_task(collect_sensors())
    loop.run_forever()

asyncio.run(main())
