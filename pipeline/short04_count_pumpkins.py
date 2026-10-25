"""Count the Pumpkins 1-5 — gentle, smiley autumn counting Short (no scary Halloween content)."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s04"; SLUG = "count-the-pumpkins-short04"
PS = 320  # pumpkin sprite size
SLOTS = [(225, 1150), (490, 1150), (755, 1150), (357, 1480), (623, 1480)]  # bottom-anchored feet points
T0, STEP = 1.7, 2.15  # number k appears at T0 + (k-1)*STEP; last at 10.3
TEND = 12.6
NUMS = ["ONE", "TWO", "THREE", "FOUR", "FIVE"]
NCOL = [(255, 90, 90), (255, 170, 40), (90, 200, 90), (70, 160, 255), (190, 110, 255)]

def bg():
    img = vgrad((120, 205, 255), (255, 225, 170)); d = ImageDraw.Draw(img, "RGBA")
    for r, a in [(240, 40), (180, 70), (130, 255)]:
        d.ellipse((900 - r, 230 - r, 900 + r, 230 + r), fill=(255, 225, 110, a))
    for cx, cy, s in [(180, 300, 1.0), (620, 560, 0.75)]:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 230))
    # autumn trees
    for x, c in [(70, (255, 150, 50)), (1010, (230, 90, 60))]:
        d.rectangle((x - 18, 760, x + 18, 1000), fill=(130, 85, 50))
        for dx, dy, r in [(-60, 0, 80), (60, 0, 80), (0, -70, 95), (0, 40, 85)]:
            d.ellipse((x + dx - r, 700 + dy - r, x + dx + r, 700 + dy + r), fill=c)
    d.ellipse((-400, 880, 900, 1900), fill=(150, 200, 90)); d.ellipse((300, 920, 1600, 1900), fill=(140, 190, 80))
    d.rectangle((0, 1150, W, H), fill=(165, 120, 75))
    for y in range(1180, H, 90):  # soil rows
        d.ellipse((-100, y, W + 100, y + 60), fill=(145, 100, 60))
    # vines + leaves
    for y in (1120, 1470):
        d.line([(x, y + 25 * math.sin(x / 60)) for x in range(0, W, 10)], fill=(70, 150, 60), width=10)
        for x in range(40, W, 160):
            yy = y + 25 * math.sin(x / 60)
            d.ellipse((x - 30, yy - 50, x + 30, yy), fill=(90, 175, 70))
    # little fence at the back
    for x in range(0, W, 90): d.rounded_rectangle((x + 15, 980, x + 45, 1130), 10, fill=(240, 220, 190))
    d.rectangle((0, 1020, W, 1040), fill=(225, 200, 165)); d.rectangle((0, 1080, W, 1100), fill=(225, 200, 165))
    return img

def pumpkin(face=0, closed=False, hue=(255, 140, 30)):
    im, d = canvas(600)
    dark = tuple(int(c * .82) for c in hue) + (255,)
    d.rounded_rectangle(S((280, 40, 320, 150)), 14 * SS, fill=(90, 140, 50, 255), outline=OL, width=8 * SS)  # stem
    d.ellipse(S((310, 70, 420, 130)), fill=(110, 190, 70, 255), outline=OL, width=7 * SS)  # leaf
    for box in [(60, 150, 330, 560), (270, 150, 540, 560), (150, 130, 450, 570)]:
        E(d, box, hue + (255,), 10)
    for x in (200, 400):
        d.arc(S((x - 70, 160, x + 70, 560)), 250, 290, fill=dark, width=8 * SS)
        d.arc(S((x - 70, 160, x + 70, 560)), 70, 110, fill=dark, width=8 * SS)
    eyes(d, 300, 320, 75, 40, closed)
    cheeks(d, 300, 400, 125)
    if face == 0: smile(d, 300, 420, 50)
    elif face == 1:
        d.chord(S((245, 400, 355, 490)), 0, 180, fill=(120, 30, 40, 255), outline=OL, width=8 * SS)
        d.ellipse(S((280, 445, 320, 480)), fill=(255, 120, 140, 255))
    else:
        d.ellipse(S((275, 410, 325, 465)), fill=(120, 30, 40, 255), outline=OL, width=8 * SS)
    return im

HUES = [(255, 140, 30), (255, 165, 40), (250, 125, 25), (255, 155, 50), (255, 135, 35)]
pk = [(finish(pumpkin(i % 3, False, HUES[i]), PS), finish(pumpkin(i % 3, True, HUES[i]), PS)) for i in range(5)]
big = finish(pumpkin(1, False), 520); bigc = finish(pumpkin(1, True), 520)
BG = bg()
hook = word_layers("LET'S COUNT", 120, (255, 255, 255)); hook2 = word_layers("PUMPKINS!", 150, (255, 200, 60))
digits = [word_layers(str(k + 1), 330, NCOL[k])[0][0] for k in range(5)]
words = [word_layers(NUMS[k] + "!", 120, (255, 255, 255), stroke=INK) for k in range(5)]
end1 = word_layers("5 HAPPY", 130, (255, 255, 255)); end2 = word_layers("PUMPKINS!", 150, (255, 200, 60)); end3 = word_layers("YAY!", 200, (255, 230, 70))

def frame(t):
    base = BG.copy()
    if t < T0:  # hook: big bouncing pumpkin + question from frame 0
        yo, sx, sy = drop_land(t + 0.15, 0.3, 500)
        sp = bigc if blinking(t, 2) and t > 0.6 else big
        ground_shadow(base, CX, 1395, 380)
        paste_scaled(base, sp, CX, 1420 + yo, 1, 3 * math.sin(t * 7), sx, sy, True)
        draw_words(base, hook, CX, 420, t + 0.3, 0.1)
        draw_words(base, hook2, CX, 600, t, 0.1)
        return base
    d = ImageDraw.Draw(base)
    n = min(5, int((t - T0) // STEP) + 1)
    lt_n = t - (T0 + (n - 1) * STEP)
    for k in range(n):
        lt = t - (T0 + k * STEP)
        x, y = SLOTS[k]
        yo, sx, sy = drop_land(lt, 0.3, 900)
        if t >= TEND: yo += -40 * abs(math.sin((t - TEND) * 6 + k))
        ground_shadow(base, x, y - 12, PS * .75 * (0.5 + 0.5 * min(1, lt / .3)), 60)
        sp = pk[k][1] if blinking(lt, k) and lt > 0.6 else pk[k][0]
        paste_scaled(base, sp, x, y + 10 + yo, 1, 3 * math.sin(lt * 5 + k), sx, sy, True)
    if t < TEND:
        x, y = SLOTS[n - 1]
        burst(d, x, y - 140, lt_n - 0.3, 8, 190)
        # number badge pops + word
        paste_scaled(base, digits[n - 1], CX, 420, ease_pop((lt_n - 0.25) / .4), 6 * math.sin(lt_n * 5))
        draw_words(base, words[n - 1], CX, 660, lt_n - 0.35)
        base = shake(base, 0.3, lt_n, 10)
    else:
        lt = t - TEND
        for i, (x, y) in enumerate([(150, 260), (830, 300), (120, 820), (860, 780), (490, 210)]):
            s = ease_pop((lt - i * .07) / .4)
            if s > 0: star(d, x, y + 10 * math.sin(t * 8 + i), 55 * s, [(255, 230, 70), (255, 255, 255), (130, 220, 255)][i % 3])
        draw_words(base, end1, CX, 330, lt)
        draw_words(base, end2, CX, 500, lt - 0.15)
        draw_words(base, end3, CX, 700, lt - 0.9)
    return base

# ---------- audio ----------
mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.1)
for k in range(5):
    at = T0 + k * STEP
    place(mix, sfx_boing(), at + 0.28)
    place(mix, sfx_ding(), at + 0.3)
    place(mix, load(f"{OUT}/n{k + 1}.wav"), at + 0.35)
place(mix, load(f"{OUT}/l6.wav"), TEND + 0.1)
for i in range(4): place(mix, sfx_pop(), TEND + 0.2 + i * .12)
place(mix, sfx_sparkle(), TEND + 0.9)
notes = [72, None, 74, 76, 79, None, 76, 74, 72, None, 76, 79, 81, 79, 76, None]
mix += 0.075 * synth_music(notes, 60 / 132 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.6, 1.4, 2.3, 3.0, 4.6, 6.7, 8.8, 10.4, 10.9, 12.2, 12.8, 13.4, 14.0, 14.6, 14.95], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
