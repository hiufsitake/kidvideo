"""Shared helpers for kids Shorts (added 2026-10-26).
Upgrades over the first examples: soft body shading + rim light, ground drop shadows,
blinking, drop-in with squash-and-stretch, word-by-word caption pop, auto-fit text,
reveal screen-shake, and safe-zone constants (x 60-920, y 180-1500)."""
import math, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR, SR = 1080, 1920, 30, 15.0, 24000
SAFE_X0, SAFE_X1, SAFE_Y0, SAFE_Y1 = 60, 920, 180, 1500
CX = (SAFE_X0 + SAFE_X1) / 2  # 490: horizontal centre of the safe zone
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
OL = (40, 30, 30, 255)
INK = (40, 30, 60)
SS = 2

def font(sz): return ImageFont.truetype(FONT, sz)

# ---------- easing ----------
def ease_pop(t):
    if t <= 0: return 0.0
    if t >= 1: return 1.0
    return 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2

def ease_out(t):
    t = min(1, max(0, t)); return 1 - (1 - t) ** 3

# ---------- gradient bg ----------
def vgrad(top, bot):
    t = np.linspace(0, 1, H)[:, None, None]
    px = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return Image.fromarray(np.repeat(px, W, axis=1).astype(np.uint8)).convert("RGBA")

# ---------- character canvas ----------
def canvas(n=900):
    im = Image.new("RGBA", (n * SS, n * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def S(box): return [v * SS for v in box]

def E(d, box, fill, ol=10):
    d.ellipse(S(box), fill=fill, outline=OL if ol else None, width=ol * SS)

def eyes(d, cx, cy, gap=90, r=48, closed=False, skin=(255, 255, 255, 255)):
    for sx in (-1, 1):
        x = cx + sx * gap
        if closed:
            d.arc(S((x - r * .8, cy - r * .5, x + r * .8, cy + r * .6)), 20, 160, fill=OL, width=9 * SS)
            continue
        E(d, (x - r, cy - r, x + r, cy + r), (255, 255, 255, 255), 8)
        E(d, (x - r * .62, cy - r * .55, x + r * .62, cy + r * .75), (30, 25, 35, 255), 0)
        d.ellipse(S((x - r * .35, cy - r * .4, x - r * .02, cy - r * .07)), fill=(255, 255, 255, 255))
        d.ellipse(S((x + r * .1, cy + r * .2, x + r * .28, cy + r * .38)), fill=(255, 255, 255, 255))

def smile(d, cx, cy, w=60, width=10):
    d.arc(S((cx - w, cy - w * .6, cx + w, cy + w * .7)), 20, 160, fill=OL, width=width * SS)

def cheeks(d, cx, cy, gap=150):
    for sx in (-1, 1):
        d.ellipse(S((cx + sx * gap - 38, cy - 22, cx + sx * gap + 38, cy + 22)), fill=(255, 120, 150, 140))

def shade(im):
    """Soft top-left light / bottom-right shadow inside the character's alpha, plus blur-softened edge."""
    a = np.asarray(im.split()[3], np.float32) / 255
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    g = (yy / h * 0.75 + xx / w * 0.25)  # 0 top-left .. 1 bottom-right
    px = np.asarray(im, np.float32).copy()
    dark = np.clip((g - 0.55) * 0.55, 0, 0.22)[..., None]
    light = np.clip((0.35 - g) * 0.5, 0, 0.12)[..., None]
    px[..., :3] = px[..., :3] * (1 - dark) + 255 * light
    return Image.fromarray(np.clip(px, 0, 255).astype(np.uint8))

def finish(im, size):
    return shade(im).resize((size, size), Image.LANCZOS)

def silhouette(im):
    s = Image.new("RGBA", im.size, (45, 35, 80, 255)); s.putalpha(im.split()[3]); return s

# ---------- compositing ----------
def paste_scaled(base, lay, cx, cy, s, rot=0, sx=1.0, sy=1.0, anchor_bottom=False):
    if s <= 0.01: return
    w, h = lay.size
    nw, nh = max(1, int(w * s * sx)), max(1, int(h * s * sy))
    l2 = lay.resize((nw, nh), Image.LANCZOS)
    if rot: l2 = l2.rotate(rot, resample=Image.BICUBIC, expand=True)
    y = cy - l2.size[1] if anchor_bottom else cy - l2.size[1] / 2
    base.alpha_composite(l2, (int(cx - l2.size[0] / 2), int(y)))

def ground_shadow(base, cx, cy, w, alpha=70):
    lay = Image.new("RGBA", (int(w) + 80, int(w * .25) + 80), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((40, 40, 40 + w, 40 + w * .25), fill=(20, 20, 40, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(lay, (int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2)))

def drop_land(lt, t_land=0.35, drop=700):
    """Returns (y_offset, sx, sy) for a drop-in that lands at t_land with squash and stretch."""
    if lt < t_land:
        k = lt / t_land
        return -drop * (1 - k * k), 0.9, 1.12
    rt = lt - t_land
    q = 0.22 * math.exp(-rt * 7) * math.cos(rt * 22)
    return 0, 1 + q, 1 - q

def blinking(t, seed=0):
    p = (t + seed * 1.37) % 2.6
    return p < 0.12

def shake(base, t0, t, amp=14):
    dt = t - t0
    if 0 <= dt < 0.25:
        a = amp * (1 - dt / 0.25)
        ox, oy = int(a * math.sin(dt * 90)), int(a * math.cos(dt * 70))
        out = Image.new("RGBA", base.size, (255, 255, 255, 255))
        out.alpha_composite(base, (ox, oy))
        return out
    return base

# ---------- text ----------
def fit_size(txt, size, maxw):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    while size > 30 and d.textlength(txt, font=font(size)) + size * 0.2 > maxw: size -= 4
    return size

def word_layers(txt, size, fill, maxw=SAFE_X1 - SAFE_X0 - 30, stroke=INK):
    """Split a caption into per-word layers with x offsets, auto-fitted to maxw."""
    size = fit_size(txt, size, maxw)
    f = font(size); sw = max(6, size // 10)
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    words = txt.split(" "); space = d.textlength(" ", font=f)
    widths = [d.textlength(w, font=f) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    out, x = [], -total / 2
    for w, ww in zip(words, widths):
        lay = Image.new("RGBA", (int(ww + sw * 2 + 10), int(size * 1.6)), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((sw + 5, size * 0.15), w, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
        out.append((lay, x + ww / 2)); x += ww + space
    return out

def draw_words(base, words, cx, cy, lt, step=0.12, dur=0.35):
    for i, (lay, ox) in enumerate(words):
        paste_scaled(base, lay, cx + ox, cy, ease_pop((lt - i * step) / dur))

def star(d, cx, cy, r, col):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * .45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=INK, width=5)

def burst(d, cx, cy, lt, n=10, rad=260, cols=((255, 230, 70), (255, 255, 255), (130, 220, 255), (255, 150, 200))):
    if not (0 <= lt < 0.7): return
    k = ease_out(lt / 0.7)
    for i in range(n):
        a = i * 2 * math.pi / n + 0.3
        r = 20 * (1 - k) + 6
        star(d, cx + math.cos(a) * rad * k, cy + math.sin(a) * rad * k, r + 10, cols[i % len(cols)])

# ---------- audio ----------
def load(path):
    s, sr = sf.read(path, dtype="float32"); assert sr == SR; return s

def synth_music(notes, step, dur=DUR, wave_gain=1.0):
    music = np.zeros(int(SR * dur) + SR, np.float32)
    tt = np.arange(int(SR * 0.45)) / SR
    for n in range(int(dur / step)):
        nt = notes[n % len(notes)]
        i = int(n * step * SR)
        if nt is not None:
            f = 440 * 2 ** ((nt - 69) / 12)
            tone = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-tt * 30)) * np.exp(-tt * 9)
            music[i:i + len(tone)] += tone[: len(music) - i]
        if n % 4 == 0:  # soft kick
            k = np.sin(2 * np.pi * (110 - 60 * tt[:4000] * 10) * tt[:4000]) * np.exp(-tt[:4000] * 25)
            music[i:i + len(k)] += 0.5 * k[: len(music) - i]
        if n % 2 == 0 and nt is not None:
            fb = 440 * 2 ** ((nt - 24 - 69) / 12)
            bass = np.sin(2 * np.pi * fb * tt) * np.exp(-tt * 5)
            music[i:i + len(bass)] += 0.6 * bass[: len(music) - i]
    return music * wave_gain

def sfx_sparkle(n=0.35):
    t = np.arange(int(SR * n)) / SR
    return np.sin(2 * np.pi * (1200 + 2400 * t) * t) * np.exp(-t * 10) * 0.25

def sfx_boing(n=0.3):
    t = np.arange(int(SR * n)) / SR
    return np.sin(2 * np.pi * (500 - 900 * t) * t) * np.exp(-t * 12) * 0.35

def sfx_pop(n=0.08):
    t = np.arange(int(SR * n)) / SR
    return np.sin(2 * np.pi * (900 - 6000 * t) * t) * np.exp(-t * 60) * 0.4

def sfx_ding(n=0.6):
    t = np.arange(int(SR * n)) / SR
    return (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 6) * 0.18

def place(mix, s, at, gain=1.0):
    i = int(at * SR); s = s[: len(mix) - i]; mix[i:i + len(s)] += s * gain

def render(frame_fn, audio, out_mp4, workdir):
    audio = audio[: int(SR * DUR)]
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.9
    sf.write(f"{workdir}/audio.wav", audio, SR)
    p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", f"{workdir}/audio.wav", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-t", str(DUR), "-movflags", "+faststart", out_mp4],
                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for n in range(int(DUR * FPS)):
        p.stdin.write(frame_fn(n / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait()

def contact_sheet(frame_fn, times, path, cols=4):
    th = [frame_fn(t).convert("RGB").resize((270, 480)) for t in times]
    rows = (len(th) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 270, rows * 480), (0, 0, 0))
    for i, im in enumerate(th):
        d = ImageDraw.Draw(im)
        d.rectangle((SAFE_X0 / 4, SAFE_Y0 / 4, SAFE_X1 / 4, SAFE_Y1 / 4), outline=(255, 0, 0))
        d.text((6, 6), f"{times[i]:.1f}s", fill=(255, 0, 0))
        sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
    sheet.save(path)
