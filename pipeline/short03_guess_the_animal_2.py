"""Guess the Animal #2 — sheep (baa), dog (woof), cat (meow)."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s03"; SLUG = "guess-the-animal-2-short03"
CH = 620  # character size on screen; centred at y=1080 -> 770..1390 (inside safe zone)
CY = 1390  # feet line (anchor bottom)

# ---------- backgrounds ----------
def flowers(d, y0=1500, n=40, seed=3):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rng.integers(0, W), rng.integers(y0, H)
        c = [(255, 230, 80), (255, 140, 180), (255, 255, 255), (180, 140, 255)][rng.integers(0, 4)]
        for a in range(5):
            ang = a * 2 * math.pi / 5
            d.ellipse((x + 14 * math.cos(ang) - 10, y + 14 * math.sin(ang) - 10, x + 14 * math.cos(ang) + 10, y + 14 * math.sin(ang) + 10), fill=c)
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(255, 190, 40))

def hills_bg(top, bot, g1, g2, extra=None):
    img = vgrad(top, bot); d = ImageDraw.Draw(img, "RGBA")
    for cx, cy, s in [(200, 330, 1.0), (760, 520, 0.8)]:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 230))
    d.ellipse((-400, 1150, 900, 2300), fill=g2); d.ellipse((300, 1220, 1600, 2300), fill=g2)
    d.rectangle((0, 1420, W, H), fill=g1); d.ellipse((-300, 1320, 1400, 1660), fill=g1)
    if extra: extra(d)
    flowers(d)
    return img

def meadow(d):  # rainbow + stone wall (sheep)
    for i, c in enumerate([(255, 90, 90), (255, 170, 60), (255, 230, 80), (110, 210, 110), (90, 160, 255), (170, 120, 230)]):
        r = 620 - i * 34
        d.arc((540 - r, 1150 - r, 540 + r, 1150 + r), 180, 360, fill=c + (200,), width=34)
    for x in range(-20, W, 110):
        d.rounded_rectangle((x, 1330, x + 100, 1400), 18, fill=(170, 165, 175), outline=(110, 105, 120), width=5)

def park(d):  # dog house + bone (dog)
    d.polygon([(800, 1130), (920, 1030), (1040, 1130)], fill=(230, 80, 70))
    d.rectangle((815, 1130, 1025, 1330), fill=(90, 150, 230))
    d.ellipse((870, 1200, 970, 1330), fill=(40, 40, 70)); d.rectangle((870, 1260, 970, 1330), fill=(40, 40, 70))
    for x in (40, 160):
        d.ellipse((x - 30, 1010, x + 90, 1130), fill=(60, 160, 70)); d.rectangle((x + 20, 1110, x + 40, 1330), fill=(130, 85, 50))

def cosy(top, bot):  # indoor room for the cat: wall, window, rug
    img = vgrad(top, bot); d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 90): d.rectangle((x, 0, x + 45, 1420), fill=(255, 255, 255, 40))
    d.rounded_rectangle((640, 300, 1000, 700), 30, fill=(150, 215, 255), outline=(255, 255, 255), width=18)
    d.line((820, 300, 820, 700), fill=(255, 255, 255), width=14); d.line((640, 500, 1000, 500), fill=(255, 255, 255), width=14)
    d.ellipse((870, 340, 960, 430), fill=(255, 235, 110))
    d.rectangle((0, 1420, W, H), fill=(205, 150, 105))
    for y in range(1440, H, 70): d.line((0, y, W, y), fill=(180, 125, 85), width=6)
    d.ellipse((60, 1300, 920, 1520), fill=(255, 130, 170)); d.ellipse((140, 1330, 840, 1490), fill=(255, 180, 205))
    # ball of yarn
    d.ellipse((60, 1180, 200, 1320), fill=(120, 140, 255), outline=(60, 70, 160), width=6)
    for k in range(3): d.arc((70 + k * 15, 1190 + k * 10, 190 - k * 15, 1310 - k * 10), 200, 340, fill=(60, 70, 160), width=5)
    return img

# ---------- characters ----------
def sheep(closed=False):
    im, d = canvas()
    for x in (330, 420, 500, 590):
        d.rounded_rectangle(S((x - 26, 640, x + 26, 840)), 20 * SS, fill=(60, 55, 70, 255), outline=OL, width=8 * SS)
    for cx, cy in [(260, 560), (340, 470), (450, 440), (560, 470), (640, 560), (600, 680), (450, 720), (300, 680), (450, 580)]:
        E(d, (cx - 110, cy - 100, cx + 110, cy + 100), (250, 250, 248, 255), 9)
    for cx, cy in [(450, 580), (340, 560), (560, 560)]:
        E(d, (cx - 100, cy - 90, cx + 100, cy + 90), (250, 250, 248, 255), 0)
    for sx in (-1, 1):
        E(d, (450 + sx * 150 - 75, 230, 450 + sx * 150 + 75, 290), (70, 65, 80, 255), 8)
    E(d, (300, 160, 600, 480), (75, 70, 85, 255))
    for cx, cy in [(380, 150), (450, 120), (520, 150)]:
        E(d, (cx - 60, cy - 55, cx + 60, cy + 55), (250, 250, 248, 255), 8)
    eyes(d, 450, 300, 70, 44, closed)
    cheeks(d, 450, 390, 110)
    d.arc(S((420, 380, 480, 430)), 20, 160, fill=(250, 250, 250, 255), width=8 * SS)
    return im

def dog(closed=False):
    im, d = canvas()
    B, B2 = (205, 140, 80, 255), (240, 205, 160, 255)
    d.arc(S((620, 440, 780, 620)), 200, 330, fill=OL, width=34 * SS); d.arc(S((620, 440, 780, 620)), 200, 330, fill=B, width=20 * SS)
    for x in (320, 410, 500, 590):
        E(d, (x - 42, 640, x + 42, 860), B)
        E(d, (x - 48, 815, x + 48, 865), B2)
    E(d, (220, 470, 700, 780), B)
    E(d, (340, 540, 560, 760), B2, 0)
    E(d, (270, 110, 630, 480), B)
    E(d, (510, 150, 620, 280), (130, 80, 45, 255), 0)  # eye patch
    for sx in (-1, 1):  # floppy ears
        x = 450 + sx * 200
        E(d, (x - 70, 130, x + 70, 400), (130, 80, 45, 255))
    eyes(d, 450, 260, 85, 44, closed)
    E(d, (350, 320, 550, 470), B2)
    E(d, (410, 320, 490, 380), (40, 30, 30, 255), 0)
    d.ellipse(S((428, 330, 450, 345)), fill=(255, 255, 255, 200))
    smile(d, 450, 410, 45)
    d.rounded_rectangle(S((425, 440, 475, 510)), 24 * SS, fill=(255, 110, 130, 255), outline=OL, width=7 * SS)
    d.rounded_rectangle(S((300, 470, 600, 510)), 18 * SS, fill=(230, 50, 60, 255), outline=OL, width=7 * SS)  # collar
    E(d, (425, 495, 475, 545), (255, 210, 60, 255), 7)
    return im

def cat(closed=False):
    im, d = canvas()
    O, O2 = (255, 160, 60, 255), (255, 235, 200, 255)
    tail = [(600, 740), (690, 730), (750, 660), (770, 570), (750, 480), (710, 440)]
    d.line(S([c for p in tail for c in p]), fill=OL, width=40 * SS, joint="curve")
    d.line(S([c for p in tail for c in p]), fill=O, width=24 * SS, joint="curve")
    E(d, (690, 420, 732, 462), O, 0)
    for x in (340, 420, 490, 570):
        E(d, (x - 38, 660, x + 38, 860), O)
        E(d, (x - 44, 820, x + 44, 866), O2)
    E(d, (250, 480, 670, 790), O)
    E(d, (360, 560, 560, 770), O2, 0)
    for sx in (-1, 1):
        cx = 450 + sx * 150
        d.polygon([(v[0] * SS, v[1] * SS) for v in [(cx - 85, 220), (cx + 85, 220), (cx + sx * 60, 60)]], fill=O, outline=OL, width=10 * SS)
        d.polygon([(v[0] * SS, v[1] * SS) for v in [(cx - 45, 200), (cx + 45, 200), (cx + sx * 45, 110)]], fill=(255, 170, 190, 255))
    E(d, (250, 140, 650, 500), O)
    for dx in (-40, 0, 40):  # forehead stripes
        d.line(S((450 + dx, 150, 450 + dx * 0.7, 200)), fill=(220, 110, 30, 255), width=14 * SS)
    eyes(d, 450, 290, 90, 46, closed)
    cheeks(d, 450, 390, 150)
    d.polygon([(v[0] * SS, v[1] * SS) for v in [(425, 365), (475, 365), (450, 392)]], fill=(255, 120, 150, 255), outline=OL, width=5 * SS)
    d.arc(S((410, 380, 452, 425)), 20, 160, fill=OL, width=7 * SS); d.arc(S((448, 380, 490, 425)), 20, 160, fill=OL, width=7 * SS)
    for sx in (-1, 1):
        for k, dy in enumerate((-15, 10)):
            d.line(S((450 + sx * 80, 390 + dy * .3, 450 + sx * 210, 375 + dy)), fill=OL, width=5 * SS)
    return im

def mk(fn):
    o = finish(fn(False), CH); c = finish(fn(True), CH)
    return o, c, silhouette(o)

# ---------- scenes ----------
SC = [  # start, end, bg, sprites, question, answer, answer colour
    (1.5, 5.4, hills_bg((120, 200, 255), (205, 238, 255), (120, 205, 90), (95, 185, 75), meadow), mk(sheep), "WHO SAYS BAA?", "SHEEP!", (255, 255, 255)),
    (5.4, 9.3, hills_bg((255, 200, 120), (255, 238, 190), (110, 200, 80), (90, 180, 70), park), mk(dog), "WHO SAYS WOOF?", "DOGGY!", (255, 200, 120)),
    (9.3, 13.2, cosy((180, 150, 255), (220, 200, 255)), mk(cat), "WHO SAYS MEOW?", "KITTY!", (255, 170, 70)),
]
REVEAL = 1.6
intro_bg = vgrad((255, 160, 210), (255, 225, 150))
qm = word_layers("?", 300, (255, 255, 255))[0][0]
q_words = [word_layers(s[4], 96, (255, 255, 255)) for s in SC]
a_words = [word_layers(s[5], 170, s[6]) for s in SC]
hook1 = word_layers("GUESS THE", 120, (255, 255, 255)); hook2 = word_layers("ANIMAL!", 160, (255, 230, 70))
badge = word_layers("#2", 90, (255, 255, 255), stroke=(230, 60, 120))
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("GREAT JOB!", 130, (255, 255, 255))
peek = [s[3][2] for s in SC]
mini = [s[3][0].resize((300, 300)) for s in SC]

def rays(base, t, col=(255, 255, 255, 50)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, 900), (CX + 2000 * math.cos(a0), 900 + 2000 * math.sin(a0)), (CX + 2000 * math.cos(a0 + .22), 900 + 2000 * math.sin(a0 + .22))], fill=col)

def frame(t):
    if t < 1.5:  # hook: motion + faces + question from the very first frame
        base = intro_bg.copy(); rays(base, t)
        for i, x in enumerate((220, 490, 760)):
            bob = 30 * math.sin(t * 8 + i * 1.7)
            paste_scaled(base, peek[i].resize((300, 300)), x, 1150 + bob, 1.0, 6 * math.sin(t * 6 + i))
            paste_scaled(base, qm, x, 1150 + bob, 0.45)
        draw_words(base, hook1, CX, 480, t + 0.35, 0.08)
        draw_words(base, hook2, CX, 680, t + 0.2, 0.08)
        draw_words(base, badge, CX, 860, t - 0.3)
        return base
    if t >= 13.2:
        lt = t - 13.2
        base = intro_bg.copy(); rays(base, t, (255, 255, 255, 60)); d = ImageDraw.Draw(base)
        for i, (x, y) in enumerate([(160, 300), (840, 360), (140, 1420), (850, 1380), (300, 930), (720, 980)]):
            s = ease_pop((lt - i * .06) / .4)
            if s > 0: star(d, x, y + 10 * math.sin(t * 8 + i), 60 * s, [(255, 230, 70), (255, 255, 255), (130, 220, 255)][i % 3])
        for i, x in enumerate((220, 490, 760)):
            yo, sx, sy = drop_land(lt - i * .1, 0.3, 500)
            if lt - i * .1 > 0: paste_scaled(base, mini[i], x, 1440 + yo + 8 * math.sin(t * 9 + i), 1, 0, sx, sy, True)
        draw_words(base, end1, CX, 600, lt)
        draw_words(base, end2, CX, 840, lt - 0.2)
        return base
    for i, (st, en, bg, (op, cl, sil), *_r) in enumerate(SC):
        if st <= t < en:
            lt = t - st; base = bg.copy()
            yo, sx, sy = drop_land(lt, 0.3, 800)
            wig = 3 * math.sin(lt * 6)
            ground_shadow(base, CX, CY - 25, CH * 0.7 * (0.6 + 0.4 * min(1, lt / 0.3)))
            if lt < REVEAL:
                paste_scaled(base, sil, CX, CY + yo, 1, wig, sx, sy, True)
                paste_scaled(base, qm, CX, 1040 + 15 * math.sin(lt * 9), ease_pop((lt - .3) / .4) * .8, 8 * math.sin(lt * 5))
                draw_words(base, q_words[i], CX, 330, lt)
            else:
                rt = lt - REVEAL
                sp = cl if blinking(rt, i) and rt > 0.5 else op
                s = 1 + 0.15 * math.exp(-rt * 6) * math.sin(rt * 25)
                paste_scaled(base, sp, CX, CY, s, wig, 1, 1, True)
                d = ImageDraw.Draw(base); burst(d, CX, 1080, rt)
                draw_words(base, a_words[i], CX, 400, rt)
                if rt < 0.12: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(180 * (1 - rt / .12)))))
                base = shake(base, 0, rt)
            return base

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
notes = [67, 72, 76, 72, 74, 77, 74, 71, 67, 72, 76, 79, 77, 74, 72, None]
mix += 0.075 * synth_music(notes, 60 / 126 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.7, 1.4, 2.0, 2.6, 3.4, 4.5, 6.0, 7.5, 10.0, 11.5, 13.6, 14.5, 14.9, 8.4, 12.4], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
