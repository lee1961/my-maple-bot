import time
import random
from playsound import playsound
import main
from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player

#===============================================================================================================
# Take a Screenshot of your game
# Open that screenshot in paint (Right click > Edit OR Right click > open with > paint)
# Point your mouse to the btm right corner minimap in the screenshot and look at the btm left corner of paint
# There should be 2 numbers. First number is for X and Second number is for Y

# Save your coordinates for maps that you frequently used here
# E.G. Eotw 1-4 (160,140)
#
#lh2 - 178x128
#eotw 2-5 -170x158

# for main shad in limina
minimapX = 169
minimapY = 167
# minimapX = 170
# minimapY = 157

#for shad, vc3 
# minimapX = 178 
# minimapY = 137

#for minis had
# minimapX = 177
# minimapY = 144

currentTime = time.time()
targetedTime = currentTime + 5


#===============================================================================================================
def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device


def function_alarm():
    playsound("alarm.mp3")


def solve_rune(g, p, target):
    attempts = 0
    while True:
        print("Pathing towards rune...")
        p.go_to(target)
        # Activate the rune.
        time.sleep(1)
        p.press("SPACE")
        # Take a picture of the rune.
        time.sleep(1.5)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            time.sleep(1)
            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                p.press("F4")
                break
            else:
                print("Trying again...")
        else:
            print("Rune unidentifiable. Trying again...")
            p.press("SPACE")
            p.hold("UP")
            time.sleep(1)
            p.release("UP")
            main.function_alarm()
            time.sleep(1.5)
            attempts += 1
            if attempts > 3:
                print("Entering Cashshop..")
                p.press("F1")
                time.sleep(9)
                print("Exiting Cashshop")
                time.sleep(5)
                p.press("ESC")
                time.sleep(0.5)
                p.press("ESC")
                time.sleep(0.5)
                p.press("ENTER")
                time.sleep(2.5)
                attempts = 0

if __name__ == "__main__":
    c = interception()
    d = bind(c)

    g = Game((5, 60, minimapX, minimapY))
    p = Player(c, d, g)
    target = (97, 32.5)

    while True:
        currentTime = time.time()
        other_location = g.get_other_location()

        fma1 = time.time() + 0
        fma2 = time.time()
        fma3 = time.time() + 45
        summon1 = time.time()


        if other_location > 0:
            print("A player has entered your map.")

        rune_location = g.get_rune_location()
        if rune_location is not None:
            print("A rune has appeared.")
            p.press("F4")
            solve_rune(g, p, rune_location)
        else:
            currentTime = time.time()
            if (fma1 - time.time() <= 0):
                p.hold("1")
                print("pressing fma1")
                time.sleep(3000)
                p.release("1")
                fma1 = time.time() + 180
            # if (fma2 - time.time() <= 0):
            #     p.press("2")
            #     print("pressing fma2")
            #     fma1 = time.time() + 180
            if (fma3 - time.time() <= 0):
                p.press("3")
                print("pressing fma3")
                fma3 = time.time() + 180
            if (currentTime > targetedTime):         
                p.press("F4")
                time.sleep(1)
                p.press("Z")
                time.sleep(2)
                p.release("Z")
                print("pressig z")

                print("setting currenttime to be this")
                targetedTime = currentTime + 60
                p.hold("DOWN")
                p.hold("D")
                time.sleep(0.8)
                p.release("DOWN")
                p.release("D")
                time.sleep(0.5)
                p.press("F4")
            


        print("Running...")
        time.sleep(3)
