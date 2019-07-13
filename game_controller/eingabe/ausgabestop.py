from pynput import keyboard
from pynput.keyboard import Key
from game_controller.eingabe.tastatur import tastatur


alt_pressed = False
ctrl_pressed = False


def on_press(key):
    try:
        global alt_pressed
        global ctrl_pressed
        if key == Key.alt:
            alt_pressed = True
        elif key == Key.ctrl:
            ctrl_pressed = True
        if key == Key.enter and ctrl_pressed and alt_pressed:
            if tastatur.ist_ausgabe_aktiv:
                print('[KEYBOARD] Stoppe Ausgabe')
                tastatur.deaktiviere_ausgabe()
            else:
                print('[KEYBOARD] Starte Ausgabe')
                tastatur.aktiviere_ausgabe()
    except Exception:
        pass


def on_release(key):
    try:
        global alt_pressed
        global ctrl_pressed
        if key == Key.alt:
            alt_pressed = False
        elif key == Key.ctrl:
            ctrl_pressed = False
    except Exception:
        pass


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)


def starte_ausgabestop():
    listener.start()
