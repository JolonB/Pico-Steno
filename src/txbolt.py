import usb_cdc

class TXBolt:
    __PACKET_LEN = 5
    __STENO_KEY_CHART = (
        ("S-", "T-", "K-", "P-", "W-", "H-"),  # 00
        ("R-", "A-", "O-", "*", "-E", "-U"),  # 01
        ("-F", "-R", "-P", "-B", "-L", "-G"),  # 10
        ("-T", "-S", "-D", "-Z", "#"),
    )  # 11

    def __init__(self):
        if len(self.__STENO_KEY_CHART) != self.__PACKET_LEN - 1:
            raise ValueError(
                "The steno key chart must contain {} groups".format(
                    self.__PACKET_LEN - 1
                )
            )

        self.packet = self._init_packet()

    def _init_packet(self):
        # The packet has 4 bytes in it
        # Initialise the first 2 bits of each byte to the index
        # The resulting packet should be:
        # 00000000 01000000 10000000 11000000
        packet = bytearray(self.__PACKET_LEN)
        # Set all of the packets, except for the last one, which is key release
        for i in range(self.__PACKET_LEN - 1):
            packet[i] |= i << 6
        return packet

    def _clear_packet(self):
        for i in range(self.__PACKET_LEN):
            self.packet[i] &= ~63  # Clear the lower 6 bits

    def write_packet(self, letters: set):
        self._clear_packet()
        self._fill_packet(letters)
        usb_cdc.data.write(self.packet)

    def _fill_packet(self, letters: set):
        # Iterate over each group in the steno key chart
        for index, key_set in enumerate(self.__STENO_KEY_CHART):
            # Iterate over each inner key
            for key_index, key in enumerate(key_set):
                # If the key was pressed, mark it as 1
                if key in letters:
                    self.packet[index] |= 1 << key_index

    def packet_to_bin(self):
        return "".join(
            "{:08b} ".format(byte) for byte in self.packet
        )