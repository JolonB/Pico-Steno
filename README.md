# Pico-Steno

An open-source Raspberry Pi Pico stenography keyboard.

I promise I'll write more here soon.

Gerber files can be found [here](hardware/gerber/).
I have not yet ordered a PCB with these gerber files, so they may have issues.

The bill of materials can be found [here](docs/bom/).

![pcb front](docs/img/pcb_3d_f.png)

![pcb back](docs/img/pcb_3d_b.png)

## Questions

### Why doesn't this use a keyboard matrix?

Good question.

1. The RPi Pico has enough GPIO pins to dedicate one to each key on a stenography keyboard.
Basically, I just though that was neat, so decided to do it that way.
I then decided I wanted optional extra keys, so added the IO extender.
1. This allows me to implement n-key rollover without needing any diodes; not that they are particularly expensive.

### Why is the circuit so messy?

That's what happens when each key is connected directly to the microcontroller without optimising the which switch connects to which pin.  
But hey, this is open source; if it bugs you, feel free to fork it!
