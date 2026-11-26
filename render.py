#!/usr/bin/env python3
"""Sum 25 Round 5 — news-image-20261125 broadsheet renderer.

Draws the 1024x1024 broadsheet exactly as specified in BRIEF-R5.md.
Deterministic: no randomness, no timestamps, no network.
Writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

NAVY = (20, 33, 61)
NAVY2 = (27, 42, 74)
RED = (192, 39, 43)
RED_D = (160, 28, 32)
BLACK = (20, 20, 20)
GREY = (90, 90, 90)
GREY_L = (200, 200, 200)
GREY_BG = (245, 245, 243)
WHITE = (255, 255, 255)
GREEN = (31, 122, 60)
GREEN_BG = (220, 240, 224)
AMBER = (150, 100, 0)
AMBER_BG = (252, 236, 190)
BLUE = (30, 90, 160)
TEAL = (0, 120, 115)
PURPLE = (110, 60, 150)
ORANGE = (200, 100, 0)
BEIGE = (208, 188, 158)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def serif_b(size):
    return font(SERIF_B, size)


def serif(size):
    return font(SERIF, size)


def sans(size):
    return font(SANS, size)


def sans_b(size):
    return font(SANS_B, size)


def tw(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(path, s, size, maxw, minsize, draw):
    while size > minsize and tw(draw, s, font(path, size)) > maxw:
        size -= 1
    return size


def draw_wrapped(draw, x, y, s, f, color, maxw, lh):
    for ln in wrap(draw, s, f, maxw):
        draw.text((x, y), ln, font=f, fill=color)
        y += lh
    return y


def chip(draw, x, y, label):
    """Verification / tag chip. Returns width used."""
    colors = {
        "CONFIRMED": (GREEN, GREEN_BG),
        "REPORTED": (AMBER, AMBER_BG),
        "OFFICIAL": ((15, 90, 50), (205, 235, 210)),
        "CLAIM": (ORANGE, (255, 230, 200)),
        "FORECAST": (BLUE, (215, 232, 250)),
        "SCHEDULED": (PURPLE, (235, 220, 245)),
        "SPORT": (RED_D, (250, 215, 215)),
        "MKT": (TEAL, (205, 240, 238)),
    }
    fg, bg = colors.get(label, (GREY, GREY_BG))
    f = sans_b(8)
    w = int(tw(draw, label, f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=bg,
                           outline=fg, width=1)
    draw.text((x + 5, y + 2), label, font=f, fill=fg)
    return w


def badge(draw, x, y, n):
    """Red circle number badge, top-left over scene corner."""
    r = 11
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED,
                 outline=WHITE, width=2)
    s = str(n)
    f = sans_b(11 if len(s) < 2 else 10)
    draw.text((x + r - tw(draw, s, f) / 2, y + 5), s, font=f, fill=WHITE)


def scene_label(draw, box, text, size=20, color=WHITE, bg=None, yoff=0):
    """Big data label baked inside a scene, centred, with dark outline."""
    x, y, w, h = box
    f = sans_b(size)
    while tw(draw, text, f) > w - 8 and size > 9:
        size -= 1
        f = sans_b(size)
    tx = x + (w - tw(draw, text, f)) / 2
    ty = y + (h - size) / 2 + yoff
    if bg is not None:
        pad = 5
        draw.rounded_rectangle(
            [tx - pad, ty - 2, tx + tw(draw, text, f) + pad, ty + size + 3],
            radius=4, fill=bg)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1),
                   (-1, 1), (1, 1)):
        draw.text((tx + dx, ty + dy), text, font=f, fill=(30, 30, 30))
    draw.text((tx, ty), text, font=f, fill=color)
    return size


def point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (
                px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- scenes
def scene_clinic(draw, x, y, w, h):
    """Hero 1: bright daylight clinic, white building, red cross, ambulance."""
    draw.rectangle([x, y, x + w, y + h], fill=(178, 216, 240))
    draw.ellipse([x + w - 52, y + 6, x + w - 30, y + 28], fill=(255, 244, 200))
    for tx, ty in ((12, h - 46), (w - 34, h - 52), (w - 70, h - 40)):
        draw.ellipse([x + tx, y + ty, x + tx + 26, y + ty + 22],
                     fill=(70, 150, 80))
        draw.rectangle([x + tx + 11, y + ty + 18, x + tx + 15, y + ty + 34],
                       fill=(90, 70, 40))
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 185, 110))
    # clinic building
    bx, by, bw, bh = x + 18, y + 34, 120, h - 52
    draw.rectangle([bx, by, bx + bw, by + bh], fill=WHITE,
                   outline=(180, 180, 180))
    draw.rectangle([bx, by, bx + bw, by + 12], fill=(200, 30, 30))
    draw.rectangle([bx + bw / 2 - 4, by + 22, bx + bw / 2 + 4, by + 42],
                   fill=(200, 30, 30))
    draw.rectangle([bx + bw / 2 - 11, by + 29, bx + bw / 2 + 11, by + 35],
                   fill=(200, 30, 30))
    for wx in (bx + 12, bx + 52, bx + 88):
        draw.rectangle([wx, by + 52, wx + 22, by + 72], fill=(170, 210, 235),
                       outline=NAVY)
    # ambulance
    ax, ay = x + w - 118, y + h - 44
    draw.rectangle([ax, ay, ax + 100, ay + 26], fill=WHITE,
                   outline=(150, 150, 150))
    draw.rectangle([ax + 62, ay, ax + 100, ay + 26], fill=(235, 235, 235),
                   outline=(150, 150, 150))
    draw.rectangle([ax + 24, ay + 6, ax + 30, ay + 20], fill=(200, 30, 30))
    draw.rectangle([ax + 17, ay + 10, ax + 37, ay + 16], fill=(200, 30, 30))
    for cx in (ax + 18, ax + 80):
        draw.ellipse([cx, ay + 22, cx + 12, ay + 34], fill=(30, 30, 30))
    # two figures in light protective suits
    for fx in (x + 150, x + 172):
        draw.ellipse([fx, y + h - 58, fx + 12, y + h - 46], fill=(240, 248, 255),
                     outline=(120, 160, 200))
        draw.rectangle([fx + 1, y + h - 46, fx + 11, y + h - 20],
                       fill=(230, 240, 250), outline=(120, 160, 200))


def scene_rocket(draw, x, y, w, h):
    """Hero 2: night launch, rocket CENTRED on its body axis."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 16, 42))
    for sx, sy in ((14, 12), (40, 30), (w - 60, 10), (w - 30, 40),
                   (60, 8), (w - 90, 26), (24, 52), (w - 44, 66)):
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # small station arc top-right
    draw.arc([x + w - 78, y + 4, x + w - 8, y + 34], start=200, end=340,
             fill=(200, 210, 235), width=3)
    cx = x + w / 2
    # launch tower to one side
    draw.rectangle([cx - 88, y + 30, cx - 68, y + h - 8], fill=(90, 95, 110))
    for ty in range(int(y + 38), int(y + h - 12), 14):
        draw.line([cx - 88, ty, cx - 68, ty + 8], fill=(60, 64, 78), width=2)
    # flame below rocket
    draw.polygon([(cx - 16, y + h - 42), (cx + 16, y + h - 42),
                  (cx + 7, y + h - 6), (cx, y + h - 2), (cx - 7, y + h - 6)],
                 fill=(255, 170, 30))
    draw.polygon([(cx - 9, y + h - 42), (cx + 9, y + h - 42),
                  (cx, y + h - 14)], fill=(255, 230, 120))
    # rocket body, centred on cx
    bw = 34
    top = y + 12
    bot = y + h - 42
    draw.rectangle([cx - bw / 2, top + 22, cx + bw / 2, bot], fill=(220, 30, 30))
    draw.rectangle([cx - bw / 2, top + 22, cx - bw / 2 + 7, bot],
                   fill=(255, 255, 255))
    draw.rectangle([cx + bw / 2 - 7, top + 22, cx + bw / 2, bot],
                   fill=(255, 255, 255))
    draw.polygon([(cx - bw / 2, top + 22), (cx + bw / 2, top + 22),
                  (cx, top)], fill=(240, 240, 240))
    draw.rectangle([cx - bw / 2 - 8, bot - 8, cx - bw / 2, bot + 4],
                   fill=(200, 200, 200))
    draw.rectangle([cx + bw / 2, bot - 8, cx + bw / 2 + 8, bot + 4],
                   fill=(200, 200, 200))
    # "24" on the rocket body, centred on the body axis
    f = sans_b(15)
    draw.text((cx - tw(draw, "24", f) / 2, top + 44), "24", font=f, fill=WHITE)
    # ground + smoke
    draw.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 44, 60))
    draw.ellipse([cx - 70, y + h - 22, cx - 30, y + h - 6], fill=(120, 125, 140))
    draw.ellipse([cx + 30, y + h - 20, cx + 72, y + h - 6], fill=(120, 125, 140))


def scene_cricket(draw, x, y, w, h):
    """Hero 3: night match, floodlit green outfield, scoreboard 204 OFF 53."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 90, 45))
    draw.ellipse([x + 8, y + h - 30, x + w - 8, y + h - 6], fill=(24, 110, 55))
    draw.rectangle([x, y, x + w, y + 26], fill=(16, 22, 48))
    for px in (x + 14, x + w - 22):
        draw.rectangle([px, y + 8, px + 4, y + 52], fill=(120, 125, 140))
        draw.rectangle([px - 8, y + 4, px + 12, y + 12], fill=(255, 244, 190))
    # scoreboard top-right inside scene
    draw.rectangle([x + w - 108, y + 30, x + w - 10, y + 56], fill=(10, 10, 10),
                   outline=(255, 210, 60), width=2)
    f = sans_b(13)
    draw.text((x + w - 103, y + 36), "204 OFF 53", font=f, fill=(255, 210, 60))
    # pitch strip
    draw.rectangle([x + 30, y + h - 52, x + w - 30, y + h - 14],
                   fill=(210, 185, 140))
    # stumps
    for sx in (x + 52, x + 58, x + 64):
        draw.rectangle([sx, y + h - 44, sx + 3, y + h - 28], fill=(240, 210, 90))
    # batsman mid-swing, dark kit
    draw.ellipse([x + 128, y + h - 78, x + 142, y + h - 64], fill=(60, 40, 30))
    draw.rectangle([x + 126, y + h - 64, x + 144, y + h - 34],
                   fill=(20, 30, 60))
    draw.rectangle([x + 128, y + h - 34, x + 134, y + h - 16], fill=(230, 230, 230))
    draw.rectangle([x + 138, y + h - 34, x + 144, y + h - 16], fill=(230, 230, 230))
    draw.line([x + 144, y + h - 56, x + 168, y + h - 78], fill=(200, 160, 90),
              width=4)
    draw.ellipse([x + 166, y + h - 84, x + 180, y + h - 70], fill=(255, 255, 255))
    # ball
    draw.ellipse([x + 196, y + h - 88, x + 204, y + h - 80], fill=(200, 30, 30))


def scene_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(150, 105, 60))
    draw.rectangle([x, y, x + w, y + 18], fill=(90, 60, 35))
    draw.rectangle([x + 14, y + 22, x + w - 14, y + h - 8], fill=(110, 72, 40))
    draw.rectangle([x + w - 34, y + 6, x + w - 18, y + 20], fill=(200, 30, 30))
    draw.rectangle([x + w - 34, y + 6, x + w - 18, y + 9], fill=WHITE)
    draw.ellipse([x + w / 2 - 8, y + 12, x + w / 2 + 8, y + 28], fill=(230, 200, 160))
    draw.rectangle([x + w / 2 - 12, y + 28, x + w / 2 + 12, y + h - 10],
                   fill=(30, 30, 30))


def scene_moscow(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(14, 18, 40))
    for bx, bw, bh in ((6, 26, 22), (38, 20, 30), (64, 30, 18), (100, 24, 26),
                       (130, 28, 20), (164, 22, 28)):
        draw.rectangle([x + bx, y + h - 14 - bh, x + bx + bw, y + h - 14],
                       fill=(40, 48, 80))
        draw.rectangle([x + bx + 4, y + h - 10 - bh, x + bx + 8, y + h - 6 - bh],
                       fill=(255, 220, 120))
    for cx in range(10, int(w), 22):
        draw.ellipse([x + cx, y + h - 11, x + cx + 3, y + h - 8],
                     fill=(255, 200, 60))
        draw.ellipse([x + cx - 1, y + h - 14, x + cx + 4, y + h - 11],
                     fill=(255, 230, 150))


def scene_pact(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(120, 90, 55))
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(90, 60, 35))
    # two flags
    draw.rectangle([x + 12, y + 8, x + 44, y + 26], fill=(0, 40, 120))
    draw.rectangle([x + 12, y + 8, x + 44, y + 13], fill=WHITE)
    draw.rectangle([x + 12, y + 21, x + 44, y + 26], fill=WHITE)
    draw.rectangle([x + w - 46, y + 8, x + w - 14, y + 26], fill=(0, 90, 160))
    draw.rectangle([x + w - 46, y + 14, x + w - 14, y + 20], fill=(255, 210, 0))
    # signed document
    draw.rectangle([x + w / 2 - 30, y + 24, x + w / 2 + 30, y + h - 4],
                   fill=WHITE, outline=(120, 120, 120))
    for ly in (y + 30, y + 36, y + 42):
        draw.line([x + w / 2 - 24, ly, x + w / 2 + 24, ly], fill=(150, 150, 150))
    draw.line([x + w / 2 - 24, y + h - 10, x + w / 2 - 2, y + h - 14],
              fill=(30, 60, 160), width=2)


def scene_port(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(200, 225, 240))
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(60, 110, 160))
    for cx in (18, 70, 122):
        draw.line([x + cx, y + 6, x + cx, y + h - 16], fill=(60, 60, 60), width=3)
        draw.line([x + cx, y + 8, x + cx + 34, y + 16], fill=(60, 60, 60), width=2)
    for bx, bc in ((20, (200, 60, 40)), (52, (40, 120, 180)), (86, (220, 160, 40)),
                   (120, (60, 160, 90))):
        draw.rectangle([x + bx, y + h - 30, x + bx + 26, y + h - 16], fill=bc)
    draw.rectangle([x + w - 58, y + h - 26, x + w - 10, y + h - 16],
                   fill=(40, 40, 40))
    draw.ellipse([x + w - 40, y + 4, x + w - 22, y + 18], fill=(120, 120, 120))
    draw.ellipse([x + w - 30, y + 10, x + w - 14, y + 22], fill=(150, 150, 150))


def scene_chart(draw, x, y, w, h, bars, label_top=True):
    draw.rectangle([x, y, x + w, y + h], fill=(245, 245, 245))
    maxv = max(v for _, v in bars)
    bw = (w - 16) / len(bars)
    base = y + h - 6
    for i, (lab, v) in enumerate(bars):
        bh = (h - 22) * v / maxv
        bx = x + 8 + i * bw + 2
        draw.rectangle([bx, base - bh, bx + bw - 4, base], fill=(30, 60, 120))
        f = sans_b(7)
        draw.text((bx, base - bh - 9), lab, font=f, fill=NAVY)
    draw.line([x + 4, base, x + w - 4, base], fill=(120, 120, 120), width=1)


def scene_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(230, 190, 140))
    for bx in (8, 46, 84, 122, 158):
        draw.rectangle([x + bx, y + 14, x + bx + 32, y + h - 6],
                       fill=(180, 150, 120), outline=(120, 100, 80))
        for wy in (y + 20, y + 32):
            draw.rectangle([x + bx + 5, wy, x + bx + 13, wy + 7],
                           fill=(90, 70, 50))
    # damaged building + smoke column
    draw.polygon([(x + 84, y + 14), (x + 116, y + 14), (x + 108, y + 26),
                  (x + 92, y + 26)], fill=(120, 95, 70))
    draw.ellipse([x + 92, y + 0, x + 112, y + 16], fill=(110, 110, 110))
    draw.ellipse([x + 86, y + 4, x + 104, y + 20], fill=(140, 140, 140))


def scene_market(draw, x, y, w, h):
    """Card 10: supermarket front at dawn, shutters OPEN, figures walking out."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 205, 130))
    draw.ellipse([x + 12, y + 4, x + 30, y + 20], fill=(255, 240, 170))
    draw.rectangle([x + 10, y + 10, x + w - 60, y + h - 6], fill=(240, 240, 235),
                   outline=(150, 150, 150))
    draw.rectangle([x + 10, y + 10, x + w - 60, y + 20], fill=(0, 120, 90))
    f = sans_b(8)
    draw.text((x + 34, y + 12), "EXITO", font=f, fill=WHITE)
    # open shutters: doors wide, glass visible
    draw.rectangle([x + 20, y + 28, x + 58, y + h - 8], fill=(170, 215, 235),
                   outline=NAVY)
    draw.rectangle([x + 66, y + 28, x + 104, y + h - 8], fill=(170, 215, 235),
                   outline=NAVY)
    # figures walking out the door, below the sign bar
    for fx in (x + 30, x + 48, x + 76):
        draw.ellipse([fx, y + h - 18, fx + 8, y + h - 10], fill=(60, 40, 30))
        draw.rectangle([fx + 1, y + h - 10, fx + 7, y + h - 2],
                       fill=(40, 80, 160))
    # small armoured vehicle at right
    draw.rectangle([x + w - 52, y + h - 24, x + w - 8, y + h - 8],
                   fill=(70, 90, 70))
    draw.rectangle([x + w - 44, y + h - 32, x + w - 20, y + h - 24],
                   fill=(70, 90, 70))
    for cx in (x + w - 44, x + w - 20):
        draw.ellipse([cx, y + h - 8, cx + 8, y + h], fill=(20, 20, 20))


def scene_fall(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 245, 240))
    pts = [(x + 8, y + 12), (x + 50, y + 16), (x + 90, y + 26),
           (x + 130, y + 22), (x + 170, y + 40), (x + w - 8, y + h - 10)]
    draw.line(pts, fill=(200, 30, 30), width=3)
    for i, (px, py) in enumerate(pts[:-1]):
        draw.rectangle([px - 3, py, px + 3, py + 10], fill=(200, 30, 30))
        draw.rectangle([px - 3, py + 10, px + 3, py + 14], fill=(40, 120, 60))


def scene_fire(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(90, 60, 40))
    draw.polygon([(x, y + h), (x + w / 2, y + 8), (x + w, y + h)],
                 fill=(60, 45, 35))
    for fx in range(8, int(w), 26):
        draw.polygon([(x + fx, y + h - 14), (x + fx + 8, y + h - 34),
                      (x + fx + 16, y + h - 14)], fill=(255, 120, 20))
        draw.polygon([(x + fx + 3, y + h - 14), (x + fx + 8, y + h - 26),
                      (x + fx + 13, y + h - 14)], fill=(255, 220, 60))
    draw.ellipse([x + w - 46, y + 2, x + w - 16, y + 20], fill=(120, 120, 120))
    draw.rectangle([x + 14, y + h - 22, x + 34, y + h - 8], fill=(30, 30, 30))
    draw.polygon([(x + 14, y + h - 22), (x + 24, y + h - 30), (x + 34, y + h - 22)],
                 fill=(30, 30, 30))


def scene_hormuz(draw, x, y, w, h):
    """Card 13: strait at dawn, TWO tankers, smoke/flame on one, mines."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 200, 140))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(90, 120, 150))
    draw.rectangle([x, y + h - 30, x + w, y + h - 22], fill=(200, 170, 130))
    # tanker 1 (left, intact)
    draw.rectangle([x + 8, y + h - 34, x + 88, y + h - 22], fill=(120, 40, 30))
    draw.rectangle([x + 20, y + h - 44, x + 44, y + h - 34], fill=(200, 200, 200))
    draw.rectangle([x + 58, y + h - 40, x + 76, y + h - 34], fill=(240, 240, 240))
    # tanker 2 (right, smoke + flame)
    draw.rectangle([x + 104, y + h - 34, x + w - 8, y + h - 22],
                   fill=(90, 30, 25))
    draw.rectangle([x + 118, y + h - 44, x + 140, y + h - 34],
                   fill=(200, 200, 200))
    draw.polygon([(x + 150, y + h - 34), (x + 158, y + h - 48),
                  (x + 166, y + h - 34)], fill=(255, 170, 30))
    draw.polygon([(x + 154, y + h - 34), (x + 158, y + h - 44),
                  (x + 162, y + h - 34)], fill=(255, 230, 120))
    draw.ellipse([x + 148, y + h - 40, x + 170, y + h - 24], fill=(90, 90, 90))
    draw.ellipse([x + 160, y + h - 46, x + 180, y + h - 32], fill=(120, 120, 120))
    # small dark mine shapes in the water
    for mx, my in ((x + 96, y + h - 12), (x + 190, y + h - 10)):
        draw.ellipse([mx, my, mx + 7, my + 7], fill=(20, 20, 20))
        for dx, dy in ((-3, 0), (7, 0), (0, -3), (0, 7)):
            draw.line([mx + 3 + dx, my + 3 + dy, mx + 3, my + 3],
                      fill=(20, 20, 20), width=1)


# ---------------------------------------------------------------- cards
HEROES = [
    dict(n=1, place="DR CONGO · HEALTH", label="5,678", scene="clinic",
         head="WHO pulls Ebola teams out of Congo hospital",
         deck="Sheltered three days in Akwe, Ituri, before evacuation; "
              "the outbreak has killed 5,678 people.",
         src="WHO · Reuters", chip="CONFIRMED"),
    dict(n=2, place="JIUQUAN, CHINA · ASIA · SPACE", label="24", scene="rocket",
         head="Shenzhou-24 lifts off with a Pakistani pilot aboard",
         deck="Lift-off 00:18 UTC with Tang Hongbo, Wu Li and Zeeshan Ali, "
              "40 — first foreign astronaut on China's station; "
              "docked ~3.5h later.",
         src="Xinhua · CMSA · 00:18 UTC", chip="CONFIRMED"),
    dict(n=3, place="DOHA, QATAR · SPORT", label="204", scene="cricket",
         head="15-year-old smashes 204 off 53 balls",
         deck="Vaibhav Sooryavanshi's fastest List A double hundred ever "
              "powers India A past the UAE.",
         src="BBC · The Hindu", chip="CONFIRMED"),
]

SECONDARY = [
    dict(n=4, place="BROOKLYN, USA · NORTH AMERICA", label="10/12",
         scene="court",
         head="Huawei guilty on 10 of 12 counts, and it will appeal",
         deck="11-week trial ends: bank fraud, sanctions violations, "
              "trade-secret theft.",
         src="DOJ · Bloomberg · BBC", chip="CONFIRMED"),
    dict(n=5, place="MOSCOW · EUROPE", label="≈500,000", scene="moscow",
         head="Russia's own figures show nearly 500,000 war dead",
         deck="Leaked state data shows the invasion's mortality toll; "
              "Putin vows retaliation.",
         src="Mediazona · Reuters", chip="REPORTED"),
    dict(n=6, place="HONIARA · OCEANIA", label="A$740m", scene="pact",
         head="Australia signs Solomon Islands security pact",
         deck="Signed in Honiara Wednesday, displacing the islands' "
              "earlier deal with China.",
         src="ABC · Reuters · BBC", chip="CONFIRMED"),
    dict(n=7, place="HODEIDAH, YEMEN · MIDDLE EAST", label="PORT",
         scene="port",
         head="Saudi-led strikes hit Hodeidah port",
         deck="Raids early Wednesday; Houthis also claim a hit on the "
              "Ras Tanura refinery.",
         src="Arab News · Reuters", chip="CONFIRMED"),
    dict(n=8, place="WASHINGTON, USA · NORTH AMERICA", label="UP TO 20%",
         scene="tariff",
         head="US readies Section 301 tariffs on 16 trading partners",
         deck="Levies of up to 20% on China, 15% or less on the EU, "
              "Japan, South Korea, India.",
         src="Reuters · AP", chip="REPORTED"),
    dict(n=9, place="GAZA CITY · MIDDLE EAST", label="≥4", scene="gaza",
         head="Gaza City strike kills at least four",
         deck="Israeli strike hits al-Shati camp apartment block; outlets "
              "say four dead.",
         src="Al Jazeera · Mehr", chip="CONFIRMED"),
    dict(n=10, place="CARTAGENA · SOUTH AMERICA", label="FREED",
         scene="market",
         head="Cartagena hostages freed in dawn raid",
         deck="Dawn raid frees the remaining hostages; one captor killed "
              "at the Éxito store.",
         src="AP · El Tiempo", chip="CONFIRMED"),
    dict(n=11, place="SEOUL / TOKYO · ASIA-PACIFIC", label="-15%",
         scene="fall",
         head="Asia's AI stocks plunge again",
         deck="Kospi sinks about 8% and SoftBank falls 15%; Nikkei down 2.7%.",
         src="CNBC · Al Jazeera", chip="CONFIRMED"),
    dict(n=12, place="FLINDERS ISLAND, TASMANIA · OCEANIA", label="3,000 ha",
         scene="fire",
         head="Bushfire emergency: 'too late to leave'",
         deck="Mount Tanner, Killiecrankie and Leeka; 3,000 ha burning.",
         src="Tas Fire Service", chip="OFFICIAL"),
    dict(n=13, place="STRAIT OF HORMUZ · MIDDLE EAST", label="2 TANKERS",
         scene="hormuz",
         head="Two tankers hit by mines in the Strait of Hormuz",
         deck="IRGC: two tankers struck naval mines and caught fire on "
              "an unauthorised route.",
         src="IRGC · Reuters", chip="REPORTED"),
]

SCENES = {"clinic": scene_clinic, "rocket": scene_rocket,
          "cricket": scene_cricket, "court": scene_court,
          "moscow": scene_moscow, "pact": scene_pact,
          "port": scene_port, "gaza": scene_gaza,
          "market": scene_market, "fall": scene_fall,
          "fire": scene_fire, "hormuz": scene_hormuz}


def draw_scene(draw, kind, x, y, w, h, label):
    if kind == "tariff":
        # label panel at TOP, bars below — label never covers a bar
        draw.rectangle([x, y, x + w, y + h], fill=(245, 245, 245))
        lf = sans_b(12)
        draw.text((x + 30, y + 2), label, font=lf, fill=NAVY)
        tf = sans_b(8)
        draw.text((x + w - 4 - tw(draw, "16 PARTNERS", tf), y + 3),
                  "16 PARTNERS", font=tf, fill=RED)
        scene_chart(draw, x, y + 16, w, h - 16,
                    [("CN", 20), ("EU", 15), ("JP", 15), ("IN", 15)])
        return
    SCENES[kind](draw, x, y, w, h)
    if kind == "rocket":
        return  # "24" already painted on the rocket body, centred
    if kind == "cricket":
        return  # "204 OFF 53" already on the scoreboard
    if kind == "clinic":
        scene_label(draw, (x + w - 96, y + 4, 88, 26), label, size=17,
                    color=NAVY, bg=(255, 255, 255))
        return
    if kind == "market":
        scene_label(draw, (x + w - 78, y + 2, 72, 18), label, size=12,
                    color=WHITE, bg=(0, 120, 90))
        return
    if kind == "hormuz":
        scene_label(draw, (x + 8, y + 2, 108, 20), label, size=12,
                    color=WHITE, bg=(20, 20, 20))
        return
    # generic centred label
    sz = 16 if len(label) <= 5 else 13
    scene_label(draw, (x, y + 2, w, 22), label, size=sz)


def draw_hero(draw, c, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=GREY_L, width=1)
    sh = 128
    draw_scene(draw, c["scene"], x + 1, y + 1, w - 2, sh, c["label"])
    badge(draw, x + 6, y + 6, c["n"])
    ty = y + sh + 6
    f = sans_b(9)
    # kicker, shrink to fit
    ks = 9
    while tw(draw, c["place"], sans_b(ks)) > w - 10 and ks > 7:
        ks -= 1
    draw.text((x + 6, ty), c["place"], font=sans_b(ks), fill=RED)
    ty += 14
    hs = fit_size(SERIF_B, c["head"], 19, w - 12, 14, draw)
    hf = serif_b(hs)
    lines = wrap(draw, c["head"], hf, w - 12)[:2]
    for ln in lines:
        draw.text((x + 6, ty), ln, font=hf, fill=NAVY)
        ty += hs + 2
    df = sans(11)
    for ln in wrap(draw, c["deck"], df, w - 12)[:3]:
        draw.text((x + 6, ty), ln, font=df, fill=BLACK)
        ty += 14
    sf = sans(9)
    draw.text((x + 6, y + h - 18), c["src"], font=sf, fill=GREY)
    cw = chip(draw, x + w - 82, y + h - 19, c["chip"])
    return y + h


def draw_secondary(draw, c, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=GREY_L, width=1)
    sh = 46
    draw_scene(draw, c["scene"], x + 1, y + 1, w - 2, sh, c["label"])
    badge(draw, x + 4, y + 4, c["n"])
    ty = y + sh + 4
    ks = 8
    while tw(draw, c["place"], sans_b(ks)) > w - 8 and ks > 6:
        ks -= 1
    draw.text((x + 5, ty), c["place"], font=sans_b(ks), fill=RED)
    ty += 11
    hs = fit_size(SERIF_B, c["head"], 12, w - 10, 10, draw)
    hf = serif_b(hs)
    for ln in wrap(draw, c["head"], hf, w - 10)[:2]:
        draw.text((x + 5, ty), ln, font=hf, fill=NAVY)
        ty += hs + 1
    df = sans(8)
    for ln in wrap(draw, c["deck"], df, w - 10)[:2]:
        draw.text((x + 5, ty), ln, font=df, fill=BLACK)
        ty += 10
    sf = sans(8)
    draw.text((x + 5, y + h - 15), c["src"], font=sf, fill=GREY)
    chip(draw, x + w - 74, y + h - 16, c["chip"])
    return y + h


# ---------------------------------------------------------------- briefs + map
BRIEFS = [
    (14, "FORECAST", "Thanksgiving-eve data pile: GDP, PCE, claims"),
    (15, "FORECAST", "October CPI due"),
    (16, "REPORTED", "Sudan drone strikes kill 19 civilians"),
    (17, "REPORTED", "Houthis 60 km from Aden"),
    (18, "CONFIRMED", "Russian strike kills two in Odesa, hits Kyiv"),
    (19, "REPORTED", "CIA, ODNI cyber breach"),
    (20, "SCHEDULED", "EU-Balkans summit opens"),
    (21, "REPORTED", "US-led group buys Lukoil overseas assets"),
    (22, "OFFICIAL", "47,000 women killed in 2023"),
    (23, "REPORTED", "Cairo tanker fire kills at least 31"),
    (24, "REPORTED", "Macy's parade postponed, first time in 100 years"),
    (25, "SCHEDULED", "Fed Beige Book at 19:00 UTC"),
    (26, "SPORT", "UCL Matchday 5: PSG v Roma"),
    (27, "REPORTED", "Trump may weigh NATO-like Kyiv deal"),
    (28, "REPORTED", "EU announces new Russia sanctions"),
    (29, "REPORTED", "Kyiv hit a Russian ship in the Gulf of Finland"),
    (30, "MKT", "Dell record Q3: $54.9bn revenue, AI servers $22bn"),
    (31, "REPORTED", "Bogor mine flood kills six, 20 trapped"),
    (32, "REPORTED", "China probes Politburo member Chen"),
    (33, "REPORTED", "Israeli strike kills Hamas security chief"),
    (34, "REPORTED", "NATO vows space defence vs Russia"),
    (35, "MKT", "Dow closes above 50,000 for the first time"),
    (36, "OFFICIAL", "US to host Copa America again in 2028"),
    (37, "SPORT", "Real Madrid rout PSG 5-1 in UCL"),
    (38, "REPORTED", "Malaysia to return 6,300 Rohingya"),
    (39, "REPORTED", "North Koreans jailed for being Christian, defectors say"),
]

PIN_LONLAT = {
    1: (23, -2), 2: (100, 40), 3: (51, 25), 4: (-74, 40), 5: (37, 55),
    6: (160, -9), 7: (43, 15), 8: (-77, 39), 9: (34, 31), 10: (-75, 10),
    11: (127, 37), 12: (148, -40), 13: (56, 26), 14: (-100, 39),
    15: (-98, 38), 16: (30, 13), 17: (45, 13), 18: (30, 46),
    19: (-77, 38), 20: (21, 42), 21: (44, 57), 22: (20, 10),
    23: (31, 30), 24: (-74, 40), 25: (-77, 39), 26: (2, 48),
    27: (30, 50), 28: (4, 50), 29: (24, 60), 30: (-97, 30),
    31: (107, -6), 32: (116, 40), 33: (34, 31), 34: (4, 50),
    35: (-74, 40), 36: (-100, 39), 37: (-3, 40), 38: (102, 3),
    39: (125, 39),
}
# display nudges (dx, dy px) to keep crowded clusters readable
PIN_NUDGE = {
    4: (-14, -10), 24: (0, 12), 35: (14, -8), 8: (-12, 8), 19: (12, -10),
    25: (0, -14), 30: (-10, -8), 14: (-8, 10), 15: (10, 8), 36: (14, 10),
    9: (-14, -10), 33: (12, 10), 23: (-16, 8), 13: (16, -8), 7: (-10, 10),
    17: (14, -8), 16: (-18, -6), 22: (0, 10), 3: (0, -10),
    26: (-16, -8), 28: (-6, -12), 34: (6, 10), 20: (14, 8), 18: (-14, 8),
    27: (10, -10), 5: (-8, -12), 21: (16, -6), 29: (0, -14),
    2: (-10, -8), 32: (0, -12), 39: (12, 8), 11: (-12, 10),
    31: (8, 8), 38: (-10, -6), 37: (12, 8), 10: (-14, 8),
}

CONTINENTS = [
    [(15, 12), (110, 6), (145, 20), (135, 38), (105, 48), (85, 62),
     (55, 58), (30, 44), (12, 30)],
    [(105, 62), (145, 62), (160, 80), (145, 98), (120, 95), (105, 80)],
    [(295, 12), (345, 8), (365, 20), (345, 34), (315, 38), (295, 28)],
    [(295, 48), (345, 44), (365, 58), (355, 84), (330, 94), (300, 76),
     (290, 62)],
    [(365, 8), (510, 4), (590, 16), (610, 38), (570, 52), (510, 48),
     (470, 62), (420, 52), (390, 38), (368, 24)],
    [(530, 76), (570, 72), (590, 84), (560, 94), (535, 88)],
]


def draw_map(draw, x, y, w, h):
    for gy in range(2, h - 2, 5):
        for gx in range(2, w - 2, 5):
            px = gx / w * 660.0
            py = gy / h * 100.0
            if any(point_in_poly(px, py, c) for c in CONTINENTS):
                draw.ellipse([x + gx - 1, y + gy - 1, x + gx + 1, y + gy + 1],
                             fill=BEIGE)
    for n in range(1, 40):
        lon, lat = PIN_LONLAT[n]
        px = x + (lon + 180) / 360.0 * w
        py = y + (90 - lat) / 180.0 * h
        dx, dy = PIN_NUDGE.get(n, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            draw.line([px, py, qx, qy], fill=(150, 40, 40), width=1)
        r = 5
        draw.ellipse([qx - r, qy - r, qx + r, qy + r], fill=RED,
                     outline=WHITE, width=1)
        s = str(n)
        f = sans_b(6)
        draw.text((qx - tw(draw, s, f) / 2, qy - 4), s, font=f, fill=WHITE)


def render():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    y = 0
    # 1. kicker bar
    d.rectangle([0, y, W, y + 20], fill=BLACK)
    d.text((12, y + 4), "THE WORLD IN ONE DAY", font=sans_b(11), fill=WHITE)
    r = "39 STORIES · 7 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - 12 - tw(d, r, sans_b(10)), y + 5), r, font=sans_b(10),
           fill=WHITE)
    y += 20
    # 2. masthead
    mf = serif_b(46)
    t = "Wednesday 25 November 2026"
    d.text(((W - tw(d, t, mf)) / 2, y + 4), t, font=mf, fill=NAVY)
    y += 56
    # 3. red subhead
    sub = ("Ebola teams out of Congo · Boy of 15 hits 204 off 53 · "
           "Shenzhou-24 lifts off with a Pakistani pilot")
    sf = sans_b(15)
    while tw(d, sub, sf) > W - 24:
        sf = sans_b(sf.size - 1)
    d.text(((W - tw(d, sub, sf)) / 2, y + 2), sub, font=sf, fill=RED)
    y += 22
    # 4. stat strip
    stats = [("5,678", "EBOLA DEAD, CONGO"), ("204", "RUNS OFF 53 BALLS, AGE 15"),
             ("10/12", "HUAWEI COUNTS GUILTY"),
             ("≈500,000", "RUSSIANS KILLED (LEAKED)"), ("-15%", "SOFTBANK SHARES"),
             ("A$740m", "SOLOMONS PACT")]
    sy = y
    d.rectangle([0, sy, W, sy + 56], fill=WHITE)
    d.line([0, sy, W, sy], fill=GREY_L, width=1)
    d.line([0, sy + 56, W, sy + 56], fill=GREY_L, width=1)
    cw = W / 6
    for i, (num, lab) in enumerate(stats):
        cx = i * cw
        if i:
            d.line([cx, sy + 8, cx, sy + 48], fill=GREY_L, width=1)
        nf = sans_b(26)
        while tw(d, num, nf) > cw - 16:
            nf = sans_b(nf.size - 1)
        d.text((cx + (cw - tw(d, num, nf)) / 2, sy + 4), num, font=nf,
               fill=NAVY)
        lf = sans_b(9)
        while tw(d, lab, lf) > cw - 10:
            lf = sans_b(lf.size - 1)
        d.text((cx + (cw - tw(d, lab, lf)) / 2, sy + 36), lab, font=lf,
               fill=RED)
    y += 56
    # 5. UTC ruler
    ruler = [("00:18", "SHENZHOU LIFTS OFF"), ("02:46", "HODEIDAH STRIKES"),
             ("07:00", "GERMANY GDP FINAL"), ("13:30", "US DATA PILE"),
             ("17:20", "HUAWEI 10/12 VERDICT"), ("19:00", "BEIGE BOOK"),
             ("20:00", "UCL NIGHT")]
    ry = y
    d.rectangle([0, ry, W, ry + 24], fill=(238, 238, 236))
    d.line([12, ry + 12, W - 12, ry + 12], fill=GREY, width=1)
    for i, (tm, lab) in enumerate(ruler):
        tx = 14 + i * (W - 28) / 6
        d.ellipse([tx - 2, ry + 10, tx + 2, ry + 14], fill=RED)
        tf = sans_b(8)
        d.text((tx - tw(d, tm, tf) / 2, ry + 1), tm, font=tf, fill=NAVY)
        lf = sans(7)
        lx = max(2, min(W - 2 - tw(d, lab, lf), tx - tw(d, lab, lf) / 2))
        d.text((lx, ry + 14), lab, font=lf, fill=GREY)
    y += 24
    # 6. heroes
    hy = y + 4
    hw = (W - 24 - 12) / 3
    hh = 268
    for i, c in enumerate(HEROES):
        draw_hero(d, c, 12 + i * (hw + 6), hy, hw, hh)
    y = hy + hh + 4
    # 7. secondary, two rows of five
    sw = (W - 24 - 24) / 5
    sh = 124
    for row in range(2):
        for i in range(5):
            c = SECONDARY[row * 5 + i]
            draw_secondary(d, c, 12 + i * (sw + 6), y + row * (sh + 4), sw, sh)
    y += 2 * sh + 4 + 4
    # 8. navy bar
    d.rectangle([0, y, W, y + 22], fill=NAVY)
    d.text((12, y + 5), "ALSO TODAY — 26 MORE STORIES", font=sans_b(11),
           fill=WHITE)
    rr = "14–39 · NUMBERED · PINNED ON THE MAP BELOW"
    d.text((W - 12 - tw(d, rr, sans_b(10)), y + 6), rr, font=sans_b(10),
           fill=WHITE)
    y += 22
    # 9. brief list, 3 columns x 9 rows
    by = y + 4
    colw = (W - 24 - 20) / 3
    for idx, (n, tag, text) in enumerate(BRIEFS):
        col, row = idx // 9, idx % 9
        bx = 12 + col * (colw + 10)
        ly = by + row * 14
        nf = sans_b(9)
        d.text((bx, ly), str(n), font=nf, fill=NAVY)
        nx = bx + 18
        # tag pill: chip() draws with sans_b(8) and width tw+10 — match it
        tf = sans_b(8)
        tagw = int(tw(d, tag, tf)) + 10
        # shrink text font until the whole line fits inside the column
        size = 9
        while size > 7:
            sf2 = sans(size)
            if (18 + tagw + 6 + tw(d, text, sf2)) <= colw:
                break
            size -= 1
        sf2 = sans(size)
        chip(d, nx, ly, tag)
        d.text((nx + tagw + 6, ly + 1), text, font=sf2, fill=BLACK)
    y = by + 9 * 14 + 4
    # 10. bottom band: map + DATE CHECK
    band_y = y
    band_h = 130
    map_w = 656
    draw_map(d, 12, band_y + 4, map_w, band_h - 22)
    leg = "WHERE IT HAPPENED · PINS = STORY NUMBERS"
    d.text((12, band_y + band_h - 16), leg, font=sans_b(8), fill=NAVY)
    regions = [("Americas", (30, 90, 160)), ("Europe", (110, 60, 150)),
               ("Asia-Pacific", (0, 120, 115)), ("Middle East", (200, 100, 0)),
               ("Oceania", (31, 122, 60)), ("Africa", (120, 80, 40)),
               ("Global", (120, 120, 120))]
    lx = 12
    ly2 = band_y + band_h - 6
    for name, col in regions:
        d.ellipse([lx, ly2, lx + 6, ly2 + 6], fill=col)
        f2 = sans(7)
        d.text((lx + 8, ly2 - 1), name, font=f2, fill=GREY)
        lx += 8 + int(tw(d, name, f2)) + 8
    # DATE CHECK box
    bx0, bx1 = 684, W - 12
    d.rectangle([bx0, band_y + 4, bx1, band_y + band_h - 4], fill=WHITE,
                outline=RED, width=2)
    d.text((bx0 + 10, band_y + 8), "DATE CHECK · NOT WEDNESDAY",
           font=sans_b(11), fill=RED)
    d.text((bx0 + 10, band_y + 26),
           "Left out on purpose — these happened on other days:",
           font=sans(9), fill=BLACK)
    excl = ["GTA 6 — 19 Nov", "COP31 failure — 23 Nov",
            "DR Congo vote — 22 Nov", "Midterm vote — 4 Nov",
            "Man Utd 3-2 Roma comeback — 3 Nov",
            "Nepal PM ends India visit — 22–23 Nov"]
    ey = band_y + 40
    for e in excl:
        d.text((bx0 + 10, ey), "✕  " + e, font=sans(9), fill=RED_D)
        ey += 11
    d.text((bx0 + 10, ey + 2), "Every story above is dated 25 Nov 2026.",
           font=sans_b(9), fill=NAVY)
    y = band_y + band_h
    # 11. footer
    d.text((12, y + 2),
           "Sources: WHO, Xinhua, CMSA, Tas Fire Service, IRGC, Reuters, UN, "
           "ABC, Al Jazeera, Mediazona, CNBC, BBC, Guardian, AP — checked vs "
           "reports dated 25 Nov 2026. 39 stories; 7 regions.",
           font=sans(9), fill=GREY)
    d.text((12, y + 14),
           "Drawn by an AI agent for make.fun · Wednesday 25 November 2026 · "
           "One page, one day",
           font=sans(9), fill=GREY)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    render()
