import time
import asyncio

import digitalio
import adafruit_logging as logging

POLLING_TIMEOUT = 0.005


class Button:
    def __init__(
        self,
        pin_id,
        key_value,
        active_high=False,
    ):
        """Create a button object representing a physical button connected to
        the given pin_id.

        Args:
            pin_id (Pin): The pin to which the button is connected. Must come
            from `board` module.
        """
        self._logger = logging.getLogger("Button")
        self._pin_name = str(pin_id)
        self._active_high = active_high
        self._key_value = key_value

        self._pressed = False
        self._pressed_time = 0.0

        # Initialise button
        self.__setup_button(pin_id)

    def __log(self, level, msg):
        self._logger.log(level, "({}) {}".format(self._pin_name, msg))

    def __setup_button(self, pin_id):
        self._button = digitalio.DigitalInOut(pin_id)
        self._button.switch_to_input()
        self._button.pull = digitalio.Pull.UP

        self.__log(logging.INFO, "Button configured on pin {}".format(pin_id))
        self._pin_name = str(pin_id)

    async def start(
        self,
        pin_id=None,
        hold_time: float = None,
    ):
        # Set optional args if they have been provided
        if pin_id is not None:
            self._button.deinit()
            self.__setup_button(pin_id)
        if hold_time is not None:
            self.hold_time = hold_time

        await self.__monitor_button()

    def __press(self):
        self._pressed = True
        self._pressed_time = time.monotonic_ns()

    def __release(self):
        self._pressed = False

    async def __monitor_button(self):
        # Detect if button is pressed, released, or held
        while True:
            if self.__button_pressed():  # pressed
                # Only trigger a press event if the button is not already pressed
                if not self.pressed:
                    self.__press()
            else:  # released
                # Only trigger a release event if the button is pressed
                if self.pressed:
                    self.__release()
            # Wait 5 ms before polling key again
            await asyncio.sleep(0.005)

    def __button_pressed(self):
        return self._button.value == self._active_high

    @property
    def name(self):
        return self._pin_name

    @property
    def pressed(self):
        return self._pressed

    @property
    def key(self):
        return self._key_value

    @property
    def press_stamp(self):
        return self._pressed_time
