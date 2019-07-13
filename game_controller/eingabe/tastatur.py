import random
from dataclasses import dataclass
from threading import Thread, Lock
import time
from typing import Union, Optional, List

from pynput.keyboard import Key, Controller

SLEEP_TIME = 1/100

tastaturLock = Lock()

Taste = Union[str, Key]


@dataclass
class GedrueckteTaste:
    taste: Taste
    dauer_in_sekunden: float
    prozent_aktiv: float

    start_zeit: Optional[float]
    end_zeit: float

    def __init__(self, taste: Taste, dauer_in_sekunden: float, prozent_aktiv: float) -> None:
        assert 0 < prozent_aktiv <= 1.0, f'[KEYBOARD] prozent_aktiv muss ein Prozentwert > 0 sein. War {prozent_aktiv}'
        self.taste = taste
        self.dauer_in_sekunden = dauer_in_sekunden
        self.prozent_aktiv = prozent_aktiv
        self.start_zeit = None
        self.end_zeit = time.time() + dauer_in_sekunden
        self.ist_gedrueckt = False

    @property
    def soll_geloescht_werden(self) -> bool:
        return self.end_zeit < time.time()

    @property
    def soll_gedrueckt_werden(self) -> bool:
        if self.ist_gedrueckt:
            return False
        if random.random() <= self.prozent_aktiv:
            return True
        else:
            return False

    @property
    def soll_losgelassen_werden(self) -> bool:
        if not self.ist_gedrueckt:
            return False
        if random.random() > self.prozent_aktiv:
            return True
        else:
            return False

    def druecke(self):
        self.start_zeit = time.time()
        self.end_zeit = self.start_zeit + self.dauer_in_sekunden

    def kombiniere_mit(self, neue_taste: 'GedrueckteTaste') -> None:
        assert not neue_taste.ist_gedrueckt, '[KEYBOARD] Neue Taste darf nicht gedrueckt sein'
        assert self.taste == neue_taste.taste, '[KEYBOARD] Zu kombinierende Tasten muessen gleich sein'

        self.dauer_in_sekunden = neue_taste.dauer_in_sekunden
        self.prozent_aktiv = neue_taste.prozent_aktiv
        self.end_zeit = time.time() + neue_taste.dauer_in_sekunden



class Tastatur(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        # Speichert zu jeder Taste die Zeit bis zu der sie gedrueckt bleiben soll
        self._gedrueckte_tasten = {}
        self.keyboard = Controller()
        self.ist_ausgabe_aktiv = False

    def run(self):
        while True:
            with tastaturLock:
                self._aktualisiere_tasten()
            time.sleep(SLEEP_TIME)

    def _aktualisiere_tasten(self):
        if not self.ist_ausgabe_aktiv:
            return
        tasten = list(self._gedrueckte_tasten.keys())
        for taste in tasten:
            betroffene_taste = self._gedrueckte_tasten[taste]
            if betroffene_taste.soll_geloescht_werden:
                if betroffene_taste.ist_gedrueckt:
                    self.keyboard.release(key=betroffene_taste.taste)
                del self._gedrueckte_tasten[taste]
            elif betroffene_taste.soll_gedrueckt_werden:
                betroffene_taste.ist_gedrueckt = True
                self.keyboard.press(key=betroffene_taste.taste)
            elif betroffene_taste.soll_losgelassen_werden:
                betroffene_taste.ist_gedrueckt = False
                self.keyboard.release(key=betroffene_taste.taste)

    def druecke_taste(self, taste: Taste, dauer_in_sekunden: float = float('inf'), prozent_aktiv: float = 1.0) -> None:
        neue_taste = GedrueckteTaste(taste=taste, dauer_in_sekunden=dauer_in_sekunden, prozent_aktiv=prozent_aktiv)
        with tastaturLock:
            if taste in self._gedrueckte_tasten:
                self._gedrueckte_tasten[taste].kombiniere_mit(neue_taste)
            else:
                self._gedrueckte_tasten[taste] = neue_taste

    def lasse_tasten_los(self, tasten: List[Taste]) -> None:
        for taste in tasten:
            self.lasse_taste_los(taste)

    def lasse_taste_los(self, taste: Taste) -> None:
        with tastaturLock:
            if taste in self._gedrueckte_tasten:
                betroffene_taste = self._gedrueckte_tasten[taste]
                if betroffene_taste.ist_gedrueckt:
                    self.keyboard.release(key=betroffene_taste.taste)
                del self._gedrueckte_tasten[taste]

    def deaktiviere_ausgabe(self):
        with tastaturLock:
            self.ist_ausgabe_aktiv = False
            for taste in self._gedrueckte_tasten:
                betroffene_taste = self._gedrueckte_tasten[taste]
                if betroffene_taste.ist_gedrueckt:
                    betroffene_taste.ist_gedrueckt = False
                    self.keyboard.release(key=betroffene_taste.taste)

    def aktiviere_ausgabe(self):
        with tastaturLock:
            self.ist_ausgabe_aktiv = True


tastatur = Tastatur()
