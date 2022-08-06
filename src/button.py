import time
import asyncio

import digitalio
import adafruit_logging as logging


class ButtonFunction:
    def __init__(self, function: callable, *args, **kwargs):
        if not callable(function):
            raise ValueError("Button function must be callable")
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.function(*self.args, **self.kwargs)

    def __str__(self):
        return "{}({}, {})".format(self.function, self.args, self.kwargs)


class Button:
    def __init__(
        self,
        pin_id,
        press_func: ButtonFunction = None,
        release_func: ButtonFunction = None,
        hold_func: ButtonFunction = None,
        hold_time: float = 1.0,
    ):
        """Create a button object representing a physical button connected to
        the given pin_id.

        Args:
            pin_id (Pin): The pin to which the button is connected. Must come
            from `board` module.
            press_func (ButtonFunction, optional): A function implementing an
            action when the button is pressed. Defaults to None.
            release_func (ButtonFunction, optional): A function implementing an
            action when the button is released. Defaults to None.
            hold_func (ButtonFunction, optional): A function implementing an
            action when the button is held for `hold_time` seconds. Defaults to
            None.
            hold_time (float, optional): The time the button must be held for
            to register as held. Defaults to 1.0.
        """
        self.__pin_name = str(pin_id)
        self.__logger = logging.getLogger("Button")

        # Set up functions to call when button is pressed, released, or held
        self._press_func = self._release_func = self._hold_func = None
        self.__setup_functions(press_func, release_func, hold_func)

        self.hold_time = hold_time

        # Initialise button
        self.__setup_button(pin_id)

    def __log(self, level, msg):
        self.__logger.log(level, "({}) {}".format(self.__pin_name, msg))

    def __setup_button(self, pin_id):
        self.button = digitalio.DigitalInOut(pin_id)
        self.button.switch_to_input()
        self.button.pull = digitalio.Pull.UP

        self.__log(logging.INFO, "Button configured on pin {}".format(pin_id))
        self.__pin_name = str(pin_id)

    def __setup_functions(self, press_func, release_func, hold_func):
        if isinstance(press_func, ButtonFunction):
            self._press_func = press_func
        elif press_func is not None:
            raise ValueError("press_func must be a ButtonFunction")

        if isinstance(release_func, ButtonFunction):
            self._release_func = release_func
        elif release_func is not None:
            raise ValueError("release_func must be a ButtonFunction")

        if isinstance(hold_func, ButtonFunction):
            self._hold_func = hold_func
        elif hold_func is not None:
            raise ValueError("hold_func must be a ButtonFunction")

    async def start(
        self,
        pin_id=None,
        press_func: ButtonFunction = None,
        release_func: ButtonFunction = None,
        hold_func: ButtonFunction = None,
        hold_time: float = None,
    ):
        # Set optional args if they have been provided
        if pin_id is not None:
            self.button.deinit()
            self.__setup_button(pin_id)
        self.__setup_functions(press_func, release_func, hold_func)
        if hold_time is not None:
            self.hold_time = hold_time

        await self.__monitor_button()

    async def __monitor_button(self):
        pressed = False
        press_time = time.monotonic()
        # Detect if button is pressed, released, or held
        while True:
            if self.button_pressed():  # pressed
                # Only trigger a press event if the button is not already pressed
                if not pressed:
                    pressed = True
                    press_time = time.monotonic()
                    self.__button_pressed()
                if time.monotonic() > press_time + self.hold_time:
                    self.__button_held()
            else:  # released
                # Only trigger a release event if the button is pressed
                if pressed:
                    pressed = False
                    self.__button_released()
            # Wait 5 ms before polling key again
            await asyncio.sleep(0.005)

    def button_pressed(self):
        return not self.button.value

    def __button_pressed(self):
        if isinstance(self._press_func, ButtonFunction):
            self.__log(logging.DEBUG, "Button pressed")
            self._press_func()

    def __button_released(self):
        if isinstance(self._release_func, ButtonFunction):
            self.__log(logging.DEBUG, "Button released")
            self._release_func()

    def __button_held(self):
        if isinstance(self._hold_func, ButtonFunction):
            self.__log(logging.DEBUG, "Button held")
            self._hold_func()
