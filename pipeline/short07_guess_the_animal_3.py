"""Guess the Animal #3 — frog (ribbit), hen (cluck), horse (neigh). Seamless loop ending (2026-10-28)."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s07"; SLUG = "guess-the-animal-3-short07"
CH = 620; CY = 1390

def poly(d, pts, fill, w=10): d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=OL, width=w * SS)

# ---------- backgrounds ----------
def clouds(d, spots):
    for cx, cy, s in spots:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 230))

def pond_bg():
    img = vgrad((110, 205, 250), (215, 245, 255)); d = ImageDraw.Draw(img, "RGBA")
    clouds(d, [(220, 320, 0.9), (800, 480, 0.7)])
    for x in range(-60, W + 60, 150):  # far bushes
        d.ellipse((x, 1060, x + 230, 1290), fill=(70, 170, 90))
    d.rectangle((0, 1230, W, H), fill=(60, 160, 230))
    for y in range(1270, H, 60):
        for x in range((y // 60) % 2 * 90, W, 180): d.arc((x, y, x + 110, y + 30), 200, 340, fill=(160, 220, 255, 200), width=6)
    for x, y, r in [(120, 1700, 90), (880, 1640, 80), (930, 1300, 60)]:
        d.ellipse((x - r, y - r * .45, x + r, y + r * .45), fill=(90, 190, 80), outline=(50, 120, 50), width=5)
        d.polygon([(x, y), (x + r, y - 15), (x + r, y + 15)], fill=(60, 160, 230))
    for x in (40, 80, 990, 1030):  # cattails
        d.line((x, 1420, x + 10, 1020), fill=(70, 140, 60), width=12)
        d.rounded_rectangle((x - 2, 1020, x + 26, 1130), 14, fill=(140, 85, 45))
    # big lily pad the frog sits on
    d.ellipse((CX - 330, CY - 70, CX + 330, CY + 90), fill=(100, 200, 90), outline=(50, 120, 50), width=8)
    d.polygon([(CX, CY + 10), (CX + 160, CY + 95), (CX + 260, CY + 70)], fill=(60, 160, 230))
    for k in range(5):  # pink water flower
        a = k * 2 * math.pi / 5
        d.ellipse((780 + 34 * math.cos(a) - 30, 1500 + 20 * math.sin(a) - 22, 780 + 34 * math.cos(a) + 30, 1500 + 20 * math.sin(a) + 22), fill=(255, 150, 200))
    d.ellipse((765, 1488, 795, 1512), fill=(255, 220, 80))
    return img

def farm_bg():
    img = vgrad((255, 210, 150), (255, 245, 210)); d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((760, 240, 960, 440), fill=(255, 230, 90))
    clouds(d, [(250, 330, 0.8)])
    # red barn on the left
    d.polygon([(-60, 950), (140, 760), (340, 950)], fill=(200, 50, 50), outline=(120, 30, 30))
    d.rectangle((-40, 950, 320, 1350), fill=(220, 65, 60))
    d.rectangle((60, 1100, 220, 1350), fill=(255, 245, 230)); d.line((60, 1100, 220, 1350), fill=(220, 65, 60), width=14); d.line((220, 1100, 60, 1350), fill=(220, 65, 60), width=14)
    d.rectangle((0, 1300, W, H), fill=(150, 205, 90))
    for x in range(330, W, 120):  # wooden fence
        d.rounded_rectangle((x, 1150, x + 34, 1330), 8, fill=(190, 130, 80), outline=(120, 80, 45), width=4)
    for y in (1190, 1260): d.rectangle((330, y, W, y + 26), fill=(205, 145, 90), outline=(120, 80, 45), width=4)
    rng = np.random.default_rng(7)
    for _ in range(60):  # grain
        x, y = rng.integers(0, W), rng.integers(1440, H)
        d.ellipse((x - 7, y - 4, x + 7, y + 4), fill=(240, 200, 90))
    # little nest with eggs
    d.ellipse((760, 1420, 960, 1520), fill=(170, 120, 60), outline=(110, 70, 30), width=6)
    for x in (810, 860, 905): d.ellipse((x - 26, 1400, x + 26, 1470), fill=(255, 250, 240), outline=(150, 140, 120), width=4)
    d.arc((760, 1380, 960, 1500), 0, 180, fill=(110, 70, 30), width=10)
    return img

def field_bg():
    img = vgrad((170, 230, 210), (235, 250, 225)); d = ImageDraw.Draw(img, "RGBA")
    clouds(d, [(180, 300, 0.8), (780, 400, 1.0)])
    d.ellipse((-500, 1050, 800, 1700), fill=(130, 200, 100)); d.ellipse((350, 1000, 1700, 1700), fill=(115, 190, 95))
    d.rectangle((0, 1380, W, H), fill=(150, 215, 110))
    d.ellipse((860, 820, 1060, 1020), fill=(70, 165, 80)); d.ellipse((800, 890, 960, 1050), fill=(80, 175, 85))
    d.rectangle((930, 1000, 965, 1160), fill=(130, 85, 50))
    for x in range(-20, W, 140):  # white fence
        d.rounded_rectangle((x, 1180, x + 36, 1370), 10, fill=(255, 255, 255), outline=(170, 170, 190), width=4)
    for y in (1220, 1290): d.rectangle((0, y, W, y + 24), fill=(255, 255, 255), outline=(170, 170, 190), width=4)
    rng = np.random.default_rng(11)
    for _ in range(35):
        x, y = rng.integers(0, W), rng.integers(1460, H)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 235, 90)); d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 160, 40))
    # hay bale
    d.rounded_rectangle((40, 1280, 230, 1420), 26, fill=(240, 200, 90), outline=(170, 130, 50), width=6)
    for x in (80, 135, 190): d.line((x, 1295, x, 1405), fill=(200, 160, 60), width=5)
    return img

# ---------- characters (900px canvas, feet at y~860) ----------
def frog(closed=False):
    im, d = canvas()
    G, G2, L = (110, 200, 80, 255), (80, 165, 60, 255), (215, 245, 160, 255)
    for sx in (-1, 1):  # back legs
        E(d, (450 + sx * 230 - 110, 620, 450 + sx * 230 + 110, 860), G2)
    E(d, (230, 420, 670, 850), G)
    E(d, (330, 560, 570, 830), L, 0)
    for sx in (-1, 1):  # front feet
        E(d, (450 + sx * 110 - 60, 800, 450 + sx * 110 + 60, 870), G)
    E(d, (170, 240, 730, 610), G)
    for sx in (-1, 1):  # eye bumps on top of the head
        E(d, (450 + sx * 140 - 115, 130, 450 + sx * 140 + 115, 360), G)
    for cx, cy, r in [(300, 470, 22), (610, 440, 18), (560, 520, 14)]:
        d.ellipse(S((cx - r, cy - r, cx + r, cy + r)), fill=G2)
    eyes(d, 450, 245, 140, 62, closed)
    d.arc(S((280, 360, 620, 540)), 15, 165, fill=OL, width=11 * SS)
    cheeks(d, 450, 470, 210)
    for sx in (-1, 1): d.ellipse(S((450 + sx * 30 - 9, 380, 450 + sx * 30 + 9, 395)), fill=OL)
    return im

def hen(closed=False):
    im, d = canvas()
    B, B2, BR = (205, 120, 60, 255), (240, 190, 130, 255), (160, 85, 40, 255)
    for k, (x0, y0) in enumerate([(600, 260), (650, 330), (620, 420)]):  # tail feathers
        E(d, (x0, y0, x0 + 170, y0 + 110), BR if k % 2 else B)
    for sx in (-1, 1):  # legs
        x = 450 + sx * 80
        d.line(S((x, 760, x, 850)), fill=(255, 160, 40, 255), width=16 * SS)
        for dx in (-34, 0, 34): d.line(S((x, 850, x + dx, 868)), fill=(255, 160, 40, 255), width=12 * SS)
    E(d, (200, 330, 700, 800), B)
    E(d, (330, 480, 570, 780), B2, 0)
    E(d, (190, 470, 400, 680), BR)  # wing
    for cx in (390, 450, 510):  # comb
        E(d, (cx - 45, 50, cx + 45, 150), (235, 50, 60, 255))
    E(d, (295, 105, 605, 420), B)
    eyes(d, 450, 230, 78, 40, closed)
    cheeks(d, 450, 300, 120)
    E(d, (430, 315, 470, 385), (235, 50, 60, 255), 6)  # wattle
    poly(d, [(410, 280), (490, 280), (450, 335)], (255, 200, 40, 255), 7)  # beak
    return im

def horse(closed=False):
    """Side view facing left: long head + muzzle, mane along the neck, tail, 4 legs with hooves."""
    im, d = canvas()
    B, M, MZ = (190, 120, 70, 255), (90, 55, 35, 255), (240, 205, 160, 255)
    d.line(S((740, 470, 830, 560, 830, 700, 790, 770)), fill=OL, width=60 * SS, joint="curve")
    d.line(S((740, 470, 830, 560, 830, 700, 790, 770)), fill=M, width=44 * SS, joint="curve")  # tail
    for x in (330, 410, 610, 690):
        d.rounded_rectangle(S((x - 34, 560, x + 34, 830)), 20 * SS, fill=B, outline=OL, width=9 * SS)
        d.rounded_rectangle(S((x - 38, 800, x + 38, 868)), 14 * SS, fill=(70, 50, 45, 255), outline=OL, width=8 * SS)
    for k, (cx, cy) in enumerate([(330, 130), (370, 210), (400, 290), (425, 370), (445, 445)]):  # mane
        E(d, (cx - 50, cy - 50, cx + 50, cy + 50), M, 8)
    poly(d, [(250, 560), (430, 480), (360, 170), (200, 210)], B, 10)  # neck
    E(d, (250, 410, 770, 700), B)
    E(d, (140, 110, 380, 330), B)
    E(d, (40, 210, 260, 400), MZ)
    poly(d, [(270, 140), (330, 150), (318, 30)], B, 9)  # ear
    poly(d, [(285, 132), (318, 136), (313, 70)], (240, 160, 150, 255), 0)
    for cx, cy in [(255, 120), (215, 135)]:  # forelock
        E(d, (cx - 40, cy - 40, cx + 40, cy + 40), M, 7)
    eyes(d, 255, 215, 0, 46, closed)
    E(d, (78, 270, 118, 310), (90, 60, 50, 255), 0)  # nostril
    d.arc(S((70, 300, 190, 370)), 10, 150, fill=OL, width=9 * SS)  # smile
    d.ellipse(S((170, 280, 240, 320)), fill=(235, 150, 140, 255))
    return im

def mk(fn):
    o = finish(fn(False), CH); c = finish(fn(True), CH)
    return o, c, silhouette(o)

SC = [  # start, end, bg, sprites, question, answer, answer colour
    (1.5, 5.4, pond_bg(), mk(frog), "WHO SAYS RIBBIT?", "FROGGY!", (140, 235, 100)),
    (5.4, 9.3, farm_bg(), mk(hen), "WHO SAYS CLUCK?", "HEN!", (255, 200, 80)),
    (9.3, 13.2, field_bg(), mk(horse), "WHO SAYS NEIGH?", "HORSEY!", (255, 170, 110)),
]
REVEAL = 1.6
intro_bg = vgrad((90, 200, 220), (205, 240, 140))
qm = word_layers("?", 300, (255, 255, 255))[0][0]
q_words = [word_layers(s[4], 96, (255, 255, 255)) for s in SC]
a_words = [word_layers(s[5], 170, s[6]) for s in SC]
hook1 = word_layers("GUESS THE", 120, (255, 255, 255)); hook2 = word_layers("ANIMAL!", 160, (255, 230, 70))
badge = word_layers("#3", 90, (255, 255, 255), stroke=(30, 120, 200))
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("GREAT JOB!", 130, (255, 255, 255))
peek = [s[3][2].resize((300, 300)) for s in SC]
mini = [s[3][0].resize((300, 300)) for s in SC]

def rays(base, t, col=(255, 255, 255, 50)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, 900), (CX + 2000 * math.cos(a0), 900 + 2000 * math.sin(a0)), (CX + 2000 * math.cos(a0 + .22), 900 + 2000 * math.sin(a0 + .22))], fill=col)

def hook(t):
    base = intro_bg.copy(); rays(base, t)
    for i, x in enumerate((220, 490, 760)):
        bob = 30 * math.sin(t * 8 + i * 1.7)
        paste_scaled(base, peek[i], x, 1150 + bob, 1.0, 6 * math.sin(t * 6 + i))
        paste_scaled(base, qm, x, 1150 + bob, 0.45)
    draw_words(base, hook1, CX, 480, t + 0.5, 0.08)
    draw_words(base, hook2, CX, 680, t + 0.5, 0.08)
    draw_words(base, badge, CX, 860, t + 0.4)  # visible from frame 0 (loop target)
    return base

def ending(lt, t):
    base = intro_bg.copy(); rays(base, t, (255, 255, 255, 60)); d = ImageDraw.Draw(base)
    confetti(d, lt)
    for i, x in enumerate((220, 490, 760)):
        yo, sx, sy = drop_land(lt - i * .1, 0.3, 500)
        if lt - i * .1 > 0: paste_scaled(base, mini[i], x, 1300 + yo + 8 * math.sin(t * 9 + i), 1, 0, sx, sy, True)
    draw_words(base, end1, CX, 560, lt)
    draw_words(base, end2, CX, 800, lt - 0.2)
    return base

def scene(i, lt):
    st, en, bg, (op, cl, sil), *_r = SC[i]
    base = bg.copy()
    yo, sx, sy = drop_land(lt, 0.3, 800)
    wig = 3 * math.sin(lt * 6)
    ground_shadow(base, CX, CY - 25, CH * 0.7 * (0.6 + 0.4 * min(1, lt / 0.3)))
    if lt < REVEAL:
        paste_scaled(base, sil, CX, CY + yo, 1, wig, sx, sy, True)
        paste_scaled(base, qm, CX, 1040 + 15 * math.sin(lt * 9), ease_pop((lt - .3) / .4) * .8, 8 * math.sin(lt * 5))
        draw_words(base, q_words[i], CX, 330, lt)
        return base
    rt = lt - REVEAL
    sp = cl if blinking(rt, i) and rt > 0.5 else op
    s = 1 + 0.15 * math.exp(-rt * 6) * math.sin(rt * 25)
    paste_scaled(base, sp, CX, CY, s, wig, 1, 1, True)
    d = ImageDraw.Draw(base); burst(d, CX, 1080, rt)
    draw_words(base, a_words[i], CX, 400, rt)
    if rt < 0.12: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(180 * (1 - rt / .12)))))
    base = shake(base, 0, rt)
    return camera(base, zoom_curve(rt, 1.05), CX, 1080)

def raw(t):
    if t < 1.5: return hook(t)
    if t >= 13.2: return ending(t - 13.2, t)
    for i, s in enumerate(SC):
        if s[0] <= t < s[1]: return scene(i, t - s[0])

def frame(t): return with_transitions(raw, [1.5, 5.4, 9.3, 13.2], t)

# ---------- audio ----------
mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.05)
for k, (st, *_r) in enumerate(SC):
    place(mix, load(f"{OUT}/l{1 + 2 * k}.wav"), st + 0.1)
    place(mix, load(f"{OUT}/l{2 + 2 * k}.wav"), st + REVEAL + 0.1)
    place(mix, sfx_boing(), st + 0.28); place(mix, sfx_sparkle(), st + REVEAL)
place(mix, load(f"{OUT}/l7.wav"), 13.25)
for i in range(3): place(mix, sfx_pop(), 13.5 + i * .1)
place(mix, sfx_ding(), 13.25)
notes = [72, 74, 76, 79, 76, 74, 72, None, 69, 72, 74, 76, 74, 72, 67, None]
mix += 0.075 * synth_music(notes, 60 / 120 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.7, 1.6, 2.2, 3.4, 4.5, 5.6, 7.5, 9.4, 11.5, 12.8, 13.3, 13.9, 14.4, 14.8, 14.97], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
