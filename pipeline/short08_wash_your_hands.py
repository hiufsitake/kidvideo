"""Wash Your Hands! — healthy habit in 5 steps: water, soap, scrub, rinse, dry. Seamless loop ending (2026-10-28)."""
import sys, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s08"; SLUG = "wash-your-hands-short08"
HY = 1040          # hand centre y
COUNTER = 1330     # counter top y
HS = 440           # hand sprite size
K = HS / 360       # offset scale for germs/bubbles

def poly(d, pts, fill, w=10): d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill, outline=OL, width=w * SS)

# ---------- background: bathroom wall (tint per step) + sink ----------
def bathroom(top, bot, tile):
    img = vgrad(top, bot); d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, COUNTER, 120): d.line((0, y, W, y), fill=tile, width=5)
    for x in range(0, W, 120): d.line((x, 0, x, COUNTER), fill=tile, width=5)
    # little shelf with a toothbrush cup (decor, left edge)
    d.rounded_rectangle((-20, 860, 150, 885), 8, fill=(255, 255, 255), outline=(150, 150, 170), width=4)
    d.rounded_rectangle((40, 770, 110, 860), 12, fill=(120, 200, 255), outline=(60, 110, 160), width=5)
    d.line((60, 770, 50, 700), fill=(255, 120, 150), width=10); d.line((90, 770, 100, 710), fill=(120, 220, 120), width=10)
    # counter + basin
    d.rectangle((0, COUNTER, W, H), fill=(250, 250, 252)); d.rectangle((0, COUNTER + 70, W, COUNTER + 90), fill=(120, 190, 240))
    d.ellipse((CX - 300, COUNTER - 30, CX + 300, COUNTER + 60), fill=(205, 225, 240), outline=(150, 170, 190), width=6)
    d.ellipse((CX - 30, COUNTER + 5, CX + 30, COUNTER + 30), fill=(150, 160, 175))
    # cabinet under the counter
    d.rectangle((0, COUNTER + 90, W, H), fill=(175, 215, 250))
    for x0 in (CX - 330, CX + 10):
        d.rounded_rectangle((x0, COUNTER + 120, x0 + 320, H + 40), 24, outline=(120, 170, 220), width=8)
        d.ellipse((x0 + (290 if x0 < CX else 10), COUNTER + 200, x0 + (310 if x0 < CX else 30), COUNTER + 220), fill=(255, 210, 90))
    # tall tap between the hands
    d.rounded_rectangle((CX - 34, 790, CX + 34, COUNTER - 10), 16, fill=(200, 210, 225), outline=(110, 120, 140), width=6)
    d.rounded_rectangle((CX - 70, 800, CX + 70, 870), 30, fill=(205, 215, 230), outline=(110, 120, 140), width=6)
    d.ellipse((CX - 45, 730, CX + 45, 800), fill=(255, 120, 120), outline=(150, 60, 60), width=6)  # handle
    return img

TAP_X, TAP_Y = CX, 865  # spout mouth

# ---------- characters ----------
SKIN, SKIN2 = (250, 205, 165, 255), (235, 175, 135, 255)

def hand():
    """Palm facing viewer, fingers up, thumb on the right (this is the viewer-left hand)."""
    im, d = canvas(600)
    d.rounded_rectangle(S((175, 500, 425, 600)), 30 * SS, fill=(90, 160, 240, 255), outline=OL, width=9 * SS)  # sleeve
    for k in range(3): d.line(S((200 + k * 0, 530 + k * 22, 400, 530 + k * 22)), fill=(140, 195, 250, 255), width=6 * SS)
    for x, top in [(185, 110), (255, 70), (325, 85), (395, 140)]:
        d.rounded_rectangle(S((x - 33, top, x + 33, 340)), 33 * SS, fill=SKIN, outline=OL, width=9 * SS)
    E(d, (365, 270, 520, 380), SKIN, 9)  # thumb
    d.rounded_rectangle(S((150, 240, 440, 520)), 110 * SS, fill=SKIN, outline=OL, width=9 * SS)
    for x, top in [(185, 110), (255, 70), (325, 85), (395, 140)]:  # redraw finger tops over palm edge
        d.rounded_rectangle(S((x - 24, top + 9, x + 24, 280)), 24 * SS, fill=SKIN)
    d.arc(S((215, 330, 385, 450)), 200, 340, fill=SKIN2, width=8 * SS)  # palm crease
    return im

def soap(closed=False):
    im, d = canvas(400)
    d.rounded_rectangle(S((40, 150, 360, 330)), 60 * SS, fill=(255, 140, 190, 255), outline=OL, width=10 * SS)
    d.rounded_rectangle(S((80, 175, 200, 210)), 18 * SS, fill=(255, 200, 225, 255))
    eyes(d, 200, 240, 55, 26, closed)
    smile(d, 200, 280, 30, 8)
    for cx, cy, r in [(100, 120, 34), (160, 85, 24), (300, 110, 40), (250, 60, 20)]:
        E(d, (cx - r, cy - r, cx + r, cy + r), (230, 245, 255, 255), 6)
        d.ellipse(S((cx - r * .5, cy - r * .6, cx - r * .1, cy - r * .2)), fill=(255, 255, 255, 255))
    return im

def germ(closed=False):
    im, d = canvas(200)
    for k in range(8):
        a = k * math.pi / 4
        E(d, (100 + 70 * math.cos(a) - 18, 100 + 70 * math.sin(a) - 18, 100 + 70 * math.cos(a) + 18, 100 + 70 * math.sin(a) + 18), (150, 220, 90, 255), 6)
    E(d, (35, 35, 165, 165), (150, 220, 90, 255), 8)
    eyes(d, 100, 92, 24, 15, closed)
    d.arc(S((80, 110, 120, 140)), 20, 160, fill=OL, width=5 * SS)
    return im

HL = finish(hand(), HS); HR = HL.transpose(Image.FLIP_LEFT_RIGHT)
SOAP = finish(soap(), 165); SOAPC = finish(soap(True), 165)
GERM = finish(germ(), 80)
GERMS = [(-1, -40, -40), (-1, 50, 20), (1, -30, 10), (1, 40, -50), (-1, 0, 90), (1, 10, 90)]  # (hand, dx, dy)
BUBS = [(-1, -60, -10, 34), (-1, 30, -60, 26), (-1, 50, 60, 30), (-1, -20, 110, 24), (-1, -80, 70, 20),
        (1, 60, -10, 34), (1, -30, -60, 26), (1, -50, 60, 30), (1, 20, 110, 24), (1, 80, 70, 20), (-1, 10, 10, 22), (1, -10, 20, 22)]

def bubble(d, x, y, r):
    if r < 2: return
    d.ellipse((x - r, y - r, x + r, y + r), fill=(235, 248, 255, 225), outline=(140, 190, 230), width=4)
    d.ellipse((x - r * .55, y - r * .6, x - r * .1, y - r * .2), fill=(255, 255, 255))

# ---------- scenes ----------
STEPS = [  # start, end, wall top, wall bottom, tile, number colour, caption, caption colour
    (1.6, 3.9, (150, 215, 255), (205, 238, 255), (130, 195, 240), (40, 130, 230), "WATER ON!", (120, 210, 255)),
    (3.9, 6.2, (255, 190, 220), (255, 228, 240), (245, 170, 205), (230, 70, 140), "ADD SOAP!", (255, 140, 200)),
    (6.2, 8.9, (205, 180, 255), (232, 220, 255), (190, 165, 245), (130, 80, 220), "SCRUB SCRUB!", (200, 160, 255)),
    (8.9, 11.2, (150, 235, 215), (215, 250, 240), (125, 215, 195), (20, 160, 130), "RINSE!", (110, 230, 200)),
    (11.2, 13.3, (255, 225, 140), (255, 245, 205), (245, 210, 120), (230, 150, 20), "DRY!", (255, 215, 80)),
]
BG = [bathroom(s[2], s[3], s[4]) for s in STEPS]
HOOK_BG = bathroom((120, 215, 240), (200, 245, 220), (105, 200, 225))
CAP = [word_layers(s[6], 140, s[7]) for s in STEPS]
NUM = [word_layers(str(i + 1), 120, (255, 255, 255), stroke=INK) for i in range(5)]
hook1 = word_layers("LET'S WASH", 130, (255, 255, 255)); hook2 = word_layers("OUR HANDS!", 140, (255, 230, 70))
end1 = word_layers("YAY!", 220, (255, 230, 70)); end2 = word_layers("CLEAN HANDS!", 120, (255, 255, 255))
T_END = 13.3

def hands(base, lx, ly, rx, ry, rot=0):
    paste_scaled(base, HL, lx, ly, 1, rot)
    paste_scaled(base, HR, rx, ry, 1, -rot)

def idle_pos(t):
    b = 12 * math.sin(t * 5)
    return CX - 200, HY + b, CX + 200, HY - b

def water(d, t, amt=1.0):
    if amt <= 0: return
    wob = 6 * math.sin(t * 30)
    d.rounded_rectangle((TAP_X - 22 * amt + wob * .3, TAP_Y, TAP_X + 22 * amt + wob * .3, COUNTER), 20, fill=(110, 190, 255, 210))
    d.line((TAP_X - 6 + wob, TAP_Y + 10, TAP_X - 6 - wob, COUNTER - 10), fill=(220, 245, 255, 220), width=6)
    rng = np.random.default_rng(int(t * 30))
    for _ in range(int(8 * amt)):  # splash drops at the basin
        x, y = TAP_X + rng.uniform(-110, 110), COUNTER - rng.uniform(5, 70)
        d.ellipse((x - 9, y - 12, x + 9, y + 12), fill=(140, 205, 255, 230))

def germs(base, pos, popped_t=None, lt=0):
    lx, ly, rx, ry = pos
    for k, (h, dx, dy) in enumerate(GERMS):
        x, y = (lx if h < 0 else rx) + dx * K, (ly if h < 0 else ry) + dy * K
        if popped_t is not None:
            pt = popped_t + k * 0.25
            if lt >= pt:
                burst(ImageDraw.Draw(base), x, y, lt - pt, n=6, rad=80)
                continue
        paste_scaled(base, GERM, x, y + 4 * math.sin(lt * 9 + k), 1)

def bubbles(base, pos, amt, t, drift=0):
    d = ImageDraw.Draw(base)
    lx, ly, rx, ry = pos
    for k, (h, dx, dy, r) in enumerate(BUBS):
        x, y = (lx if h < 0 else rx) + dx * K, (ly if h < 0 else ry) + dy * K + drift * (1 + k % 3)
        bubble(d, x, y + 3 * math.sin(t * 7 + k), r * amt * (1 + 0.08 * math.sin(t * 9 + k)))

def caption(base, i, lt):
    d = ImageDraw.Draw(base)
    s = ease_pop(lt / 0.35)
    if s > 0:
        r = 85 * s
        d.ellipse((CX - r, 300 - r, CX + r, 300 + r), fill=STEPS[i][5], outline=(255, 255, 255), width=10)
        draw_words(base, NUM[i], CX, 300, lt)
    draw_words(base, CAP[i], CX, 500, lt - 0.15, 0.1)

def soap_on_counter(base, t, drop_lt=None):
    yo, sx, sy = (0, 1, 1) if drop_lt is None else drop_land(drop_lt, 0.3, 900)
    sp = SOAPC if blinking(t, 2) else SOAP
    paste_scaled(base, sp, 850, COUNTER + 22 + yo, 1, 3 * math.sin(t * 4), sx, sy, True)

def hook(t):
    base = HOOK_BG.copy()
    soap_on_counter(base, t)
    pos = idle_pos(t)
    wave = 10 * math.sin(t * 9)
    paste_scaled(base, HL, pos[0], pos[1], 1, wave); paste_scaled(base, HR, pos[2], pos[3], 1, -wave)
    germs(base, pos, lt=t)
    d = ImageDraw.Draw(base)
    for k in range(6):  # floating bubbles from the first frame
        y = 1250 - ((t * 160 + k * 170) % 900); x = 150 + k * 130 + 25 * math.sin(t * 3 + k)
        bubble(d, x, y, 22 + 8 * (k % 3))
    draw_words(base, hook1, CX, 330, t + 0.5, 0.08)
    draw_words(base, hook2, CX, 510, t + 0.5, 0.08)
    return base

def step(i, lt, t):
    base = BG[i].copy(); d = ImageDraw.Draw(base, "RGBA")
    pos = idle_pos(t); zoom = 1.0
    if i == 0:
        soap_on_counter(base, t, None)
        water(d, t, ease_out(lt / 0.3)); hands(base, *pos); germs(base, pos, lt=t)
        for k in range(5):  # drops bouncing off the hands
            ph = (lt * 2 + k * .2) % 1; x = TAP_X + (k - 2) * 90 * ph
            d.ellipse((x - 10, HY - 60 * math.sin(ph * math.pi) - 12, x + 10, HY - 60 * math.sin(ph * math.pi) + 12), fill=(130, 200, 255, 220))
    elif i == 1:
        soap_on_counter(base, t, lt)
        hands(base, *pos); germs(base, pos, lt=t)
        bubbles(base, pos, min(1, max(0, (lt - 0.6) / 1.0)) * 0.7, t)
    elif i == 2:
        soap_on_counter(base, t)
        w = math.sin(lt * 14)
        pos = (CX - 140 + 50 * w, HY + 30 * w, CX + 140 - 50 * w, HY - 30 * w)
        hands(base, *pos, rot=4 * w)
        germs(base, pos, popped_t=0.7, lt=lt)
        bubbles(base, pos, 0.7 + 0.5 * min(1, lt / 1.2), t)
        for k in range(6):  # bubbles floating up
            y = HY - ((lt * 260 + k * 90) % 600); x = CX + (k - 2.5) * 120 + 20 * math.sin(lt * 4 + k)
            bubble(d, x, y, 18 + 6 * (k % 3))
        zoom = zoom_curve(lt, 1.06)
    elif i == 3:
        soap_on_counter(base, t)
        water(d, t); hands(base, *pos)
        amt = 1.2 * (1 - ease_out(lt / 1.6))
        bubbles(base, pos, amt, t, drift=60 * ease_out(lt / 1.6))
    else:
        soap_on_counter(base, t)
        hands(base, *pos)
        tx = CX + 230 * math.sin(lt * 5); ty = HY + 40
        if lt < 1.3:  # towel swiping across the hands
            tw = Image.new("RGBA", (440, 230), (0, 0, 0, 0)); td = ImageDraw.Draw(tw)
            td.rounded_rectangle((5, 5, 435, 225), 40, fill=(255, 210, 70), outline=OL, width=9)
            for y in (60, 165): td.rectangle((15, y, 425, y + 18), fill=(255, 140, 90))
            paste_scaled(base, tw, tx, ty, 1, 8 * math.sin(lt * 5))
        else:
            rt = lt - 1.3
            burst(ImageDraw.Draw(base), pos[0], HY - 40, rt, n=8, rad=170)
            burst(ImageDraw.Draw(base), pos[2], HY - 40, rt - 0.1, n=8, rad=170)
            zoom = zoom_curve(rt, 1.05)
    caption(base, i, lt)
    return camera(base, zoom, CX, HY)

def ending(lt, t):
    base = HOOK_BG.copy(); d = ImageDraw.Draw(base)
    soap_on_counter(base, t)
    wave = 14 * math.sin(t * 10)
    s = ease_pop(lt / 0.4)
    paste_scaled(base, HL, CX - 200, HY - 20, s, wave); paste_scaled(base, HR, CX + 200, HY - 20, s, -wave)
    for k, (x, y) in enumerate([(CX - 300, 900), (CX + 300, 880), (CX - 60, 820), (CX + 80, 1180)]):
        sc = ease_pop((lt - 0.2 - k * 0.1) / 0.4)
        if sc > 0: star(d, x, y + 10 * math.sin(t * 8 + k), 40 * sc, (255, 240, 120))
    confetti(d, lt)
    draw_words(base, end1, CX, 340, lt)
    draw_words(base, end2, CX, 560, lt - 0.2)
    return base

def raw(t):
    if t < STEPS[0][0]: return hook(t)
    if t >= T_END: return ending(t - T_END, t)
    for i, s in enumerate(STEPS):
        if s[0] <= t < s[1]: return step(i, t - s[0], t)

def frame(t): return with_transitions(raw, [s[0] for s in STEPS] + [T_END], t)

# ---------- audio ----------
def sfx_water(n):
    rng = np.random.default_rng(1); x = rng.standard_normal(int(SR * n)).astype(np.float32)
    k = np.ones(12, np.float32) / 12; x = np.convolve(x, k, "same")
    env = np.minimum(1, np.arange(len(x)) / (SR * .15)) * np.minimum(1, (len(x) - np.arange(len(x))) / (SR * .3))
    return x * env * 0.35

def sfx_swish(n=0.35):
    rng = np.random.default_rng(2); x = rng.standard_normal(int(SR * n)).astype(np.float32)
    t = np.arange(len(x)) / SR
    return np.convolve(x, np.ones(6) / 6, "same") * np.sin(np.pi * t / n) * 0.3

mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/h0.wav"), 0.08)
for i, key in enumerate(["h1", "h2", "h3", "h4", "h5"]):
    st = STEPS[i][0]
    place(mix, sfx_sparkle(), st, 0.7)
    place(mix, load(f"{OUT}/{key}.wav"), st + 0.12)
place(mix, sfx_water(2.2), STEPS[0][0] + 0.05, 0.6); place(mix, sfx_water(2.2), STEPS[3][0] + 0.05, 0.6)
place(mix, sfx_boing(), STEPS[1][0] + 0.28)
for k in range(6): place(mix, sfx_pop(), STEPS[1][0] + 0.7 + k * 0.17, 0.7)
for k in range(6): place(mix, sfx_pop(), STEPS[2][0] + 0.7 + k * 0.25, 0.9)
for k in range(3): place(mix, sfx_swish(), STEPS[4][0] + 0.15 + k * 0.4, 0.8)
place(mix, sfx_ding(), STEPS[4][0] + 1.3)
place(mix, load(f"{OUT}/h6.wav"), T_END + 0.1)
place(mix, sfx_ding(), T_END + 0.05); place(mix, sfx_sparkle(), T_END + 0.3)
notes = [72, 76, 79, 76, 77, 74, 71, 74, 72, 76, 79, 84, 81, 79, 76, None]
mix += 0.075 * synth_music(notes, 60 / 128 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.8, 1.7, 3.0, 4.1, 5.5, 6.4, 7.6, 8.6, 9.5, 10.8, 11.5, 12.8, 13.6, 14.4, 14.97], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
