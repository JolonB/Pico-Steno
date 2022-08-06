import asyncio

import pwmio
import adafruit_simplemath as smath
import adafruit_logging as logging


class Backlight:
    __MAX_DUTY = 65535

    def __init__(self, pin, fade_rate:float=1.0):
        # Initialise PWM pin for backlight control
        self.__pin_name = str(pin)
        self.__logger = logging.getLogger("Backlight")

        # Set initial mode to OFF
        self.__mode_functions = [
            self.off,
            self.on_25,
            self.on_50,
            self.on_75,
            self.on_100,
            self.blink,
            self.fade,
        ]
        self.__mode = 0
        self.__fade_rate = fade_rate

        self.__init_led(pin)

    def __get_duty_cycle(self, duty_0_1) -> int:
        """Convert the duty cycle from 0-1 to 0-2^16

        Args:
            duty_0_1 (float): A duty cycle between 0 and 1
        """
        return int(smath.map_range(duty_0_1, 0, 1, 0, self.__MAX_DUTY))

    def __log(self, level, msg):
        self.__logger.log(level, "({}) {}".format(self.__pin_name, msg))

    def __init_led(self, pin):
        self.__led = pwmio.PWMOut(pin, duty_cycle=0, frequency=5000)
        self.set_duty_cycle(0)

        self.__log(logging.INFO, "Backlight control configured on pin {}".format(pin))
        self.__pin_name = str(pin)

    def set_duty_cycle(self, duty_0_1):
        self.__led.duty_cycle = self.__get_duty_cycle(duty_0_1)

    def increment_mode(self):
        self.__mode += 1
        # Cycle back to the start if we've hit the end
        if self.__mode >= len(self.__mode_functions):
            self.__mode = 0

    async def start(self, pin=None, fade_rate=None):
        # Override previous values if new ones are provided
        if pin is not None:
            self.__led.deinit()
            self.__init_led(pin)
        if fade_rate is not None:
            self.__fade_rate = fade_rate

        # Start the backlight loop
        while True:
            self.__log(logging.DEBUG, "Backlight set to mode {}".format(self.__mode))
            await self.__mode_functions[self.__mode]()

    async def off(self):
        self.set_duty_cycle(0)
        while self.__mode == 0:
            await asyncio.sleep(0.5)

    async def on_25(self):
        self.set_duty_cycle(0.25)
        while self.__mode == 1:
            await asyncio.sleep(0.5)

    async def on_50(self):
        self.set_duty_cycle(0.5)
        while self.__mode == 2:
            await asyncio.sleep(0.5)

    async def on_75(self):
        self.set_duty_cycle(0.75)
        while self.__mode == 3:
            await asyncio.sleep(0.5)

    async def on_100(self):
        self.set_duty_cycle(1)
        while self.__mode == 4:
            await asyncio.sleep(0.5)

    async def blink(self):
        while self.__mode == 5:
            self.set_duty_cycle(1)
            await asyncio.sleep(0.5)
            self.set_duty_cycle(0)
            await asyncio.sleep(0.5)

    async def fade(self):
        sleep_time = 0.01
        fade_amount = sleep_time / self.__fade_rate
        brightness = 0.0

        while self.__mode == 6:
            self.set_duty_cycle(brightness)
            brightness += fade_amount
            # Reverse the fading direction if we've hit the end of the fade
            if not (0 <= brightness <= 1):
                fade_amount = -fade_amount
            await asyncio.sleep(sleep_time)
