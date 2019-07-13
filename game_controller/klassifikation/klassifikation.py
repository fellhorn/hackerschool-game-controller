import json
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Klasse:
    name: str
    konfidenz: float


@dataclass
class Klassifikation:
    def __init__(self, klassifikation_als_dict: Dict[str, Any]):
        self.zeit_in_sekunden: float = float(klassifikation_als_dict['zeit'])
        self.klassen: List[Klasse] = []
        for klasse in klassifikation_als_dict['klassen']:
            konvertierte_klasse = Klasse(name=str(klasse['name']), konfidenz=float(klasse['konfidenz']))
            self.klassen.append(konvertierte_klasse)

    @property
    def beste_klasse(self):
        return max(self.klassen, key=lambda klasse: klasse.konfidenz)


async def hole_klassifikation(websocket) -> Klassifikation:
    klassifikation_als_string = await websocket.recv()
    klassifikation_als_dict = json.loads(klassifikation_als_string)
    return Klassifikation(klassifikation_als_dict)
