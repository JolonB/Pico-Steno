"""
THIS IS SAMPLE CODE
DON'T BOTHER RUNNING THIS
"""

import asyncio

import board
import pwmio
import digitalio

# async def blink(pin, interval, count):
#     with digitalio.DigitalInOut(pin) as led:
#         led.switch_to_output(value=False)
#         for _ in range(count):
#             led.value = not led.value
#             await asyncio.sleep(interval)

# async def main():
#     led_task = asyncio.create_task(blink(board.LED, 0.5, 20))
#     await asyncio.gather(led_task)

# if __name__ == "__main__":
#     asyncio.run(main())
#     print("done")

class LightingLED:
    class Modes():
        OFF = 0
        ON_25 = 1
        ON_50 = 2
        ON_75 = 3
        ON_100 = 4
        BLINK = 5
        FADE = 6

    MAX_DUTY = 65535

    def __init__(self, pin):
        self.mode = self.Modes.OFF
        self.led = pwmio.PWMOut(pin, duty_cycle=0, frequency=5000)
        self.function_map = {
            self.Modes.OFF: self.off,
            self.Modes.ON_25: self.on_25,
            self.Modes.ON_50: self.on_50,
            self.Modes.ON_75: self.on_75,
            self.Modes.ON_100: self.on_100,
            self.Modes.BLINK: self.blink,
            self.Modes.FADE: self.fade,
        }

    def __duty_cycle(self, duty_0_1):
        """Convert the duty cycle from 0-1 to 0-2^16

        Args:
            duty_0_1 (float): A duty cycle between 0 and 1
        """
        return max(0, min(int(duty_0_1 * self.MAX_DUTY), self.MAX_DUTY))

    def set_duty_cycle(self, duty_0_1):
        self.led.duty_cycle = self.__duty_cycle(duty_0_1)

    def increment_mode(self):
        self.mode = self.mode + 1
        # Cycle back to the start if we've hit the end
        if self.mode > self.Modes.FADE:
            self.mode = self.Modes.OFF

    async def run(self):
        while True:
            await self.function_map[self.mode]()

    async def off(self):
        self.set_duty_cycle(0)
        print(self.mode)
        while self.mode == self.Modes.OFF:
            await asyncio.sleep(1)

    async def on_25(self):
        self.set_duty_cycle(0.25)
        print(self.mode)
        while self.mode == self.Modes.ON_25:
            await asyncio.sleep(1)

    async def on_50(self):
        self.set_duty_cycle(0.5)
        print(self.mode)
        while self.mode == self.Modes.ON_50:
            await asyncio.sleep(1)

    async def on_75(self):
        self.set_duty_cycle(0.75)
        print(self.mode)
        while self.mode == self.Modes.ON_75:
            await asyncio.sleep(1)

    async def on_100(self):
        self.set_duty_cycle(1)
        print(self.mode)
        while self.mode == self.Modes.ON_100:
            await asyncio.sleep(1)

    async def blink(self):
        print(self.mode)
        while self.mode == self.Modes.BLINK:
            self.set_duty_cycle(1)
            await asyncio.sleep(0.5)
            self.set_duty_cycle(0)
            await asyncio.sleep(0.5)

    async def fade(self):
        print(self.mode)
        fade_amount = 0.01
        brightness = 0.
        while self.mode == self.Modes.FADE:
            self.set_duty_cycle(brightness)
            brightness += fade_amount
            # Reverse the fading direction if we've hit the end of the fade
            if not (0 <= brightness <= 1):
                fade_amount = -fade_amount
            await asyncio.sleep(0.01)
            

async def monitor_interval_buttons(pin, lighting):
    with digitalio.DigitalInOut(pin) as button:
        button.switch_to_input()
        button.pull = digitalio.Pull.UP

        released = True
        while True:
            if not button.value:
                if released:
                    released = False
                    print("Button pressed")
                    lighting.increment_mode()
            else:
                released = True
            await asyncio.sleep(.01)

async def main():
    led = LightingLED(board.LED)
    led_task = asyncio.create_task(led.run())
    button_task = asyncio.create_task(monitor_interval_buttons(board.GP13, led))
    await asyncio.gather(button_task, led_task)

import buttons.button as but
async def main2():
    pf = but.ButtonFunction(print, "pressed")
    rf = but.ButtonFunction(print, "released")
    hf = but.ButtonFunction(print, "held")
    
    button = but.Button(board.GP13, press_func=pf, release_func=rf, hold_func=hf, hold_time=0.5)
    button_task = button.start()
    
    await asyncio.gather(button_task)

if __name__ == "__main__":
    asyncio.run(main2())