import math, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 15.0
OUT = "/home/claude/short02"
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
OL = (40, 30, 60, 255)
SS = 2

def font(sz): return ImageFont.truetype(FONT, sz)

def grad(top, bot):
    t = np.linspace(0, 1, H)[:, None, None]
    px = np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t
    return Image.fromarray(np.repeat(px, W, axis=1).astype(np.uint8)).convert("RGBA")

def confetti_bg(top, bot, seed):
    img = grad(top, bot)
    d = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(seed)
    for _ in range(70):
        x, y, r = rng.integers(0, W), rng.integers(0, H), rng.integers(8, 22)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, 90))
    for cx, cy, s in [(200, 1650, 1.2), (850, 1720, 1.0)]:
        for dx, dy, r in [(-70, 10, 60), (0, -20, 80), (75, 10, 60), (0, 30, 65)]:
            d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=(255, 255, 255, 200))
    return img

def C(d, box, fill, ol=10):
    d.ellipse([v * SS for v in box], fill=fill, outline=OL if ol else None, width=ol * SS)

def face(d, cx, cy, s=1.0, cheek=True):
    for sx in (-1, 1):
        x = cx + sx * 55 * s; r = 26 * s
        C(d, (x - r, cy - r * 1.2, x + r, cy + r * 1.2), (35, 25, 40, 255), 0)
        d.ellipse([v * SS for v in (x - r * .55, cy - r * .9, x - r * .05, cy - r * .35)], fill=(255, 255, 255, 255))
        if cheek:
            d.ellipse([v * SS for v in (x + sx * 40 * s - 30 * s, cy + 40 * s, x + sx * 40 * s + 30 * s, cy + 62 * s)], fill=(255, 120, 150, 150))
    d.arc([v * SS for v in (cx - 40 * s, cy + 5 * s, cx + 40 * s, cy + 60 * s)], 15, 165, fill=OL, width=10 * SS)

def layer():
    im = Image.new("RGBA", (700 * SS, 700 * SS), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)

def done(im): return im.resize((700, 700), Image.LANCZOS)

def balloon(col, dark):
    im, d = layer()
    pts = [(350 + 30 * math.sin(i / 6) , 560 + i * 3) for i in range(45)]
    d.line([(x * SS, y * SS) for x, y in pts], fill=OL, width=6 * SS)
    d.polygon([(v[0] * SS, v[1] * SS) for v in [(325, 575), (375, 575), (350, 535)]], fill=dark, outline=OL, width=6 * SS)
    C(d, (150, 40, 550, 560), col)
    d.ellipse([v * SS for v in (220, 110, 310, 260)], fill=(255, 255, 255, 150))
    return done(im)

def apple():
    im, d = layer()
    d.line([v * SS for v in (350, 170, 370, 90)], fill=(110, 70, 40, 255), width=22 * SS)
    d.ellipse([v * SS for v in (380, 70, 520, 140)], fill=(80, 190, 80, 255), outline=OL, width=8 * SS)
    C(d, (120, 150, 380, 600), (235, 50, 60, 255)); C(d, (320, 150, 580, 600), (235, 50, 60, 255))
    d.ellipse([v * SS for v in (140, 170, 560, 590)], fill=(235, 50, 60, 255))
    d.ellipse([v * SS for v in (190, 220, 260, 330)], fill=(255, 255, 255, 140))
    face(d, 350, 380)
    return done(im)

def starimg():
    im, d = layer()
    pts = []
    for i in range(10):
        rr = 300 if i % 2 == 0 else 135
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(((350 + rr * math.cos(a)) * SS, (380 + rr * math.sin(a)) * SS))
    d.polygon(pts, fill=(255, 210, 40, 255), outline=OL, width=12 * SS)
    face(d, 350, 380, 0.9)
    return done(im)

def drop():
    im, d = layer()
    pts = [(350, 40)]
    for i in range(0, 361, 6):
        a = math.radians(i)
        pts.append((350 + 230 * math.sin(a), 420 + 230 * math.cos(a)))
    pts = [p for p in pts if not (p[1] < 300 and abs(p[0] - 350) > 10)]
    # build teardrop: tip + lower circle
    poly = [(350 * SS, 40 * SS)]
    for i in range(-130, 131, 4):
        a = math.radians(i)
        poly.append(((350 + 230 * math.sin(a)) * SS, (420 - 230 * math.cos(a) * -1) * SS))
    poly = [(350 * SS, 40 * SS)] + [((350 + 230 * math.cos(math.radians(t))) * SS, (420 + 230 * math.sin(math.radians(t))) * SS) for t in range(-40, 221, 4)]
    d.polygon(poly, fill=(50, 140, 240, 255), outline=OL, width=12 * SS)
    d.ellipse([v * SS for v in (220, 300, 280, 420)], fill=(255, 255, 255, 150))
    face(d, 350, 440)
    return done(im)

def leaf():
    im, d = layer()
    big = Image.new("RGBA", (700 * SS, 700 * SS), (0, 0, 0, 0)); bd = ImageDraw.Draw(big)
    bd.ellipse([v * SS for v in (170, 40, 530, 640)], fill=(70, 185, 80, 255), outline=OL, width=12 * SS)
    bd.line([v * SS for v in (350, 70, 350, 690)], fill=(40, 120, 50, 255), width=10 * SS)
    for y in (200, 300, 520):
        bd.line([v * SS for v in (350, y + 40, 250, y)], fill=(40, 120, 50, 255), width=7 * SS)
        bd.line([v * SS for v in (350, y + 40, 450, y)], fill=(40, 120, 50, 255), width=7 * SS)
    big = big.rotate(-20, resample=Image.BICUBIC)
    im.alpha_composite(big)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([v * SS for v in (250, 340, 450, 470)], 60 * SS, fill=(70, 185, 80, 255))
    face(d, 360, 390, 0.9)
    return done(im)

def text_layer(txt, size, fill, stroke=(40, 30, 60)):
    f = font(size)
    lay = Image.new("RGBA", (W, int(size * 1.7)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text(((W - d.textlength(txt, font=f)) / 2, size * 0.15), txt, font=f, fill=fill, stroke_width=max(6, size // 9), stroke_fill=stroke)
    return lay

def pop(t):
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    return 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2

def paste(base, lay, cx, cy, s, rot=0):
    if s <= 0.01: return
    w, h = lay.size
    l2 = lay.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    if rot: l2 = l2.rotate(rot, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(l2, (int(cx - l2.size[0] / 2), int(cy - l2.size[1] / 2)))

SEG = 2.9
colours = [  # name, main, dark, bg top, bg bottom, object
    ("RED", (240, 60, 70, 255), (180, 30, 40, 255), (255, 200, 200), (255, 150, 160), apple(), "APPLE"),
    ("YELLOW", (255, 215, 50, 255), (210, 160, 20, 255), (255, 245, 190), (255, 215, 120), starimg(), "STAR"),
    ("BLUE", (60, 140, 240, 255), (30, 90, 190, 255), (200, 230, 255), (140, 190, 255), drop(), "WATER"),
    ("GREEN", (70, 190, 90, 255), (40, 130, 60, 255), (210, 250, 210), (150, 225, 160), leaf(), "LEAF"),
]
segs = []
for i, (name, col, dark, top, bot, obj, word) in enumerate(colours):
    segs.append(dict(st=2.0 + i * SEG, bg=confetti_bg(top, bot, i), bal=balloon(col, dark), obj=obj,
                     name=text_layer(name + "!", 190, col[:3]), word=text_layer(word, 90, (255, 255, 255))))
intro_bg = confetti_bg((255, 190, 230), (190, 210, 255), 9)
t1 = text_layer("LET'S LEARN", 120, (255, 255, 255)); t2 = text_layer("COLOURS!", 190, (255, 220, 60))
END = 2.0 + 4 * SEG
e1 = text_layer("YAY!", 230, (255, 220, 60)); e2 = text_layer("YOU DID IT!", 130, (255, 255, 255))
mini = [balloon(c[1], c[2]).resize((260, 260), Image.LANCZOS) for c in colours]

def frame(t):
    if t < 2.0 or t >= END:
        base = intro_bg.copy()
        lt = t if t < 2.0 else t - END
        for i, m in enumerate(mini):
            x = 170 + i * 247
            y = 1500 - 40 * math.sin(t * 3 + i) - (0 if t < 2.0 else 300 * lt)
            paste(base, m, x, y, pop((lt - 0.15 * i) / 0.5), 6 * math.sin(t * 4 + i))
        if t < 2.0:
            paste(base, t1, W / 2, 560, pop((lt - .05) / .45)); paste(base, t2, W / 2, 780, pop((lt - .3) / .45))
        else:
            paste(base, e1, W / 2, 620, pop(lt / .4)); paste(base, e2, W / 2, 880, pop((lt - .2) / .4))
        return base
    for s in segs:
        if s["st"] <= t < s["st"] + SEG:
            lt = t - s["st"]; base = s["bg"].copy()
            rise = 1 - pop(lt / 0.6)
            paste(base, s["bal"], 330, 1150 + 900 * rise + 30 * math.sin(lt * 4), 1.0, 5 * math.sin(lt * 3))
            paste(base, s["name"], W / 2, 330, pop((lt - .1) / .4))
            os_ = pop((lt - .7) / .45) * 0.75
            paste(base, s["obj"], 770, 1050 + 20 * math.sin(lt * 8), os_, 6 * math.sin(lt * 5))
            paste(base, s["word"], 770, 1380, pop((lt - .9) / .4))
            return base

SR = 24000
mix = np.zeros(int(SR * DUR) + SR, np.float32)
def put(name, at):
    s, _ = sf.read(f"{OUT}/{name}.wav", dtype="float32"); i = int(at * SR); mix[i:i + len(s)] += s
put("l0", 0.25)
for i, s in enumerate(segs): put(f"l{i + 1}", s["st"] + 0.1)
put("l5", END + 0.1)
notes = [67, 72, 76, 72, 69, 74, 77, 74, 71, 74, 79, 74, 72, 76, 79, 84]
music = np.zeros_like(mix); tt = np.arange(int(SR * .4)) / SR
for n in range(int(DUR / .25)):
    f = 440 * 2 ** ((notes[n % 16] - 69) / 12)
    tone = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 30)) * np.exp(-tt * 9)
    i = int(n * .25 * SR); music[i:i + len(tone)] += tone[:len(music) - i]
    if n % 2 == 0:
        b = np.sin(2 * np.pi * f / 4 * tt) * np.exp(-tt * 5); music[i:i + len(b)] += .6 * b[:len(music) - i]
mix += .07 * music
for s in segs:  # pop sfx when object appears
    i = int((s["st"] + .7) * SR); n = int(SR * .25); t2_ = np.arange(n) / SR
    mix[i:i + n] += np.sin(2 * np.pi * (500 + 3000 * t2_) * t2_) * np.exp(-t2_ * 14) * .3
mix = mix[:int(SR * DUR)]; mix = mix / np.abs(mix).max() * .9
sf.write(f"{OUT}/audio.wav", mix, SR)

p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", f"{OUT}/audio.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", f"{OUT}/learn-colours-short02.mp4"],
                     stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
for n in range(int(DUR * FPS)):
    p.stdin.write(frame(n / FPS).convert("RGB").tobytes())
p.stdin.close(); p.wait()
ims = [frame(t).convert("RGB").resize((270, 480)) for t in (1.5, 4.0, 6.8, 9.7, 12.6, 14.6)]
c = Image.new("RGB", (270 * 6, 480)); [c.paste(im, (i * 270, 0)) for i, im in enumerate(ims)]; c.save(f"{OUT}/contact.png")
print("done")
