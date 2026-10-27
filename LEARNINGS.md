# Learnings log

Each run adds: date · what we learned from top Shorts · which upgrade we applied · result (from analytics, once available).

## 2026-10-25 — baseline
- Research: the most-viewed kids content is nursery rhymes/songs, animals & animal sounds, learning basics (colours, ABC, counting), opposites, and healthy habits. Top Shorts channels lean on simple this-or-that contrasts and bright, homemade-feeling lessons.
- Baseline style (Shorts #1–#2): flat cartoon drawn in code, outlined characters with faces, pop-in captions, synth melody, sparkle/pop SFX, kokoro af_heart voice.
- Known weak spots to fix next: characters are flat (no shading), no blinking or squash-and-stretch, static camera, first frame is a title card rather than motion, captions pop as whole lines not word-by-word.

## 2026-10-26 — Shorts #3 (Guess the Animal #2) and #4 (Count the Pumpkins)
- Research: web search for current top kids Shorts returned only generic channel charts (Tubefilter); takeaways carried over: guessing games with a pause-then-reveal and simple counting with a visible running total keep toddlers watching; seasonal-but-gentle topics (autumn pumpkins, late October) ride search interest without scary content.
- Upgrades applied (new shared `pipeline/common.py`):
  1. Hook in 1 second — no title card; frame 0 already has moving characters/silhouettes and the question.
  2. Character appeal — soft gradient shading on every character, ground drop shadows, blinking, drop-in with squash-and-stretch on landing.
  3. Text — captions pop word-by-word and auto-fit to the safe zone (centred at x=490).
  4. Camera/sound — reveal flash + small screen shake, star burst on each reveal/count, distinct boing/ding/sparkle SFX, soft kick in the music.
- Safe zone now enforced: characters/captions kept in x 60–920, y 180–1500 (Shorts #1–2 placed characters down to y≈1680).
- Result: pending analytics (Short #1 only published 2026-10-25).

## 2026-10-27 — Shorts #5 (Shape Friends) and #6 (Big or Small?)
- Analytics: Metricool returned no views/retention yet for Shorts #1–#4, so no series could be favoured; rotated into two untouched high-view categories (shapes, opposites).
- Research: web search again returned only generic Tubefilter channel charts; takeaway carried over — simple this-or-that contrasts (big vs small) and "spot it in real life" examples (circle = sun) are strong toddler formats.
- Upgrades applied (added to `pipeline/common.py`):
  1. Camera life — `camera()` + `zoom_curve()`: gentle 5–6% zoom toward the focus on each reveal (example object / small animal).
  2. Transitions — iris-wipe between scenes (0.22 s expanding circle with white rim) instead of hard cuts.
  3. Polish — `confetti()` falling, spinning confetti on the ending payoff.
  4. Learning beats — numbered corner dots pop one by one (square 1–4, triangle 1–3) with a pop SFX each; size contrast taught visually with BIG caption vs small caption.
- Caught in contact sheet: first ending of #6 showed the bear larger than the elephant (contradicts the lesson) — fixed to elephant vs mouse; sea light-rays read as harsh stripes — replaced with bubbles.
- Result: pending analytics.

## 2026-10-27 (follow-up) — fixing last run's problems
- Research fixed: extended web search + fetching the air.io "viral Shorts for YouTube Kids" guide gave concrete tips (now in PIPELINE.md "Standing takeaways"). New idea to apply next: make the last frame loop back into the first (same background/characters) so rewatches feel seamless.
- Analytics explained: Metricool showed 8 subscribers but no per-video views yet because YouTube data arrives with a 2–3 day lag. First usable numbers for Shorts #1–#4 should appear from ~2026-10-28; field IDs documented in PIPELINE.md.
- Repo access: `add_repo` isn't always offered; PIPELINE.md now says to use the existing clone when fetch/push work.
