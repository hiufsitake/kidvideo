"""Baby Animals #1 — mommy dog -> puppy, mommy cat -> kitten, mommy hen -> chick (2026-10-29).
Reuses the channel's dog/cat/hen characters (as a recurring cast) from shorts 03/07 via AST import;
new chick character; heart 'hug' micro-beat; drifting parallax clouds."""
import sys, ast, math, numpy as np
sys.path.insert(0, "/home/claude/kidvideo/pipeline")
from common import *
from PIL import Image, ImageDraw

OUT = "/home/claude/s10"; SLUG = "baby-animals-1-short10"
P = "/home/claude/kidvideo/pipeline/"
def borrow(path, names):
    tree = ast.parse(open(path).read())
    mod = ast.Module([n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], [])
    exec(compile(mod, path, "exec"), globals())
borrow(P + "short03_guess_the_animal_2.py", {"flowers", "hills_bg", "cosy", "dog", "cat"})
borrow(P + "short07_guess_the_animal_3.py", {"poly", "hen"})

MCH, BCH, GY = 680, 400, 1450   # mommy size, baby size, ground line
MX, BX = 300, 745

def doghouse(d):
    d.polygon([(40, 1150), (160, 1040), (280, 1150)], fill=(255, 120, 60))
    d.rectangle((55, 1150, 265, 1360), fill=(250, 210, 90))
    d.ellipse((110, 1220, 210, 1360), fill=(60, 50, 70)); d.rectangle((110, 1280, 210, 1360), fill=(60, 50, 70))
    for x in (860, 990):
        d.ellipse((x - 70, 980, x + 70, 1120), fill=(70, 170, 90)); d.rectangle((x - 12, 1100, x + 12, 1360), fill=(130, 85, 50))

def coop(d):
    d.polygon([(830, 1080), (960, 960), (1090, 1080)], fill=(170, 60, 60))
    d.rectangle((850, 1080, 1070, 1360), fill=(240, 180, 110))
    d.rounded_rectangle((920, 1200, 1000, 1360), 30, fill=(110, 70, 40))
    for x in range(0, 300, 60): d.rounded_rectangle((x, 1240, x + 26, 1380), 8, fill=(255, 250, 240), outline=(170, 160, 150), width=4)
    d.rectangle((0, 1270, 300, 1290), fill=(255, 250, 240)); d.rectangle((0, 1330, 300, 1350), fill=(255, 250, 240))
    rng = np.random.default_rng(4)
    for _ in range(40):
        x, y = rng.integers(0, W), rng.integers(1460, H)
        d.ellipse((x - 7, y - 4, x + 7, y + 4), fill=(240, 200, 90))

def chick(closed=False):
    im, d = canvas()
    Y, Y2, O = (255, 220, 60, 255), (255, 240, 150, 255), (255, 150, 40, 255)
    for sx in (-1, 1):
        x = 450 + sx * 90
        d.line(S((x, 760, x, 850)), fill=O, width=16 * SS)
        for dx in (-34, 0, 34): d.line(S((x, 850, x + dx, 868)), fill=O, width=12 * SS)
    for cx, cy in [(430, 80), (470, 70), (450, 95)]:  # fluffy tuft
        E(d, (cx - 30, cy - 50, cx + 30, cy + 50), Y, 7)
    E(d, (170, 110, 730, 800), Y)
    E(d, (300, 450, 600, 770), Y2, 0)
    for sx in (-1, 1):  # little wings
        x = 450 + sx * 270
        E(d, (x - 70, 420, x + 70, 600), (250, 200, 40, 255))
    eyes(d, 450, 330, 110, 56, closed)
    cheeks(d, 450, 440, 170)
    poly(d, [(400, 410), (500, 410), (450, 475)], O, 7)
    return im

def mk(fn, size):
    o = finish(fn(False), size); c = finish(fn(True), size)
    return o, c, silhouette(o)

CLOUDS = [(220, 330, 0.9), (780, 480, 0.75), (520, 230, 0.55)]
SC = [  # start, end, bg, mommy, baby, mommy caption, answer, colour
    (1.5, 5.4, hills_bg((110, 215, 225), (210, 245, 240), (130, 210, 95), (105, 190, 80), doghouse), mk(dog, MCH), mk(dog, BCH), "MOMMY DOG'S", "PUPPY!", (255, 200, 120)),
    (5.4, 9.3, cosy((150, 220, 180), (215, 245, 220)), mk(cat, MCH), mk(cat, BCH), "MOMMY CAT'S", "KITTEN!", (255, 170, 70)),
    (9.3, 13.2, hills_bg((255, 185, 150), (255, 235, 205), (150, 205, 90), (125, 190, 80), coop), mk(hen, MCH), mk(chick, BCH), "MOMMY HEN'S", "CHICK!", (255, 225, 60)),
]
REVEAL = 1.8; HUG = 2.75
qa = [word_layers(s[5], 100, (255, 255, 255)) for s in SC]
qb = word_layers("BABY IS...?", 100, (255, 230, 90))
ans = [word_layers(s[6], 165, s[7]) for s in SC]
qm = word_layers("?", 260, (255, 255, 255))[0][0]
hook1 = word_layers("WHO'S THE", 130, (255, 255, 255)); hook2 = word_layers("BABY?", 200, (255, 230, 70))
badge = word_layers("BABY ANIMALS #1", 70, (255, 255, 255), stroke=(220, 70, 130))
end1 = word_layers("YAY!", 230, (255, 230, 70)); end2 = word_layers("GREAT JOB!", 130, (255, 255, 255))
intro_bg = vgrad((140, 200, 255), (255, 200, 225))
peek = [s[4][2] for s in SC]
mini_m = [s[3][0].resize((230, 230)) for s in SC]; mini_b = [s[4][0].resize((140, 140)) for s in SC]

def heart_img(sz=160, col=(255, 90, 130, 255)):
    im, d = canvas(200)
    E(d, (20, 30, 110, 120), col, 0); E(d, (90, 30, 180, 120), col, 0)
    d.polygon([(v * SS) for v in (24, 95, 176, 95, 100, 185)], fill=col)
    d.ellipse(S((45, 50, 75, 75)), fill=(255, 255, 255, 170))
    return im.resize((sz, sz), Image.LANCZOS)
HEART = heart_img()

def rays(base, t, col=(255, 255, 255, 55)):
    d = ImageDraw.Draw(base, "RGBA")
    for i in range(12):
        a0 = t * 0.6 + i * math.pi / 6
        d.polygon([(CX, 1000), (CX + 2000 * math.cos(a0), 1000 + 2000 * math.sin(a0)), (CX + 2000 * math.cos(a0 + .22), 1000 + 2000 * math.sin(a0 + .22))], fill=col)

def hook(t):
    base = intro_bg.copy(); rays(base, t)
    for i, x in enumerate((215, 490, 765)):
        bob = 34 * math.sin(t * 8 + i * 1.9)
        paste_scaled(base, peek[i], x, 1200 + bob, 0.9, 6 * math.sin(t * 6 + i))
        paste_scaled(base, qm, x, 1200 + bob, 0.45)
    draw_words(base, hook1, CX, 480, t + 0.5, 0.08)
    draw_words(base, hook2, CX, 700, t + 0.5, 0.08)
    draw_words(base, badge, CX, 1420, t + 0.4, 0.05)
    return base

def ending(lt, t):
    base = intro_bg.copy(); rays(base, t, (255, 255, 255, 60)); d = ImageDraw.Draw(base)
    confetti(d, lt)
    for i, x in enumerate((215, 490, 765)):
        yo, sx, sy = drop_land(lt - i * .1, 0.3, 500)
        if lt - i * .1 > 0:
            paste_scaled(base, mini_m[i], x - 30, 1330 + yo, 1, 0, sx, sy, True)
            paste_scaled(base, mini_b[i], x + 75, 1330 + yo - 10 * abs(math.sin(t * 7 + i)), 1, 0, sx, sy, True)
    draw_words(base, end1, CX, 500, lt)
    draw_words(base, end2, CX, 720, lt - 0.2)
    return base

def scene(i, lt, t):
    st, en, bg, (mo, mc, _ms), (bo, bc, bs), *_r = SC[i]
    base = bg.copy(); drift_clouds(base, t, CLOUDS)
    yo, sx, sy = drop_land(lt, 0.3, 500)
    ground_shadow(base, MX, GY - 20, MCH * 0.62); ground_shadow(base, BX, GY - 12, BCH * 0.62)
    msp = mc if blinking(lt, i) else mo
    paste_scaled(base, msp, MX, GY + yo, 1, 2 * math.sin(lt * 5), sx, sy, True)
    if lt < REVEAL:
        paste_scaled(base, bs, BX, GY - 20 * abs(math.sin(lt * 6)), 1, 4 * math.sin(lt * 6), 1, 1, True)
        paste_scaled(base, qm, BX, GY - BCH * 0.5, ease_pop((lt - .4) / .4) * .45)
        draw_words(base, qa[i], CX, 300, lt)
        draw_words(base, qb, CX, 440, lt - 0.3)
        return base
    rt = lt - REVEAL
    hop = 0
    if lt >= HUG: hop = 70 * max(0, math.sin(min(math.pi, (lt - HUG) * 7)))  # happy hop on the hug beat
    bsp = bc if blinking(rt, i + 2) and rt > 0.5 else bo
    s = 1 + 0.18 * math.exp(-rt * 6) * math.sin(rt * 25)
    paste_scaled(base, bsp, BX, GY - hop, s, 4 * math.sin(lt * 7), 1, 1, True)
    d = ImageDraw.Draw(base); burst(d, BX, GY - BCH * 0.5, rt, rad=200)
    draw_words(base, ans[i], CX, 380, rt)
    if lt >= HUG:  # heart floats up between mommy and baby
        k = lt - HUG
        paste_scaled(base, HEART, (MX + BX) / 2 + 20, 1000 - 120 * ease_out(k / 1.0), ease_pop(k / .35) * (1 + 0.08 * math.sin(k * 10)))
    if rt < 0.12: base.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(160 * (1 - rt / .12)))))
    base = shake(base, 0, rt, 10)
    return camera(base, zoom_curve(rt, 1.06), BX - 60, GY - 200)

def raw(t):
    if t < 1.5: return hook(t)
    if t >= 13.2: return ending(t - 13.2, t)
    for i, s in enumerate(SC):
        if s[0] <= t < s[1]: return scene(i, t - s[0], t)

def frame(t): return with_transitions(raw, [1.5, 5.4, 9.3, 13.2], t)

# ---------- audio ----------
def sfx_heart(n=0.4):
    tt = np.arange(int(SR * n)) / SR
    return (np.sin(2 * np.pi * 880 * tt) * (tt < .12) + np.sin(2 * np.pi * 1175 * tt) * (tt >= .12)) * np.exp(-tt * 8) * 0.2

mix = np.zeros(int(SR * DUR) + SR, np.float32)
place(mix, load(f"{OUT}/l0.wav"), 0.1)
for k, (st, *_r) in enumerate(SC):
    place(mix, load(f"{OUT}/l{1 + 2 * k}.wav"), st + 0.15)
    place(mix, load(f"{OUT}/l{2 + 2 * k}.wav"), st + REVEAL + 0.05)
    place(mix, sfx_boing(), st + 0.28); place(mix, sfx_sparkle(), st + REVEAL); place(mix, sfx_heart(), st + HUG)
place(mix, load(f"{OUT}/l7.wav"), 13.25)
for i in range(3): place(mix, sfx_pop(), 13.45 + i * .1)
place(mix, sfx_ding(), 13.25)
notes = [72, 76, 79, 76, 77, 74, 71, None, 74, 77, 79, 77, 76, 72, 67, None]
mix += 0.07 * synth_music(notes, 60 / 116 / 2)

if __name__ == "__main__":
    contact_sheet(frame, [0.0, 0.8, 1.6, 2.6, 3.4, 4.4, 5.0, 5.7, 7.4, 8.3, 9.6, 11.3, 12.2, 13.5, 14.2, 14.97], f"{OUT}/sheet.png")
    if "--sheet" not in sys.argv:
        render(frame, mix, f"/home/claude/kidvideo/shorts/{SLUG}.mp4", OUT); print("rendered")
