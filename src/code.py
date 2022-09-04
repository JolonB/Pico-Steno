"""
THIS IS SAMPLE CODE
DON'T BOTHER RUNNING THIS
"""

import asyncio

import board

import backlight
import button
import keymap
import txbolt


PROCESS_TIMEOUT = 0.001


async def process_keys(keys, tx: txbolt.TXBolt):
    # Track the timestamp of each key press
    key_timestamps = [0.0] * len(keys)
    for key in keys:
        asyncio.create_task(key.start())

    print("Buttons started")

    keys_pressed = set()
    while True:
        none_pressed = True
        for index, key in enumerate(keys):
            if key.pressed:
                key_action = key.key

                if callable(key_action):
                    pressed_time = key.press_stamp
                    # If the key is callable, call the function only if this is a new keypress
                    if pressed_time != key_timestamps[index]:
                        # Also update the timestamp
                        key_timestamps[index] = pressed_time
                        key_action()
                else:
                    # Otherwise, assume it is a steno key and send the data
                    none_pressed = False
                    keys_pressed.add(key_action)

        # If keys have been pressed, but none are pressed anymore, send them
        if none_pressed and keys_pressed:
            tx.write_packet(keys_pressed)
            keys_pressed = set()

        await asyncio.sleep(PROCESS_TIMEOUT)


async def main():
    # Create a backlight, which will be mapped to the pin with the LED keymap
    bklight = backlight.Backlight(board.GP28)

    # Set up buttons
    buttons = []
    for pin, keycode in keymap.steno_keys.items():
        buttons.append(button.Button(pin, keycode))
    for pin, keycode in keymap.extra_keys.items():
        if keycode == ("LED",):
            key = button.Button(pin, bklight.increment_mode)
        buttons.append(key)

    tx = txbolt.TXBolt()

    await asyncio.gather(bklight.start(), process_keys(buttons, tx))


if __name__ == "__main__":
    asyncio.run(main())
