import asyncio

import websockets

from pynput.keyboard import Key
from game_controller.eingabe.tastatur import tastatur
from game_controller.eingabe.ausgabestop import starte_ausgabestop
from game_controller.klassifikation.klassifikation import hole_klassifikation

print(f'Starte Server')
tastatur.start()
starte_ausgabestop()


"""Eure Aufgabe: Ein Browserspiel fernsteuern.

<Strg + Enter> pausiert die Tastaturausgabe


Funktionen die ihr brauchen könntet:

# Vorhergesagte klasse vom Server holen (ist ein string)
klassifikation = hole_klassifikation(websocket)
klasse = klassifikation.beste_klasse.name

# Eine Taste dauerhaft drücken
tastatur.druecke_taste(Key.left, dauer_in_sekunden=float('inf'))

# Eine Taste seltener drücken



tastatur.druecke_taste(Key.left, dauer_in_sekunden=10.0, prozent_aktiv=0.7)

# Eine Taste loslassen
tastatur.lasse_taste_los(Key.left)

# Mehrere Tasten loslassen
tastatur.lasse_tasten_los([Key.left, Key.right])
"""


async def server(websocket, path):
    while True:
        klassifikation = await hole_klassifikation(websocket)
        klasse = klassifikation.beste_klasse.name

        # print(klasse)

        if klasse == "rechts":

            tastatur.druecke_taste(Key.right, dauer_in_sekunden=0.5,  prozent_aktiv=0.7)
            tastatur.lasse_taste_los(Key.left)

        elif klasse == "links":
            tastatur.lasse_taste_los(Key.right)

            tastatur.druecke_taste(Key.left, dauer_in_sekunden=0.5,  prozent_aktiv=0.7)

        elif klasse == "nichts":
            pass



start_server = websockets.serve(server, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

