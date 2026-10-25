import math, os, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
OUT = "/home/claude/short01"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SS = 2  # supersample for characters

def font(sz): return ImageFont.truetype(FONT, sz)

# ---------- backgrounds ----------
def background(sky_top, sky_bot, ground, ground2, extras):
    img = Image.new("RGB", (W, H))
    px = np.zeros((H, W, 3), np.float32)
    t = np.linspace(0, 1, H)[:, None]
    px[:] = (np.array(sky_top) * (1 - t) + np.array(sky_bot) * t)[:, None, :][:, 0, :][:, None, :]
    img = Image.fromarray(px.astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    # sun
    for r, a in [(260, 40), (200, 70), (150, 255)]:
        d.ellipse((800 - r, 260 - r, 800 + r, 260 + r), fill=(255, 236, 120, a))
    # clouds
    for cx, cy, s in [(220, 380, 1.0), (640, 560, 0.8), (930, 760, 0.6)]:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 235))
    # hills
    d.ellipse((-400, 1180, 900, 2300), fill=ground2)
    d.ellipse((300, 1250, 1600, 2300), fill=ground2)
    d.rectangle((0, 1450, W, H), fill=ground)
    d.ellipse((-300, 1350, 1400, 1700), fill=ground)
    extras(d)
    return img

def farm_extras(d):
    # barn
    d.polygon([(760, 1160), (900, 1060), (1040, 1160)], fill=(170, 40, 40))
    d.rectangle((775, 1160, 1025, 1330), fill=(200, 50, 50))
    d.rectangle((860, 1220, 940, 1330), fill=(250, 245, 235))
    d.line((860, 1220, 940, 1330), fill=(200, 50, 50), width=8)
    d.line((940, 1220, 860, 1330), fill=(200, 50, 50), width=8)
    flowers(d)

def pond_extras(d):
    d.ellipse((-150, 1500, 1230, 1880), fill=(70, 160, 230))
    d.ellipse((-80, 1530, 1160, 1840), fill=(110, 190, 245))
    for x, y in [(180, 1700), (820, 1640), (560, 1790)]:
        d.ellipse((x - 70, y - 28, x + 70, y + 28), fill=(60, 170, 80))
        d.ellipse((x - 18, y - 30, x + 18, y + 4), fill=(255, 170, 200))
    for x in [60, 110, 980, 1030]:
        d.rectangle((x, 1260, x + 10, 1520), fill=(70, 130, 50))
        d.rounded_rectangle((x - 10, 1230, x + 20, 1330), 15, fill=(140, 90, 50))

def yard_extras(d):
    for x in range(0, W, 120):
        d.rectangle((x + 20, 1240, x + 50, 1420), fill=(190, 140, 90))
    d.rectangle((0, 1280, W, 1305), fill=(170, 120, 75))
    d.rectangle((0, 1360, W, 1385), fill=(170, 120, 75))
    for x, y in [(90, 1330), (980, 1340)]:
        d.rounded_rectangle((x - 80, y - 60, x + 80, y + 70), 25, fill=(235, 200, 90))
    flowers(d)

def flowers(d):
    rng = np.random.default_rng(3)
    for _ in range(40):
        x, y = rng.integers(0, W), rng.integers(1480, H)
        c = [(255, 230, 80), (255, 140, 180), (255, 255, 255), (180, 140, 255)][rng.integers(0, 4)]
        for a in range(5):
            ang = a * 2 * math.pi / 5
            d.ellipse((x + 14 * math.cos(ang) - 10, y + 14 * math.sin(ang) - 10, x + 14 * math.cos(ang) + 10, y + 14 * math.sin(ang) + 10), fill=c)
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(255, 190, 40))

# ---------- characters (drawn on 900x900 canvas x SS) ----------
OL = (40, 30, 30, 255)

def canvas():
    im = Image.new("RGBA", (900 * SS, 900 * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def E(d, box, fill, ol=10):
    b = [v * SS for v in box]
    d.ellipse(b, fill=fill, outline=OL, width=ol * SS)

def eyes(d, cx, cy, gap=90, r=48):
    for sx in (-1, 1):
        x = cx + sx * gap
        E(d, (x - r, cy - r, x + r, cy + r), (255, 255, 255, 255), 8)
        E(d, (x - r * .62, cy - r * .55, x + r * .62, cy + r * .75), (30, 25, 35, 255), 0)
        d.ellipse([v * SS for v in (x - r * .35, cy - r * .4, x - r * .02, cy - r * .07)], fill=(255, 255, 255, 255))
        d.ellipse([v * SS for v in (x + r * .1, cy + r * .2, x + r * .28, cy + r * .38)], fill=(255, 255, 255, 255))

def smile(d, cx, cy, w=60):
    d.arc([v * SS for v in (cx - w, cy - w * .6, cx + w, cy + w * .7)], 20, 160, fill=OL, width=10 * SS)

def cheeks(d, cx, cy, gap=150):
    for sx in (-1, 1):
        d.ellipse([v * SS for v in (cx + sx * gap - 38, cy - 22, cx + sx * gap + 38, cy + 22)], fill=(255, 120, 150, 140))

def cow():
    im, d = canvas()
    for x in (300, 400, 520, 620):
        E(d, (x - 40, 640, x + 40, 840), (250, 250, 250, 255))
        E(d, (x - 44, 800, x + 44, 860), (60, 50, 50, 255))
    E(d, (220, 470, 700, 760), (250, 250, 250, 255))
    for box in [(300, 520, 410, 610), (540, 600, 650, 700), (460, 500, 540, 560)]:
        E(d, box, (45, 40, 45, 255), 0)
    E(d, (180, 150, 330, 240), (250, 250, 250, 255)); E(d, (570, 150, 720, 240), (250, 250, 250, 255))
    E(d, (205, 170, 300, 225), (255, 170, 185, 255), 0); E(d, (600, 170, 695, 225), (255, 170, 185, 255), 0)
    E(d, (330, 80, 380, 170), (240, 220, 170, 255), 8); E(d, (520, 80, 570, 170), (240, 220, 170, 255), 8)
    E(d, (270, 110, 630, 480), (250, 250, 250, 255))
    E(d, (290, 140, 400, 260), (45, 40, 45, 255), 0)
    eyes(d, 450, 270, 85, 46)
    E(d, (320, 340, 580, 480), (255, 175, 190, 255))
    E(d, (385, 385, 420, 420), (190, 90, 110, 255), 0); E(d, (480, 385, 515, 420), (190, 90, 110, 255), 0)
    smile(d, 450, 420, 45)
    return im

def duck():
    im, d = canvas()
    for x in (370, 530):
        d.polygon([(v[0] * SS, v[1] * SS) for v in [(x - 15, 720), (x + 15, 720), (x + 15, 800), (x - 15, 800)]], fill=(255, 140, 30, 255))
        E(d, (x - 70, 790, x + 70, 850), (255, 140, 30, 255))
    E(d, (220, 430, 700, 790), (255, 214, 50, 255))
    E(d, (500, 500, 680, 680), (255, 200, 40, 255), 8)
    E(d, (250, 120, 650, 500), (255, 220, 60, 255))
    d.polygon([(v[0] * SS, v[1] * SS) for v in [(420, 118), (450, 50), (470, 120)]], fill=(255, 220, 60, 255), outline=OL)
    eyes(d, 450, 270, 85, 46)
    cheeks(d, 450, 360, 140)
    E(d, (360, 330, 540, 430), (255, 145, 30, 255))
    d.line([v * SS for v in (375, 380, 525, 380)], fill=OL, width=6 * SS)
    return im

def pig():
    im, d = canvas()
    for x in (310, 410, 510, 610):
        E(d, (x - 40, 640, x + 40, 850), (255, 170, 185, 255))
        E(d, (x - 44, 810, x + 44, 860), (200, 110, 130, 255))
    E(d, (200, 460, 720, 770), (255, 180, 195, 255))
    d.arc([v * SS for v in (680, 520, 760, 600)], 180, 500, fill=OL, width=10 * SS)
    for sx in (-1, 1):
        cx = 450 + sx * 170
        d.polygon([(v[0] * SS, v[1] * SS) for v in [(cx - 70, 220), (cx + 70, 220), (cx + sx * 40, 90)]], fill=(255, 160, 180, 255), outline=OL, width=10 * SS)
    E(d, (250, 130, 650, 500), (255, 185, 200, 255))
    eyes(d, 450, 260, 90, 44)
    cheeks(d, 450, 360, 160)
    E(d, (360, 320, 540, 430), (255, 150, 170, 255))
    E(d, (400, 355, 435, 400), (170, 80, 100, 255), 0); E(d, (465, 355, 500, 400), (170, 80, 100, 255), 0)
    smile(d, 450, 430, 40)
    return im

def finish(im):
    im = im.resize((900, 900), Image.LANCZOS)
    a = im.split()[3]
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    shadow.putalpha(a.point(lambda v: int(v * 0.0)))
    return im

def silhouette(im):
    s = Image.new("RGBA", im.size, (40, 30, 60, 255))
    s.putalpha(im.split()[3])
    return s

# ---------- text ----------
def text_layer(txt, size, fill, stroke=(40, 30, 60), y=0):
    f = font(size)
    lay = Image.new("RGBA", (W, size * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bw = d.textlength(txt, font=f)
    d.text(((W - bw) / 2, size * 0.3), txt, font=f, fill=fill, stroke_width=max(6, size // 10), stroke_fill=stroke)
    return lay

def ease_pop(t):  # 0..1 -> overshoot scale
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    return 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2

def paste_scaled(base, lay, cx, cy, s, rot=0):
    if s <= 0.01: return
    w, h = lay.size
    l2 = lay.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    if rot: l2 = l2.rotate(rot, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(l2, (int(cx - l2.size[0] / 2), int(cy - l2.size[1] / 2)))

# ---------- scenes ----------
scenes = [  # (start, end, bg, char, question, answer, colour)
    (2.0, 5.95, background((120, 200, 255), (200, 235, 255), (110, 200, 80), (90, 180, 70), farm_extras), finish(cow()), "WHO SAYS MOO?", "COW!", (255, 255, 255)),
    (5.95, 9.9, background((110, 195, 255), (195, 235, 255), (110, 200, 80), (90, 180, 70), pond_extras), finish(duck()), "WHO SAYS QUACK?", "DUCK!", (255, 225, 60)),
    (9.9, 13.85, background((130, 205, 255), (205, 238, 255), (120, 200, 85), (95, 180, 70), yard_extras), finish(pig()), "WHO SAYS OINK?", "PIGGY!", (255, 170, 195)),
]
sil = [silhouette(s[3]) for s in scenes]
REVEAL = 1.75
intro_bg = background((255, 170, 210), (255, 225, 150), (120, 200, 85), (95, 180, 70), flowers)
q_layers = [text_layer(s[4], 92, (255, 255, 255)) for s in scenes]
a_layers = [text_layer(s[5], 170, s[6]) for s in scenes]
t1 = text_layer("CAN YOU GUESS", 110, (255, 255, 255)); t2 = text_layer("THE ANIMAL?", 130, (255, 230, 70))
qmark = text_layer("?", 420, (255, 255, 255))
end1 = text_layer("YAY!", 230, (255, 230, 70)); end2 = text_layer("GREAT JOB!", 130, (255, 255, 255))
stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))

def star(d, cx, cy, r, col):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * .45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=(40, 30, 60), width=5)

def frame(t):
    if t < 2.0:
        base = intro_bg.convert("RGBA")
        paste_scaled(base, t1, W / 2, 520, ease_pop((t - 0.1) / 0.5))
        paste_scaled(base, t2, W / 2, 700, ease_pop((t - 0.4) / 0.5))
        paste_scaled(base, qmark, W / 2, 1200 + 25 * math.sin(t * 6), ease_pop((t - 0.6) / 0.5), 10 * math.sin(t * 4))
        return base
    if t >= 13.85:
        base = intro_bg.convert("RGBA")
        lt = t - 13.85
        d = ImageDraw.Draw(base)
        for i, (x, y) in enumerate([(180, 300), (900, 380), (150, 1500), (930, 1450), (540, 1700), (300, 900), (800, 1000)]):
            s = ease_pop((lt - i * .06) / .4)
            if s > 0: star(d, x, y + 10 * math.sin(t * 8 + i), 70 * s, [(255, 230, 70), (255, 255, 255), (130, 220, 255)][i % 3])
        paste_scaled(base, end1, W / 2, 760, ease_pop(lt / 0.4))
        paste_scaled(base, end2, W / 2, 1020, ease_pop((lt - 0.2) / 0.4))
        return base
    for i, (st, en, bg, ch, *_r) in enumerate(scenes):
        if st <= t < en:
            lt = t - st
            base = bg.convert("RGBA")
            bob = 14 * math.sin(lt * 7)
            cx, cy = W / 2, 1230
            if lt < REVEAL:
                s = ease_pop(lt / 0.45) * 1.05
                paste_scaled(base, sil[i], cx, cy + bob, s)
                paste_scaled(base, qmark, cx, 820 + 15 * math.sin(lt * 9), ease_pop((lt - .2) / .4) * .6, 8 * math.sin(lt * 5))
                paste_scaled(base, q_layers[i], W / 2, 330, ease_pop((lt - .05) / .4))
            else:
                rt = lt - REVEAL
                s = 1.05 * (1 + 0.18 * math.exp(-rt * 6) * math.sin(rt * 25))
                if rt < 0.15:
                    flash = Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - rt / .15))))
                    paste_scaled(base, ch, cx, cy + bob, s)
                    base.alpha_composite(flash)
                else:
                    paste_scaled(base, ch, cx, cy + bob, s, 4 * math.sin(lt * 6))
                paste_scaled(base, a_layers[i], W / 2, 420, ease_pop(rt / .4))
            return base

# ---------- audio ----------
SR = 24000
mix = np.zeros(int(SR * DUR) + SR, np.float32)
def put(name, at, gain=1.0):
    s, sr = sf.read(f"{OUT}/{name}.wav", dtype="float32")
    i = int(at * SR); mix[i:i + len(s)] += s * gain
put("l0", 0.25)
for k, (st, *_r) in enumerate(scenes):
    put(f"l{1 + 2 * k}", st + 0.1)
    put(f"l{2 + 2 * k}", st + REVEAL + 0.1)
put("l7", 13.9)
# cheerful background tune (simple marimba-like synth)
notes = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84, 79, 76, 74, 72]
bpm, step = 120, 0.25
music = np.zeros_like(mix)
tt = np.arange(int(SR * 0.4)) / SR
for n in range(int(DUR / step)):
    f = 440 * 2 ** ((notes[n % len(notes)] - 69) / 12)
    env = np.exp(-tt * 9)
    tone = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 30)) * env
    i = int(n * step * SR); music[i:i + len(tone)] += tone[: len(music) - i]
    if n % 2 == 0:
        fb = 440 * 2 ** ((notes[n % len(notes)] - 12 - 12 - 69) / 12)
        bass = np.sin(2 * np.pi * fb * tt) * np.exp(-tt * 5)
        music[i:i + len(bass)] += 0.6 * bass[: len(music) - i]
mix = mix + 0.07 * music
# sparkle sfx on reveals
for st, *_r in scenes:
    i = int((st + REVEAL) * SR); n = int(SR * .35); tt2 = np.arange(n) / SR
    sp = np.sin(2 * np.pi * (1200 + 2400 * tt2) * tt2) * np.exp(-tt2 * 10) * 0.25
    mix[i:i + n] += sp
mix = mix[: int(SR * DUR)]
mix = mix / max(1e-6, np.abs(mix).max()) * 0.9
sf.write(f"{OUT}/audio.wav", mix, SR)

# ---------- video ----------
p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", f"{OUT}/audio.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", f"{OUT}/guess-the-animal-short01.mp4"],
                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
for n in range(int(DUR * FPS)):
    p.stdin.write(frame(n / FPS).convert("RGB").tobytes())
p.stdin.close(); p.wait()
for t in (1.0, 3.0, 4.5, 12.5, 14.5):
    frame(t).convert("RGB").save(f"{OUT}/check_{t}.png")
print("done")
