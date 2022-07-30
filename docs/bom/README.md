# Bill of Materials

The parts and prices shown in [`bom.csv`](bom.csv) are based on products available at DigiKey and, for most components, are only a suggestion.
The price isn't great, but you are able to purchase the same/similar components elsewhere for lower prices.
For example, AliExpress is a great place to look for the LEDs, MOSFETs, resistors, and even switches.  
As long as the component fits the footprint, there should be no issues.
Instead of buying proper Cherry MX switches, you could get pin-compatible switches from Kailh or Outemu for possibly half the price.  
If you want LED backlighting, make sure you choose an LED that fits in the switch.
The BOM uses a 1.8mm (green\*) LED which is the best type for Kailh switches.

\*Feel free to use any colour.

## Do I need to buy all of these?

No!

A "minimal" BOM is shown in [`bom_min.csv`](bom_min.csv).
This removes a few of the extra switches (marked by `Xn`) as well as the I2C expander than interfaces with them.

This *technically* isn't the true minimal BOM.
If you choose to, you can remove the LED backlighting by getting rid of:

- 1 switch (LED setting)
- 1 2N7000
- 27 LEDs
- 1 10k resistor
- 29 1k resistors

which will make the BOM consist of only the SC0915 (Raspberry Pi Pico) and the 26 remaining switches.
Buying the switches from AliExpress makes the true minimal *component* BOM no more than NZ$30 (excl. shipping).
