"""Police Unicode commune aux images générées pour l'atelier."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

CHEMIN_POLICE = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "DejaVuSans.ttf"


@lru_cache(maxsize=32)
def police_unicode(taille: int):
    """Renvoie DejaVu Sans, jamais la police bitmap aux accents incomplets."""
    if not CHEMIN_POLICE.is_file():
        raise FileNotFoundError(f"Police Unicode attendue dans le kit : {CHEMIN_POLICE}")
    return ImageFont.truetype(str(CHEMIN_POLICE), int(taille))
