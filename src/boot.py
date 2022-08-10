import usb_cdc
import usb_hid
import usb_midi

usb_cdc.enable(console=True,data=True)
usb_midi.disable()
usb_hid.enable()
