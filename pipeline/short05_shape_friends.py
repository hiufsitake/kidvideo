"""Shape Friends — circle, square, triangle, star with faces; corners counted; real-life example for each."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s05"; SLUG = "shape-friends-short05"
SP = 480                 # shape sprite size on screen
SX, SFEET = 320, 1300    # shape centre x, feet line (sprite spans y 820..1300, x 80..560)
OX, OY = 745, 1060       # example object centre (spans ~595..895)
T_HOOK, STEP = 1.5, 2.7  # scenes start at 1.5, 4.2, 6.9, 9.6
T_END = T_HOOK + 4 * STEP  # 12.3
OBJ_AT = 1.05            # when the example object pops (scene-local)

# ---------- shapes (600px canvas, drawn at SS) ----------
def tri_pts(): return [(300, 50), (560, 530), (40, 530)]
def star_pts(cx=300, cy=310, r=275):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * .47
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

def shape(kind, col, closed=False):
    im, d = canvas(600)
    c = col + (255,)
    if kind == "circle": E(d, (50, 50, 550, 550), c, 12); fy = 290
    elif kind == "square": d.rounded_rectangle(S((60, 60, 540, 540)), 30 * SS, fill=c, outline=OL, width=12 * SS); fy = 280
    elif kind == "triangle": d.polygon([(x * SS, y * SS) for x, y in tri_pts()], fill=c, outline=OL, width=12 * SS); fy = 380
    else: d.polygon([(x * SS, y * SS) for x, y in star_pts()], fill=c, outline=OL, width=12 * SS); fy = 320
    gap, r = (62, 34) if kind in ("triangle", "star") else (85, 44)
    eyes(d, 300, fy, gap, r, closed)
    cheeks(d, 300, fy + r + 30, gap + 45 if kind != "star" else 85)
    if kind == "star":
        d.ellipse(S((205, fy + 50, 235, fy + 80)), fill=(255, 120, 150, 140)); smile(d, 300, fy + 70, 32, 8)
    else:
        d.chord(S((300 - 55, fy + 55, 300 + 55, fy + 135)), 0, 180, fill=(120, 30, 40, 255), outline=OL, width=8 * SS)
        d.ellipse(S((280, fy + 100, 320, fy + 130)), fill=(255, 120, 140, 255))
    return im

def corners(kind):
    if kind == "square": return [(60, 60), (540, 60), (540, 540), (60, 540)]
    if kind == "triangle": return tri_pts()
    return []

# ---------- example objects (400px canvas) ----------
def sun():
    im, d = canvas(400)
    for i in range(12):
        a = i * math.pi / 6
        p = [(200 + 120 * math.cos(a - .18), 200 + 120 * math.sin(a - .18)), (200 + 190 * math.cos(a), 200 + 190 * math.sin(a)), (200 + 120 * math.cos(a + .18), 200 + 120 * math.sin(a + .18))]
        d.polygon([(x * SS, y * SS) for x, y in p], fill=(255, 170, 40, 255), outline=OL, width=7 * SS)
    E(d, (75, 75, 325, 325), (255, 220, 60, 255), 9)
    eyes(d, 200, 185, 45, 24); smile(d, 200, 235, 30, 7)
    return im

def present():
    im, d = canvas(400)
    d.rounded_rectangle(S((60, 100, 340, 380)), 14 * SS, fill=(255, 110, 150, 255), outline=OL, width=9 * SS)
    d.rectangle(S((178, 100, 222, 380)), fill=(255, 230, 80, 255), outline=OL, width=6 * SS)
    d.rectangle(S((60, 218, 340, 262)), fill=(255, 230, 80, 255), outline=OL, width=6 * SS)
    for sx in (-1, 1):
        E(d, (200 + sx * 70 - 55, 40, 200 + sx * 70 + 55, 110), (255, 230, 80, 255), 7)
    E(d, (175, 70, 225, 115), (255, 200, 50, 255), 7)
    return im

def party_hat():
    im, d = canvas(400)
    tri = [(200, 50), (340, 360), (60, 360)]
    d.polygon([(x * SS, y * SS) for x, y in tri], fill=(80, 170, 255, 255), outline=OL, width=9 * SS)
    for k, col in enumerate([(255, 230, 80, 255), (255, 120, 160, 255)]):  # stripes clipped to triangle
        y0 = 160 + k * 100; w0 = (y0 - 50) / 310 * 140; w1 = (y0 + 40 - 50) / 310 * 140
        d.polygon([(x * SS, y * SS) for x, y in [(200 - w0, y0), (200 + w0, y0), (200 + w1, y0 + 40), (200 - w1, y0 + 40)]], fill=col)
    d.polygon([(x * SS, y * SS) for x, y in tri], outline=OL, width=9 * SS)
    E(d, (165, 15, 235, 85), (255, 90, 90, 255), 7)
    return im

def twinkles():
    im, d = canvas(400)
    for cx, cy, r in [(200, 190, 120), (80, 330, 55), (330, 70, 50), (330, 320, 40)]:
        d.polygon([(x * SS, y * SS) for x, y in star_pts(cx, cy, r)], fill=(255, 240, 120, 255), outline=OL, width=6 * SS)
    return im

# ---------- backgrounds ----------
def scene_bg(top, bot, floor, night=False):
    img = vgrad(top, bot); d = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(len(str(top)))
    if night:
        for _ in range(60):
            x, y, r = rng.integers(0, W), rng.integers(0, 1300), rng.integers(2, 6)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 230, 200))
        d.ellipse((800, 160, 980, 340), fill=(255, 245, 200)); d.ellipse((850, 140, 1010, 300), fill=top)
    else:  # soft confetti dots + clouds
        for _ in range(26):
            x, y, r = rng.integers(0, W), rng.integers(0, 1350), rng.integers(10, 26)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 70))
        for cx, cy, s in [(150, 250, 0.9), (820, 700, 0.7)]:
            for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
                d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 200))
    d.rectangle((0, 1330, W, H), fill=floor)
    d.ellipse((-200, 1260, 1280, 1420), fill=floor)
    for x in range(0, W, 120): d.ellipse((x, 1500, x + 60, 1530), fill=(255, 255, 255, 50))
    return img

SC = [  # kind, colour, bg, object, name, sub-caption, name colour
    ("circle", (255, 80, 80), scene_bg((255, 200, 205), (255, 235, 225), (255, 160, 170)), sun(), "CIRCLE!", "ROUND LIKE THE SUN", (255, 90, 90)),
    ("square", (70, 140, 255), scene_bg((180, 215, 255), (225, 240, 255), (130, 180, 245)), present(), "SQUARE!", "4 SIDES", (80, 150, 255)),
    ("triangle", (70, 195, 100), scene_bg((195, 245, 195), (235, 255, 225), (130, 210, 130)), party_hat(), "TRIANGLE!", "3 SIDES", (80, 210, 110)),
    ("star", (255, 210, 40), scene_bg((40, 40, 110), (90, 70, 170), (60, 55, 140), night=True), twinkles(), "STAR!", "TWINKLE TWINKLE", (255, 220, 60)),
]
SPR = [(finish(shape(k, c), SP), finish(shape(k, c, True), SP)) for k, c, *_ in SC]
OBJ = [finish(s[3], 300) for s in SC]
NAME = [word_layers(s[4], 170, s[6]) for s in SC]
SUB = [word_layers(s[5], 84, (255, 255, 255)) for s in SC]
NUMS = [word_layers(str(i + 1), 64, (255, 255, 255))[0][0] for i in range(4)]
hook_bg = vgrad((255, 175, 215), (255, 230, 160))
hook1 = word_layers("LET'S LEARN", 120, (255, 255, 255)); hook2 = word_layers("SHAPES!", 190, (255, 230, 70))
mini = [s[0].resize((230, 230), Image.LANCZOS) for s in SPR]
minic = [s[1].resize((230, 230), Image.LANCZOS) for s in SPR]
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("GREAT JOB!", 130, (255, 255, 255))

def rays(base, t, cy=1000, col=(255, 255, 255, 55)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, cy), (CX + 2200 * math.cos(a0), cy + 2200 * math.sin(a0)), (CX + 2200 * math.cos(a0 + .22), cy + 2200 * math.sin(a0 + .22))], fill=col)

def corner_screen(px, py):
    return SX - SP / 2 + px * SP / 600, SFEET - SP + py * SP / 600

def hook(t):
    base = hook_bg.copy(); rays(base, t)
    for i, (x, y) in enumerate([(285, 1050), (695, 1050), (285, 1400), (695, 1400)]):
        yo, sx, sy = drop_land(t + 0.25 - i * 0.12, 0.3, 600)
        if t + 0.25 - i * 0.12 <= 0: continue
        bob = 18 * math.sin(t * 8 + i * 1.6)
        ground_shadow(base, x, y - 10, 200 * min(1, max(0.3, (t + 0.25 - i * 0.12) / 0.3)), 50)
        paste_scaled(base, (minic if blinking(t, i) and t > 0.5 else mini)[i].resize((320, 320)), x, y + yo + bob - 4, 1, 5 * math.sin(t * 6 + i), sx, sy, True)
    draw_words(base, hook1, CX, 420, t + 0.35, 0.08)
    draw_words(base, hook2, CX, 640, t + 0.15, 0.08)
    return base

def scene(i, lt):
    kind, col, bg, _o, *_r = SC[i]
    base = bg.copy(); d = ImageDraw.Draw(base)
    yo, sx, sy = drop_land(lt, 0.3, 900)
    sp = SPR[i][1] if blinking(lt, i) and lt > 0.7 else SPR[i][0]
    wig = 0 if corners(kind) else 3 * math.sin(lt * 5)
    ground_shadow(base, SX, SFEET - 18, SP * .7 * (0.5 + 0.5 * min(1, lt / .3)), 60)
    paste_scaled(base, sp, SX, SFEET + yo, 1, wig, sx, sy, True)
    draw_words(base, NAME[i], CX, 360, lt - 0.2)
    # corner counting: numbered dots pop on each corner, one by one
    cs = corners(kind)
    for k, (px, py) in enumerate(cs):
        s = ease_pop((lt - 0.6 - k * 0.25) / 0.3)
        if s <= 0: continue
        x, y = corner_screen(px, py)
        r = 46 * s
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 90, 140), outline=INK, width=6)
        paste_scaled(base, NUMS[k], x, y, s * 0.95)
    # example object pops beside the shape
    olt = lt - OBJ_AT
    if olt > 0:
        s = ease_pop(olt / 0.4) * (1 + 0.04 * math.sin(lt * 6))
        paste_scaled(base, OBJ[i], OX, OY + 10 * math.sin(lt * 4), s, 4 * math.sin(lt * 3))
        burst(d, OX, OY, olt, 8, 200)
    draw_words(base, SUB[i], CX, 560, lt - (OBJ_AT if not cs else 0.6 + 0.25 * len(cs)), 0.1)
    return camera(base, zoom_curve(max(0, lt - OBJ_AT), 1.05, 0.8), CX, 1000)

def ending(lt, t):
    base = hook_bg.copy(); rays(base, t, 1000, (255, 255, 255, 65)); d = ImageDraw.Draw(base)
    xs = [167, 382, 597, 812]
    for i, x in enumerate(xs):
        l = lt - i * 0.1
        if l <= 0: continue
        yo, sx, sy = drop_land(l, 0.3, 600)
        hop = -50 * abs(math.sin((lt) * 5 + i * .8)) if lt > 0.8 else 0
        ground_shadow(base, x, 1290, 150, 50)
        paste_scaled(base, (minic if blinking(lt, i) and lt > 0.8 else mini)[i].resize((205, 205)), x, 1300 + yo + hop, 1, 0, sx, sy, True)
    draw_words(base, end1, CX, 520, lt)
    draw_words(base, end2, CX, 780, lt - 0.25)
    confetti(d, lt - 0.1)
    return base

def raw(t):
    if t < T_HOOK: return hook(t)
    if t >= T_END: return ending(t - T_END, t)
    i = int((t - T_HOOK) // STEP); return scene(i, t - T_HOOK - i * STEP)

def frame(t):
    """Iris transition: the new scene opens in an expanding circle over the old one (0.22s)."""
    for b in [T_HOOK + k * STEP for k in range(5)]:
        if b <= t < b + 0.22:
            k = (t - b) / 0.22
            old, new = raw(b - 0.001), raw(t)
            m = Image.new("L", (W, H), 0); r = 1150 * ease_out(k)
            ImageDraw.Draw(m).ellipse((CX - r, 1000 - r, CX + r, 1000 + r), fill=255)
            old.paste(new, (0, 0), m)
            ImageDraw.Draw(old).ellipse((CX - r, 1000 - r, CX + r, 1000 + r), outline=(255, 255, 255), width=18)
            return old
    return raw(t)

# ---------- audio ----------
mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.08)
for i in range(4): place(mix, sfx_pop(), max(0, i * 0.12 - 0.05 + 0.3))
for i, key in enumerate("cstr"):
    st = T_HOOK + i * STEP
    place(mix, sfx_sparkle(), st); place(mix, sfx_boing(), st + 0.28)
    place(mix, load(f"{OUT}/{key}.wav"), st + 0.12)
    for k in range(len(corners(SC[i][0]))): place(mix, sfx_pop(), st + 0.63 + k * 0.25, 0.8)
    place(mix, sfx_ding(), st + OBJ_AT, 0.8)
place(mix, load(f"{OUT}/e.wav"), T_END + 0.1)
place(mix, sfx_sparkle(), T_END); place(mix, sfx_ding(), T_END + 0.15)
notes = [72, 76, 79, 76, 77, 81, 79, None, 76, 79, 84, 79, 77, 74, 72, None]
mix += 0.07 * synth_music(notes, 60 / 128 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.5, 1.2, 1.6, 2.3, 3.6, 4.4, 5.2, 6.2, 7.6, 8.4, 9.65, 10.8, 12.4, 13.4, 14.9], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
