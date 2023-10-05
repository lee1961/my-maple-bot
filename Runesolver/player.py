from interception.stroke import key_stroke
import time

SC_DECIMAL_ARROW = {
    "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
}


SC_DECIMAL_ARROW = {
    "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
}

SC_DECIMAL = {
    "ALT": 56, "SPACE": 57, "CTRL": 29, "SHIFT": 42,
    "Q": 16, "W": 17, "E": 18, "R": 19, "T" : 20, "Y": 21, "U":22,
    "A": 30, "S": 31, "D": 32, "F": 33, "G": 34, "H":35, "J":36,
    "Z": 44, "X": 45, "C": 46, "V": 47, "B": 48, "N": 49, "O":24,
    "1": 2, "2": 3, "3": 4, "4": 5, "5": 5, "6": 7, "7": 8, "8": 9, "9": 10, "0" : 11,
    "F9" : 67, "F10": 68, "F8" : 66, "INS" : 82, "F3" : 61, "F4": 62, "F1": 59, "ESC": 1, "ENTER": 28
}

JUMP_KEY = "ALT"
ROPE_LIFT_KEY = "J"


class Player:
    def __init__(self, context, device, game):
        self.game = game
        # interception
        self.context = context
        self.device = device

    def release_all(self):
        for key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        for key in SC_DECIMAL:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def press(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def release(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def hold(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))

    def go_to(self, target):
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                continue

            x1, y1 = player_location
            x2, y2 = target


            if abs(x1 - x2) < 2:
                self.release_all()
                if abs(y2 - y1) < 7:
                    self.release_all()
                    break
                elif y1 < y2:
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                else:
                    if y1 - y2 > 1:
                        self.press(ROPE_LIFT_KEY)
                        self.hold("UP")
                    else:
                        self.hold("UP")
                time.sleep(1.5)
            else:
                if x1 < x2:
                    self.hold("RIGHT")
                    self.release("LEFT")
                else:
                    self.hold("LEFT")
                    self.release("RIGHT")
                if abs(x2 - x1) > 20:
                    self.press(JUMP_KEY)
                    self.press(JUMP_KEY)

