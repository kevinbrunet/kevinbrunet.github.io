"""Draw an editorial diagram of zero-event one-sided binomial confidence bounds."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static/images/articles/oracle-confidence.fr.png"
W, H = 1600, 820
PAPER, INK, BLUE, CORAL = "#F3EFE6", "#121C2B", "#2457F5", "#FF5A4E"
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def font(size, bold=False):
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", size)


def text(x, y, value, size=30, bold=False, fill=INK):
    d.text((x, y), value, font=font(size, bold), fill=fill)


text(70, 45, "0,5 % est une borne haute, pas le centre de l’intervalle", 44, True)
text(70, 113, "Même test : 600 propositions incorrectes, aucune acceptée à tort", 31)
x0, x1 = 360, 1480


def x(pct):
    return x0 + (x1 - x0) * pct


target_x = x(0.5)
for y in range(210, 585, 20):
    d.line((target_x, y, target_x, y + 9), fill=CORAL, width=3)
text(target_x - 115, 185, "Borne visée : 0,5 %", 26, True, CORAL)
for c, y in [(0.95, 310), (0.99, 465)]:
    upper_pct = 100 * (-math.expm1(math.log1p(-c) / 600))
    assert 0 < upper_pct < 1
    text(70, y - 27, f"Confiance : {int(c * 100)} %", 30, True)
    d.rounded_rectangle((x0, y - 17, x(upper_pct), y + 17), radius=17, fill=BLUE)
    d.line((x0, y - 32, x0, y + 32), fill=INK, width=4)
    d.line((x(upper_pct), y - 32, x(upper_pct), y + 32), fill=INK, width=4)
    label = f"De 0 à environ {upper_pct:.2f} %".replace(".", ",")
    text(x0, y - 73, label, 29, True)

d.line((x0, 575, x1, 575), fill=INK, width=2)
for tick in [0, 0.25, 0.5, 0.75, 1]:
    px = x(tick)
    d.line((px, 575, px, 585), fill=INK, width=2)
    label = f"{tick:g} %".replace(".", ",")
    bounds = d.textbbox((0, 0), label, font=font(25))
    text(px - (bounds[2] - bounds[0]) / 2, 598, label, 25)
text(x0, 640, "Taux de fausses acceptations parmi les propositions incorrectes", 27)
text(70, 717, "À données identiques, demander 99 % de confiance élargit l’intervalle.", 29, True)
text(70, 763, "Pour ramener sa borne haute à 0,5 % à 99 %, il faut 919 cas sans fausse acceptation.", 27)
OUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUT)
print(OUT)
