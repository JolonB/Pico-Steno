import board
import i2c_conf

# Set up default keycodes
# S, T, K, P, W, H, R, A, O, STAR, E, U, F, R2, P2, B, L, G, T2, S2, D, Z
steno_keys = {
    board.GP0: "S-",
    board.GP1: "T-",
    board.GP2: "K-",
    board.GP3: "P-",
    board.GP4: "W-",
    board.GP5: "H-",
    board.GP6: "R-",
    board.GP7: "A-",
    board.GP8: "O-",
    board.GP9: "*",
    board.GP10: "-E",
    board.GP11: "-U",
    board.GP12: "-F",
    board.GP13: "-R",
    board.GP14: "-P",
    board.GP15: "-B",
    board.GP16: "-L",
    board.GP17: "-G",
    board.GP18: "-T",
    board.GP19: "-S",
    board.GP20: "-D",
    board.GP21: "-Z",
    board.GP22: "#",
}


extra_keys = {}
if i2c_conf.USING_I2C:
    extra_keys["I2C0"] = i2c_conf.I2C_KEY0
    extra_keys["I2C1"] = i2c_conf.I2C_KEY1
    extra_keys["I2C2"] = i2c_conf.I2C_KEY2
    extra_keys["I2C3"] = i2c_conf.I2C_KEY3
    extra_keys["I2C4"] = i2c_conf.I2C_KEY4
    extra_keys["I2C5"] = i2c_conf.I2C_KEY5
    extra_keys["I2C6"] = i2c_conf.I2C_KEY6
    extra_keys["I2C7"] = ("LED",)
else:
    extra_keys[board.GP27] = ("LED",)
