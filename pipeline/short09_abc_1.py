"""ABC Fun #1 — A is for Apple, B is for Ball, C is for Car (2026-10-29).
Guess-then-reveal per letter; new 'letter link' beat (first letter flies from the word up to the big letter)
and drifting parallax clouds."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s09"; SLUG = "abc-fun-1-short09"
CH = 560; OY = 1080  # object size / centre

def poly(d, pts, fill, w=10): d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=OL, width=w * SS)

# ---------- backgrounds (one dominant colour each) ----------
def orchard_bg():
    img = vgrad((255, 190, 190), (255, 235, 225)); d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((-300, 1300, 700, 1900), fill=(140, 210, 110)); d.ellipse((400, 1280, 1400, 1900), fill=(120, 195, 95))
    d.rectangle((0, 1560, W, H), fill=(150, 215, 115))
    for x in (60, 1000):
        d.rectangle((x - 22, 1100, x + 22, 1420), fill=(140, 90, 55))
        d.ellipse((x - 140, 880, x + 140, 1160), fill=(90, 175, 80))
        for dx, dy in [(-60, -40), (50, 10), (-20, 60)]: d.ellipse((x + dx - 18, 1020 + dy - 18, x + dx + 18, 1020 + dy + 18), fill=(230, 60, 60))
    return img

def park_bg():
    img = vgrad((140, 200, 255), (215, 238, 255)); d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 1440, W, H), fill=(120, 200, 100))
    d.ellipse((-200, 1340, 1300, 1560), fill=(120, 200, 100))
    for x in range(30, W, 120):
        d.ellipse((x - 20, 1620 + (x % 3) * 40, x + 20, 1660 + (x % 3) * 40), fill=(255, 255, 255, 180))
    # goal net on the right edge (background decoration)
    d.rectangle((960, 1150, 1080, 1460), outline=(255, 255, 255), width=12)
    for y in range(1170, 1460, 40): d.line((960, y, 1080, y), fill=(255, 255, 255, 120), width=3)
    return img

def road_bg():
    img = vgrad((255, 225, 110), (255, 245, 200)); d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((780, 220, 980, 420), fill=(255, 250, 220))
    for x, h, c in [(0, 380, (255, 170, 90)), (150, 300, (120, 180, 255)), (840, 340, (255, 130, 150)), (980, 420, (140, 210, 140))]:
        d.rectangle((x, 1350 - h, x + 130, 1350), fill=c)
        for wy in range(1350 - h + 30, 1330, 70):
            d.rectangle((x + 25, wy, x + 55, wy + 35), fill=(255, 255, 230)); d.rectangle((x + 75, wy, x + 105, wy + 35), fill=(255, 255, 230))
    d.rectangle((0, 1350, W, H), fill=(110, 110, 130))
    for x in range(-40, W, 200): d.rectangle((x, 1600, x + 110, 1625), fill=(255, 255, 255))
    d.rectangle((0, 1350, W, 1380), fill=(200, 200, 210))
    return img

# ---------- objects with faces (900 canvas) ----------
def face(d, cx, cy, closed, gap=95, r=46, sm=55):
    eyes(d, cx, cy, gap, r, closed); cheeks(d, cx, cy + 90, gap + 50); smile(d, cx, cy + 85, sm)

def apple(closed=False):
    im, d = canvas()
    R = (230, 50, 55, 255)
    d.line(S((450, 250, 470, 120)), fill=(110, 70, 40, 255), width=26 * SS)
    E(d, (470, 110, 640, 200), (90, 190, 80, 255), 8)
    E(d, (150, 230, 480, 800), R); E(d, (420, 230, 750, 800), R)
    E(d, (190, 260, 710, 790), R, 0)
    d.ellipse(S((240, 330, 320, 450)), fill=(255, 255, 255, 120))
    face(d, 450, 470, closed)
    return im

def ball(closed=False):
    im, d = canvas()
    cols = [(255, 80, 80, 255), (255, 255, 255, 255), (60, 140, 255, 255), (255, 255, 255, 255), (255, 210, 50, 255), (255, 255, 255, 255)]
    for k, c in enumerate(cols):
        d.pieslice(S((130, 130, 770, 770)), -90 + k * 60, -30 + k * 60, fill=c)
    d.ellipse(S((130, 130, 770, 770)), outline=OL, width=10 * SS)
    d.ellipse(S((400, 400, 500, 500)), fill=(255, 255, 255, 255), outline=OL, width=6 * SS)
    d.rounded_rectangle(S((260, 380, 640, 640)), 120 * SS, fill=(255, 255, 255, 235))  # face patch
    face(d, 450, 470, closed, 80, 42, 50)
    return im

def car(closed=False):
    im, d = canvas()
    B = (70, 150, 255, 255)
    d.rounded_rectangle(S((230, 230, 650, 470)), 90 * SS, fill=B, outline=OL, width=10 * SS)  # cabin
    d.rounded_rectangle(S((280, 270, 600, 450)), 60 * SS, fill=(230, 245, 255, 255), outline=OL, width=7 * SS)  # windscreen
    d.rounded_rectangle(S((90, 420, 810, 700)), 110 * SS, fill=B, outline=OL, width=10 * SS)  # body
    eyes(d, 440, 360, 80, 46, closed)
    smile(d, 450, 560, 70); cheeks(d, 450, 560, 200)
    for x in (130, 770): E(d, (x - 40, 470, x + 40, 540), (255, 240, 120, 255), 7)  # headlights
    for x in (250, 650):
        E(d, (x - 105, 600, x + 105, 810), (50, 45, 60, 255))
        E(d, (x - 45, 660, x + 45, 750), (200, 200, 210, 255), 6)
    return im

def letter_block(ch, col):
    im, d = canvas(400)
    d.rounded_rectangle(S((30, 30, 370, 370)), 50 * SS, fill=col, outline=OL, width=10 * SS)
    d.rounded_rectangle(S((60, 60, 340, 340)), 36 * SS, outline=(255, 255, 255, 160), width=8 * SS)
    f = font(230 * SS); tw = d.textlength(ch, font=f)
    d.text(((400 * SS - tw) / 2, 10 * SS), ch, font=f, fill=(255, 255, 255, 255), stroke_width=9 * SS, stroke_fill=INK)
    return shade(im).resize((300, 300), Image.LANCZOS)

def mk(fn):
    o = finish(fn(False), CH); c = finish(fn(True), CH)
    return o, c, silhouette(o)

CLOUDS = [(200, 330, 0.9), (760, 470, 0.7), (520, 250, 0.5)]
SC = [  # start, end, bg, sprites, letter, word, colour
    (1.5, 5.4, orchard_bg(), mk(apple), "A", "APPLE", (235, 60, 70)),
    (5.4, 9.3, park_bg(), mk(ball), "B", "BALL", (40, 120, 240)),
    (9.3, 13.2, road_bg(), mk(car), "C", "CAR", (250, 150, 20)),
]
REVEAL = 1.35; LINK = 2.5
big = [word_layers(s[4] + s[4].lower(), 330, s[6]) for s in SC]
q_words = [word_layers(f"{s[4]} IS FOR...?", 100, (255, 255, 255)) for s in SC]
qm = word_layers("?", 300, (255, 255, 255))[0][0]
def word_split(w, col):
    """word layer pieces: first letter (colour) + rest (white), positioned around CX."""
    f = font(170); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w0, w1 = d.textlength(w[0], font=f), d.textlength(w[1:], font=f); tot = w0 + w1
    a = word_layers(w[0], 170, col)[0][0]; b = word_layers(w[1:], 170, (255, 255, 255))[0][0]
    return (a, -tot / 2 + w0 / 2), (b, -tot / 2 + w0 + w1 / 2)
words = [word_split(s[5], s[6]) for s in SC]
blocks = [letter_block(ch, c) for ch, c in [("A", (235, 70, 80, 255)), ("B", (60, 140, 250, 255)), ("C", (255, 170, 40, 255))]]
hook1 = word_layers("LET'S LEARN", 120, (255, 255, 255)); hook2 = word_layers("A B C!", 190, (255, 230, 70))
badge = word_layers("#1", 90, (255, 255, 255), stroke=(200, 60, 120))
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("GREAT JOB!", 130, (255, 255, 255))
mini = [s[3][0].resize((280, 280)) for s in SC]
intro_bg = vgrad((255, 150, 190), (255, 225, 140))

def rays(base, t, col=(255, 255, 255, 55)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, 1000), (CX + 2000 * math.cos(a0), 1000 + 2000 * math.sin(a0)), (CX + 2000 * math.cos(a0 + .22), 1000 + 2000 * math.sin(a0 + .22))], fill=col)

def hook(t):
    base = intro_bg.copy(); rays(base, t)
    for i, x in enumerate((215, 490, 765)):
        bob = 34 * math.sin(t * 8 + i * 1.9)
        paste_scaled(base, blocks[i], x, 1150 + bob, 0.85, 7 * math.sin(t * 6 + i))
    draw_words(base, hook1, CX, 480, t + 0.5, 0.08)
    draw_words(base, hook2, CX, 700, t + 0.5, 0.08)
    draw_words(base, badge, CX, 1400, t + 0.4)
    return base

def ending(lt, t):
    base = intro_bg.copy(); rays(base, t, (255, 255, 255, 60)); d = ImageDraw.Draw(base)
    confetti(d, lt)
    for i, x in enumerate((215, 490, 765)):
        yo, sx, sy = drop_land(lt - i * .1, 0.3, 500)
        if lt - i * .1 > 0: paste_scaled(base, mini[i], x, 1340 + yo + 8 * math.sin(t * 9 + i), 1, 0, sx, sy, True)
        paste_scaled(base, blocks[i], x, 980 + 12 * math.sin(t * 7 + i), 0.55 * ease_pop((lt - .25 - i * .1) / .35))
    draw_words(base, end1, CX, 500, lt)
    draw_words(base, end2, CX, 720, lt - 0.2)
    return base

def scene(i, lt, t):
    st, en, bg, (op, cl, sil), L, Wd, col = SC[i]
    base = bg.copy(); drift_clouds(base, t, CLOUDS)
    # big letter pops in at the top and bounces gently
    bl = 1 + 0.05 * math.sin(lt * 5)
    if lt >= LINK and lt < LINK + 0.6: bl += 0.25 * math.exp(-(lt - LINK - 0.35) * 8) * (lt > LINK + 0.35)
    for lay, ox in big[i]: paste_scaled(base, lay, CX + ox, 560, ease_pop(lt / .35) * bl)
    ground_shadow(base, CX, OY + CH * 0.36, CH * 0.6)
    if lt < REVEAL:
        yo, sx, sy = drop_land(lt, 0.3, 400)
        paste_scaled(base, sil, CX, OY + yo, 1, 3 * math.sin(lt * 6), sx, sy)
        paste_scaled(base, qm, CX, OY + 15 * math.sin(lt * 9), ease_pop((lt - .3) / .4) * .7)
        draw_words(base, q_words[i], CX, 280, lt)
        return base
    rt = lt - REVEAL
    sp = cl if blinking(rt, i) and rt > 0.5 else op
    s = 1 + 0.15 * math.exp(-rt * 6) * math.sin(rt * 25)
    paste_scaled(base, sp, CX, OY + 6 * math.sin(lt * 4), s, 3 * math.sin(lt * 6))
    d = ImageDraw.Draw(base); burst(d, CX, OY, rt)
    (a, ax), (b, bx) = words[i]
    paste_scaled(base, a, CX + ax, 1430, ease_pop(rt / .35)); paste_scaled(base, b, CX + bx, 1430, ease_pop((rt - .08) / .35))
    if lt >= LINK:  # letter link: a copy of the first letter flies from the word up to the big letter
        k = (lt - LINK) / 0.45
        if k < 1: fly(a, base, (CX + ax, 1430), (CX + big[i][0][1], 560), k, 1.0, 330 / 170, -120)
    if rt < 0.12: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(180 * (1 - rt / .12)))))
    base = shake(base, 0, rt)
    return camera(base, zoom_curve(rt, 1.05), CX, OY)

def raw(t):
    if t < 1.5: return hook(t)
    if t >= 13.2: return ending(t - 13.2, t)
    for i, s in enumerate(SC):
        if s[0] <= t < s[1]: return scene(i, t - s[0], t)

def frame(t): return with_transitions(raw, [1.5, 5.4, 9.3, 13.2], t)

# ---------- audio ----------
mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.05)
for k, (st, *_r) in enumerate(SC):
    place(mix, load(f"{OUT}/l{1 + 2 * k}.wav"), st + 0.15)
    place(mix, load(f"{OUT}/l{2 + 2 * k}.wav"), st + REVEAL + 0.05)
    place(mix, sfx_boing(), st + 0.28); place(mix, sfx_sparkle(), st + REVEAL); place(mix, sfx_pop(), st + LINK + 0.35)
place(mix, load(f"{OUT}/l7.wav"), 13.25)
for i in range(3): place(mix, sfx_pop(), 13.45 + i * .1)
place(mix, sfx_ding(), 13.25)
notes = [67, 67, 74, 74, 76, 76, 74, None, 72, 72, 71, 71, 69, 69, 67, None]
mix += 0.075 * synth_music(notes, 60 / 120 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.7, 1.6, 2.3, 3.0, 4.2, 4.9, 5.6, 7.5, 8.2, 9.5, 11.3, 12.0, 13.5, 14.2, 14.97], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
