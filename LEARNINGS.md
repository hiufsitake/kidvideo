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

## 2026-10-28 — Shorts #7 (Guess the Animal #3) and #8 (Let's Wash Our Hands!)
- Analytics: Metricool still shows only channel totals (8 subscribers); per-video views for #1–#6 are still null (2–3 day lag), so no series could be ranked yet. Continued the Guess the Animal series (#3) and opened a new high-view category (healthy habits).
- Research (extended search + conthunt.app Shorts best-practices guide): promise the payoff in the first 1–2 s; one idea per Short; every cut must earn its place; make the last frame match the first so the loop feels seamless; captions should reinforce, not cover, the action.
- Upgrades applied (promoted into `pipeline/common.py`):
  1. **Seamless loop** — `with_transitions()` crossfades the last 0.45 s into frame 0 (same background, characters and caption as the hook), so YouTube's auto-replay flows straight back into the question.
  2. Iris wipe is now a shared helper (`iris()`), and hook captions are fully visible on frame 0 (they're also the loop target).
  3. Numbered step badges (1–5) with one dominant colour per step for the handwashing routine; zoom on the scrub and the dry payoff.
- Caught in contact sheet: front-view horse read like a lion/cow (curly mane round the face) — redrawn in side profile with long muzzle and neck mane; tap stream was hidden behind a hand — tap moved between the hands; soap bar overlapped a sleeve — moved and shrunk.
- Result: pending analytics.

## 2026-10-29 — Shorts #9 (ABC Fun #1) and #10 (Baby Animals #1)
- Analytics: Metricool still returns null views for all published Shorts (#1–#6 listed, no numbers yet; 2–3 day lag), so no series ranked. Opened two new numbered series in high-view categories not yet covered: ABC/alphabet and baby animal names.
- Research (extended search + aibrify "Shorts retention curve playbook 2026"): change the visual every ~1.5–2 s (not faster than ~1.2 s, never a gap > 2.5 s); 2–4 high-contrast words per frame; deliver the first payoff in the first half and make each item a self-contained mini-payoff; match last frame to first for the loop.
- Upgrades applied:
  1. **Extra mid-scene beat** so nothing sits still > ~1.5 s: ABC — "letter link" (the first letter flies from the word up into the big letter, with a pop); Baby Animals — heart "hug" beat with a happy hop and a two-note chime.
  2. **Parallax clouds** — `drift_clouds()` in `common.py`: clouds slowly drift over each static background.
  3. **Solid silhouettes** — `silhouette()` now ignores semi-transparent cheeks/highlights, which used to show through the guess silhouettes.
  4. Recurring cast: dog/cat/hen reused from #3/#7 via AST import (`borrow()`), new chick character; new scene concept (parent + baby pair).
- Music: ABC Short uses our own synth of the traditional "Twinkle/ABC" melody (1761, public domain).
- Caught in contact sheet: flying letter overshot and overlapped the big letter (fixed to land exactly on it); Baby Animals characters too small (mommy 560→680, baby 330→400).
- Result: pending analytics.
