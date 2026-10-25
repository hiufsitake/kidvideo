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
