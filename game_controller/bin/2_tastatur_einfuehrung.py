import time

from pynput.keyboard import Key

from game_controller.eingabe.tastatur import tastatur
from game_controller.eingabe.ausgabestop import starte_ausgabestop

tastatur.start()
# starte_ausgabestop()
tastatur.aktiviere_ausgabe()

# tastatur.druecke_taste("a", dauer_in_sekunden=30, prozent_aktiv=0.7)
# tastatur.aktiviere_ausgabe()

time.sleep(5)


"""
Eure Aufgabe: 'Hhhhhhaaaaaallllllllllllllooooooo' in eine Textdatei schreiben.
<Strg + Enter> startet (und pausiert) die Tastaturausgabe

Funktionen die ihr brauchen werdet:

# Taste eine bestimmte Zeit drücken
tastatur.druecke_taste('a', dauer_in_sekunden=0.1)
"""

# Euer Code kommt hier hin

# tastatur.druecke_taste('H', dauer_in_sekunden=0.1)
tastatur.druecke_taste(Key.shift, dauer_in_sekunden=0.4)
tastatur.druecke_taste('h', dauer_in_sekunden=0.4)
time.sleep(0.4)
tastatur.druecke_taste('a', dauer_in_sekunden=0.6)
time.sleep(0.6)
tastatur.druecke_taste('l', dauer_in_sekunden=1, prozent_aktiv=0.7)
time.sleep(1)
tastatur.druecke_taste('o', dauer_in_sekunden=1)
time.sleep(1)


time.sleep(10)