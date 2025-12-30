from pathlib import Path
from typing import Optional

import discord

MAPS_DIR = Path(__file__).resolve().parents[2] / "resource" / "map"
GAME_MAPS = [
    ("World", "World"),
    ("GiantWorldMap", "Giant World Map"),
    ("Europe", "Europe"),
    ("EuropeClassic", "Europe Classic"),
    ("Mena", "Mena"),
    ("NorthAmerica", "North America"),
    ("SouthAmerica", "South America"),
    ("Oceania", "Oceania"),
    ("BlackSea", "Black Sea"),
    ("Africa", "Africa"),
    ("Pangaea", "Pangaea"),
    ("Asia", "Asia"),
    ("Mars", "Mars"),
    ("Britannia", "Britannia"),
    ("GatewayToTheAtlantic", "Gateway to the Atlantic"),
    ("Australia", "Australia"),
    ("Iceland", "Iceland"),
    ("EastAsia", "East Asia"),
    ("BetweenTwoSeas", "Between Two Seas"),
    ("FaroeIslands", "Faroe Islands"),
    ("DeglaciatedAntarctica", "Deglaciated Antarctica"),
    ("FalklandIslands", "Falkland Islands"),
    ("Baikal", "Baikal"),
    ("Halkidiki", "Halkidiki"),
    ("StraitOfGibraltar", "Strait of Gibraltar"),
    ("Italia", "Italia"),
    ("Japan", "Japan"),
    ("Pluto", "Pluto"),
    ("Montreal", "Montreal"),
    ("NewYorkCity", "New York City"),
    ("Achiran", "Achiran"),
    ("BaikalNukeWars", "Baikal (Nuke Wars)"),
    ("FourIslands", "Four Islands"),
    ("Svalmel", "Svalmel"),
    ("GulfOfStLawrence", "Gulf of St. Lawrence"),
    ("Lisbon", "Lisbon"),
    ("Manicouagan", "Manicouagan"),
    ("Lemnos", "Lemnos"),
]
MAP_KEY_TO_DISPLAY = {key: display for key, display in GAME_MAPS}
MAP_DISPLAY_TO_KEY = {display: key for key, display in GAME_MAPS}
MAP_THUMBNAILS = {key: f"{key}.webp" for key, _ in GAME_MAPS}


def normalize_map_key(map_name: str) -> Optional[str]:
    if map_name in MAP_THUMBNAILS:
        return map_name
    return MAP_DISPLAY_TO_KEY.get(map_name)


def get_thumbnail_file(map_name: str) -> Optional[discord.File]:
    key = normalize_map_key(map_name)
    if not key:
        return None
    filename = MAP_THUMBNAILS.get(key)
    if not filename:
        return None
    path = MAPS_DIR / filename
    if not path.exists():
        return None
    return discord.File(path, filename=filename)
