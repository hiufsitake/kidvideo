"""Big and Small — opposites: elephant/mouse, whale/fish, bear/bunny."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s06"; SLUG = "big-and-small-short06"
BIG, SMALL = 540, 200
BX, SXP, FEET = 340, 785, 1400          # big spans x 70..610, small 685..885
T_HOOK, STEP, T_SMALL = 1.7, 3.8, 1.8   # pairs at 1.7, 5.5, 9.3; small one arrives 1.8s in
T_END = T_HOOK + 3 * STEP               # 13.1

def poly(d, pts, fill, w=10): d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=OL, width=w * SS)
def curve(d, pts, col, w):
    flat = [c * SS for p in pts for c in p]
    d.line(flat, fill=OL, width=(w + 14) * SS, joint="curve"); d.line(flat, fill=col, width=w * SS, joint="curve")

# ---------- characters (900px canvas, feet at y~860) ----------
def elephant(closed=False):
    im, d = canvas(); G, G2, P = (150, 165, 205, 255), (125, 140, 185, 255), (255, 170, 190, 255)
    curve(d, [(700, 560), (770, 600), (790, 680)], G, 16)
    for x in (300, 400, 500, 600): E(d, (x - 55, 620, x + 55, 865), G); d.arc(S((x - 40, 830, x + 40, 875)), 200, 340, fill=OL, width=6 * SS)
    E(d, (190, 420, 730, 790), G)
    for sx in (-1, 1): E(d, (450 + sx * 215 - 150, 120, 450 + sx * 215 + 150, 470), G2); E(d, (450 + sx * 215 - 100, 170, 450 + sx * 215 + 100, 420), P, 0)
    E(d, (260, 90, 640, 470), G)
    curve(d, [(450, 380), (450, 500), (440, 600), (480, 660), (530, 640)], G, 70)
    eyes(d, 450, 270, 85, 42, closed); cheeks(d, 450, 360, 140)
    for sx in (-1, 1): poly(d, [(450 + sx * 55, 420), (450 + sx * 110, 470), (450 + sx * 70, 480)], (255, 255, 245, 255), 6)  # tusks
    return im

def mouse(closed=False):
    im, d = canvas(); G, P = (175, 170, 185, 255), (255, 170, 190, 255)
    curve(d, [(650, 760), (760, 740), (800, 640), (760, 580)], P, 12)
    for x in (360, 540): E(d, (x - 50, 790, x + 50, 865), P)
    E(d, (230, 470, 670, 840), G); E(d, (340, 560, 560, 820), (225, 220, 230, 255), 0)
    for sx in (-1, 1): E(d, (450 + sx * 190 - 140, 60, 450 + sx * 190 + 140, 340), G); E(d, (450 + sx * 190 - 90, 110, 450 + sx * 190 + 90, 290), P, 0)
    E(d, (250, 180, 650, 540), G)
    eyes(d, 450, 330, 85, 46, closed); cheeks(d, 450, 430, 140)
    E(d, (420, 400, 480, 450), (255, 110, 140, 255), 7); smile(d, 450, 470, 35, 7)
    for sx in (-1, 1):
        for dy in (-12, 14): d.line(S((450 + sx * 50, 430 + dy * .3, 450 + sx * 190, 420 + dy)), fill=OL, width=5 * SS)
    return im

def whale(closed=False):
    im, d = canvas(); B, B2 = (70, 140, 235, 255), (190, 225, 255, 255)
    poly(d, [(700, 520), (850, 380), (880, 470), (820, 560), (880, 650), (850, 720)], B)
    E(d, (60, 300, 780, 760), B)
    d.chord(S((120, 480, 720, 760)), 0, 180, fill=B2, outline=OL, width=10 * SS)
    for x in range(220, 640, 70): d.line(S((x, 640, x + 10, 735)), fill=(150, 195, 240, 255), width=7 * SS)
    for dx in (-40, 0, 40): curve(d, [(330, 300), (330 + dx * .6, 230), (330 + dx * 1.6, 170)], (150, 215, 255, 255), 14)
    eyes(d, 300, 450, 85, 44, closed); cheeks(d, 300, 545, 135)
    smile(d, 300, 560, 70, 10)
    return im

def fish(closed=False):
    im, d = canvas(); Y, Pu = (255, 210, 60, 255), (190, 120, 255, 255)
    poly(d, [(640, 450), (840, 300), (840, 600)], Pu)
    poly(d, [(380, 250), (520, 180), (560, 300)], Pu, 8)
    E(d, (120, 230, 700, 670), Y)
    for x in (420, 520): d.arc(S((x - 70, 260, x + 70, 640)), 290, 70, fill=(255, 160, 40, 255), width=22 * SS)
    eyes(d, 300, 420, 70, 46, closed); cheeks(d, 300, 520, 110)
    E(d, (180, 520, 250, 575), (255, 120, 140, 255), 7)
    return im

def bear(closed=False):
    im, d = canvas(); Br, Br2 = (175, 115, 70, 255), (235, 200, 160, 255)
    for x in (330, 570): E(d, (x - 80, 720, x + 80, 868), Br); E(d, (x - 45, 790, x + 45, 855), Br2, 0)
    E(d, (200, 440, 700, 830), Br); E(d, (320, 540, 580, 800), Br2, 0)
    for sx in (-1, 1): E(d, (450 + sx * 215 - 65, 470, 450 + sx * 215 + 65, 670), Br)
    for sx in (-1, 1): E(d, (450 + sx * 165 - 75, 60, 450 + sx * 165 + 75, 210), Br); E(d, (450 + sx * 165 - 40, 95, 450 + sx * 165 + 40, 175), Br2, 0)
    E(d, (240, 90, 660, 490), Br)
    eyes(d, 450, 260, 90, 44, closed); cheeks(d, 450, 360, 150)
    E(d, (360, 310, 540, 450), Br2); E(d, (415, 320, 485, 370), (60, 40, 35, 255), 0); smile(d, 450, 390, 35, 8)
    return im

def bunny(closed=False):
    im, d = canvas(); Wt, P = (250, 248, 252, 255), (255, 170, 195, 255)
    E(d, (640, 640, 740, 740), Wt)
    for x in (360, 540): E(d, (x - 70, 790, x + 70, 868), Wt)
    E(d, (240, 520, 660, 850), Wt)
    for sx in (-1, 1):
        cx = 450 + sx * 85
        E(d, (cx - 60, 0, cx + 60, 330), Wt); E(d, (cx - 30, 40, cx + 30, 290), P, 0)
    E(d, (250, 230, 650, 590), Wt)
    eyes(d, 450, 380, 85, 46, closed); cheeks(d, 450, 480, 140)
    E(d, (425, 455, 475, 495), (255, 120, 150, 255), 6)
    d.line(S((450, 495, 450, 520)), fill=OL, width=6 * SS); smile(d, 450, 525, 35, 7)
    return im

def pair(fn, size): o = finish(fn(False), size); return o, finish(fn(True), size)

# ---------- backgrounds ----------
def savanna():
    img = vgrad((255, 200, 110), (255, 238, 180)); d = ImageDraw.Draw(img, "RGBA")
    for r, a in [(220, 50), (160, 90), (115, 255)]: d.ellipse((860 - r, 280 - r, 860 + r, 280 + r), fill=(255, 240, 140, a))
    for x, s in [(110, 1.0), (980, 0.8)]:
        d.rectangle((x - 16 * s, 900, x + 16 * s, 1250), fill=(140, 90, 55))
        d.ellipse((x - 170 * s, 820 - 40 * s, x + 170 * s, 900 + 20 * s), fill=(110, 170, 70))
    d.ellipse((-300, 1150, 1400, 1550), fill=(200, 205, 90))
    d.rectangle((0, 1350, W, H), fill=(185, 190, 80))
    for x in range(0, W, 55): d.polygon([(x, 1360), (x + 18, 1310), (x + 36, 1360)], fill=(165, 175, 65))
    return img

def sea():
    img = vgrad((70, 190, 245), (20, 90, 190)); d = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(7)
    for _ in range(30):
        x, y, r = rng.integers(0, W), rng.integers(100, 1400), rng.integers(8, 28)
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255, 150), width=4)
        d.ellipse((x - r * .5, y - r * .6, x - r * .1, y - r * .2), fill=(255, 255, 255, 150))
    d.ellipse((-300, 1380, 1400, 1700), fill=(245, 215, 150)); d.rectangle((0, 1500, W, H), fill=(245, 215, 150))
    for x, h, c in [(60, 300, (60, 190, 110)), (1000, 380, (80, 210, 120)), (930, 240, (60, 180, 100))]:
        d.line([(x + 25 * math.sin(y / 50), 1500 - y) for y in range(0, h, 10)], fill=c, width=28)
    for x, y in [(180, 1520), (850, 1560)]: d.ellipse((x - 40, y - 20, x + 40, y + 20), fill=(255, 150, 170))
    return img

def forest():
    img = vgrad((170, 230, 255), (220, 248, 220)); d = ImageDraw.Draw(img, "RGBA")
    for cx, cy, s in [(200, 280, 0.9), (780, 420, 0.7)]:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 220))
    for x, s, c in [(70, 1.0, (60, 160, 80)), (1010, 1.1, (50, 150, 75)), (960, 0.7, (80, 180, 90))]:
        d.rectangle((x - 22 * s, 1050, x + 22 * s, 1360), fill=(130, 85, 50))
        for k in range(3): d.polygon([(x - (170 - k * 35) * s, (1100 - k * 150) * 1), (x + (170 - k * 35) * s, 1100 - k * 150), (x, (850 - k * 150))], fill=c)
    d.ellipse((-300, 1200, 1400, 1550), fill=(120, 200, 90)); d.rectangle((0, 1360, W, H), fill=(105, 185, 80))
    for x, y in [(120, 1560), (900, 1620), (500, 1700)]:
        d.rectangle((x - 12, y - 10, x + 12, y + 30), fill=(250, 240, 220)); d.chord((x - 45, y - 50, x + 45, y + 20), 180, 360, fill=(240, 80, 80))
        d.ellipse((x - 20, y - 35, x - 4, y - 19), fill=(255, 255, 255))
    return img

SC = [  # bg, big sprites, small sprites, big name, small name, float (water)?
    (savanna(), pair(elephant, BIG), pair(mouse, SMALL), "ELEPHANT", "MOUSE", False),
    (sea(), pair(whale, BIG + 40), pair(fish, SMALL), "WHALE", "FISH", True),
    (forest(), pair(bear, BIG), pair(bunny, SMALL), "BEAR", "BUNNY", False),
]
BIGW = word_layers("BIG!", 250, (255, 230, 70)); SMALLW = word_layers("small!", 110, (255, 255, 255), stroke=(230, 60, 120))
BN = [word_layers(s[3], 100, (255, 255, 255)) for s in SC]; SN = [word_layers(s[4], 100, (255, 255, 255)) for s in SC]
hook_bg = vgrad((140, 210, 255), (255, 220, 240))
H1 = word_layers("BIG", 260, (255, 230, 70)); H2 = word_layers("or", 90, (255, 255, 255)); H3 = word_layers("small?", 110, (255, 255, 255), stroke=(230, 60, 120))
hook_big = SC[0][1][0].resize((430, 430), Image.LANCZOS); hook_sm = SC[0][2][0].resize((170, 170), Image.LANCZOS)
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("BIG AND SMALL!", 120, (255, 255, 255))

def rays(base, t, cy=1000, col=(255, 255, 255, 55)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, cy), (CX + 2200 * math.cos(a0), cy + 2200 * math.sin(a0)), (CX + 2200 * math.cos(a0 + .22), cy + 2200 * math.sin(a0 + .22))], fill=col)

def hook(t):
    base = hook_bg.copy(); rays(base, t)
    sq = 1 + 0.05 * math.sin(t * 7)
    ground_shadow(base, 330, 1380, 320, 55); ground_shadow(base, 770, 1380, 130, 55)
    paste_scaled(base, hook_big, 330, 1400, 1, 2 * math.sin(t * 5), 1 / sq, sq, True)
    hop = -60 * abs(math.sin(t * 6))
    paste_scaled(base, hook_sm, 770, 1400 + hop, 1, 6 * math.sin(t * 6), 1, 1, True)
    draw_words(base, H1, CX, 430, t + 0.3); draw_words(base, H2, CX, 620, t - 0.15); draw_words(base, H3, CX, 740, t - 0.35)
    return base

def scene(i, lt):
    bg, (bo, bc), (so, sc), _bn, _sn, water = SC[i]
    base = bg.copy(); d = ImageDraw.Draw(base)
    bob = 14 * math.sin(lt * 3) if water else 0
    by = 1300 if water else FEET  # whale floats a little higher
    yo, sx, sy = drop_land(lt, 0.35, 950)
    if not water: ground_shadow(base, BX, FEET - 22, BIG * .75 * (0.5 + 0.5 * min(1, lt / .35)), 70)
    paste_scaled(base, bc if blinking(lt, i) and lt > 0.8 else bo, BX, by + yo + bob, 1, 0 if not water else 2 * math.sin(lt * 2), sx, sy, True)
    if 0.35 <= lt < 0.75: burst(d, BX, FEET - 40, lt - 0.35, 8, 300)
    st = lt - T_SMALL
    if st < 0:
        draw_words(base, BIGW, CX, 380, lt - 0.25); draw_words(base, BN[i], CX, 590, lt - 0.45)
        return shake(base, 0.35, lt, 18)
    # small one pops in with a cheeky hop
    s = ease_pop(st / 0.35)
    hop = -45 * abs(math.sin(st * 7)) * (1 if st > 0.35 else 0)
    if water: hop = 20 * math.sin(st * 5) - 260
    if not water: ground_shadow(base, SXP, FEET - 10, SMALL * .7 * s, 60)
    paste_scaled(base, sc if blinking(st, i + 3) and st > 0.6 else so, SXP, FEET + hop, s, 6 * math.sin(st * 6), 1, 1, True)
    burst(d, SXP, FEET - 100 + (-260 if water else 0), st, 8, 150)
    draw_words(base, SMALLW, CX, 380, st); draw_words(base, SN[i], CX, 560, st - 0.2)
    return camera(base, zoom_curve(st, 1.06, 0.6), SXP, FEET - 100 + (-260 if water else 0))

def ending(lt, t):
    base = hook_bg.copy(); rays(base, t, 1000, (255, 255, 255, 65)); d = ImageDraw.Draw(base)
    xs = [(340, SC[0][1][0], 460), (770, SC[0][2][0], 170)]
    for k, (x, spr, sz) in enumerate(xs):
        l = lt - k * 0.12
        if l <= 0: continue
        yo, sx, sy = drop_land(l, 0.3, 700)
        hop = -40 * abs(math.sin(lt * 5 + k)) if lt > 0.7 else 0
        ground_shadow(base, x, 1385, sz * .7, 55)
        paste_scaled(base, spr.resize((sz, sz), Image.LANCZOS), x, 1400 + yo + hop, 1, 0, sx, sy, True)
    draw_words(base, end1, CX, 480, lt); draw_words(base, end2, CX, 730, lt - 0.25, 0.1)
    confetti(d, lt - 0.1)
    return base

def raw(t):
    if t < T_HOOK: return hook(t)
    if t >= T_END: return ending(t - T_END, t)
    i = int((t - T_HOOK) // STEP); return scene(i, t - T_HOOK - i * STEP)

def frame(t):
    """Iris transition between scenes (0.22s)."""
    for b in [T_HOOK + k * STEP for k in range(4)]:
        if b <= t < b + 0.22:
            k = (t - b) / 0.22; old, new = raw(b - 0.001), raw(t)
            m = Image.new("L", (W, H), 0); r = 1150 * ease_out(k)
            ImageDraw.Draw(m).ellipse((CX - r, 1000 - r, CX + r, 1000 + r), fill=255)
            old.paste(new, (0, 0), m)
            ImageDraw.Draw(old).ellipse((CX - r, 1000 - r, CX + r, 1000 + r), outline=(255, 255, 255), width=18)
            return old
    return raw(t)

# ---------- audio ----------
def sfx_thud(n=0.35):
    t = np.arange(int(SR * n)) / SR
    return np.sin(2 * np.pi * (140 - 200 * t) * t) * np.exp(-t * 11) * 0.7

def sfx_squeak(n=0.22):
    t = np.arange(int(SR * n)) / SR
    return np.sin(2 * np.pi * (1800 + 1400 * np.sin(t * 40)) * t) * np.exp(-t * 9) * 0.18

mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.08)
for i in range(3):
    st = T_HOOK + i * STEP
    place(mix, sfx_sparkle(), st); place(mix, sfx_thud(), st + 0.35)
    place(mix, load(f"{OUT}/b{i + 1}.wav"), st + 0.25)
    place(mix, sfx_squeak(), st + T_SMALL); place(mix, sfx_pop(), st + T_SMALL + 0.05)
    place(mix, load(f"{OUT}/m{i + 1}.wav"), st + T_SMALL + 0.2)
place(mix, load(f"{OUT}/e.wav"), T_END + 0.1)
place(mix, sfx_ding(), T_END + 0.1); place(mix, sfx_sparkle(), T_END + 0.5)
notes = [60, 64, 67, 72, None, 67, 72, 76, 74, 71, 67, None, 65, 69, 72, 71]
mix += 0.075 * synth_music(notes, 60 / 120 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.8, 1.5, 2.3, 3.0, 4.0, 5.0, 6.2, 7.0, 8.5, 9.9, 11.6, 12.8, 13.3, 14.0, 14.9], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
