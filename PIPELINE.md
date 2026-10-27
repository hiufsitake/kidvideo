# Kids Shorts pipeline

Daily job: make 2 new 15-second kids YouTube Shorts and schedule them in Metricool.

## Channel rules
- Audience: toddlers / preschoolers (about 2–6). Made for Kids = true. Public. Type = short. Category = EDUCATION.
- 15.0 s, 1080x1920, 30 fps, H.264 + AAC, `-preset veryfast -crf 20`.
- Structure: bright hook question in the first second → 3–4 quick beats with pop animations → happy ending ("Yay! Great job!").
- Original content only: no copyrighted characters (no Peppa, Cocomelon, Baby Shark, Bluey, KPop Demon Hunters, Sonic…), no copyrighted songs. Public-domain nursery rhymes are fine.
- Cartoon style drawn in code (flat, cute, faces on objects, thick dark outlines, confetti/sky backgrounds). Not realistic, so `isAiGeneratedContent` = false.
- Every Short must have real learning value (sounds, colours, counting, shapes, opposites, ABC, healthy habits…), not filler.

## Channel safety — TOP PRIORITY (Fs does not want the channel banned)
Safety beats views. If a Short can't meet every rule below, don't post it; report why instead.
- **Copyright:** only original visuals, voice and music made in the pipeline. No characters, logos, songs, sound clips or footage from anyone else — not even "a similar version". Nursery rhymes only if published before 1929, sung with our own melody synth, and never a modern remake's arrangement.
- **Child safety:** nothing scary, violent, gross, unsafe to copy (no climbing, fire, choking hazards, medicine, strangers), or "Elsagate"-style. Gentle, positive, age 2–6.
- **No misleading metadata:** title, description, tags and thumbnail must describe exactly what's in the video. No clickbait, no fake "Part 2" of other channels, no trending names or brands that aren't in the video, max ~10 relevant tags, no tag or hashtag stuffing (≤ 6 hashtags).
- **Not mass-produced / repetitive (inauthentic content policy):** every Short must have a different script and a clearly different visual concept, characters or format from the last 14 in `topics.md`. Never re-upload or lightly re-edit an earlier video. Series are fine; clones are not.
- **Spam:** never post the same video twice, never post to other channels, no "sub4sub", no links, no asking kids to like/comment/subscribe.
- **Made for Kids** must always be `true` (COPPA). AI disclosure: set `isAiGeneratedContent` true if a video ever contains realistic-looking AI people, animals or places.
- **Accuracy:** every fact taught (animal sounds, colours, counts, spellings) must be correct — double-check before rendering.
- **Volume:** stay within 2 Shorts/day and Metricool's monthly limit; never bulk-post to catch up.

## Topic selection (high views)
Highest-viewed kids categories on YouTube: nursery rhymes / kids songs; animals & animal sounds;
learning basics (colours, ABC/phonics, counting, shapes); opposites / this-or-that (big vs small);
healthy habits (wash hands, brush teeth, eat veggies). Rotate across these, build series
(e.g. "Guess the Animal #2"), and never repeat a topic already in `topics.md`.
If Metricool analytics show a series doing best, make more of it.

## Learn from top Shorts (every run, before writing scripts)
- Web-search what kids' Shorts are getting the most views right now. Generic "most viewed" queries only return Tubefilter channel charts, so:
  use `mode: "extended"`, search for formats/techniques (e.g. "viral YouTube Kids Shorts tips", "toddler Shorts hooks retention", "trending preschool learning topics <month year>"),
  and WebFetch at least one useful article to pull concrete tips. If results are still thin, say so in `LEARNINGS.md` and reuse the standing takeaways below.
- Standing takeaways (2026-10-27, air.io YouTube Kids Shorts guide): question or striking visual in the first seconds; a short pause before each payoff;
  new scene/animation every few seconds; numbered series; bold captions (kids watch muted); **loop the ending back into the opening** so rewatches feel seamless.
  Ignore any advice to add calls-to-action for kids (our spam rules forbid asking kids to like/subscribe).
- Study only the *ideas*: topics, hook styles, pacing, length, colour palettes, question formats, series structures. Formats aren't owned by anyone.
- Never download, copy, trace or re-edit anyone else's video, art, characters, voice or music. Everything we publish is made from scratch here.
- Note 1–3 takeaways in `LEARNINGS.md` and use them in today's Shorts.

## Make it attractive — continuous improvement
Every run must make the videos noticeably better than the last, not just new. Pick at least ONE upgrade per run, apply it,
and log it in `LEARNINGS.md` (date, what changed, why). Keep upgrades that work; promote proven ones into the example scripts in `pipeline/`.
**Safe zone (mandatory):** YouTube's Shorts UI covers the bottom ~20% (title, handle, description) and the right ~13% (like/share buttons) and the top ~8%.
Keep all characters, captions and key action inside x 60–920, y 180–1500 of the 1080x1920 frame; only background decoration may sit outside it.
Upgrade ideas, roughly in priority order:
1. **Hook in 1 second:** the first frame already has motion, a big face and a question; no slow fade-ins.
2. **Character appeal:** soft gradient shading, rim highlights, drop shadows, bigger heads and eyes, blinking, squash-and-stretch on landing, little idle wiggles.
3. **Camera life:** gentle zoom-ins on reveals, slight pans, screen shake on "pop", parallax background layers.
4. **Pacing:** something new happens every 1–1.5 s; total 15 s; end on a satisfying payoff.
5. **Colour:** bright, saturated, high-contrast palettes; each scene has one dominant colour.
6. **Text:** huge, bold, few words, word-by-word pop synced to the voice; always readable on a phone.
7. **Sound:** a catchy simple melody that matches the theme, a distinct SFX for every pop/reveal, the voice clearly above the music.
8. **Polish:** particles (stars, confetti, bubbles), smooth easing, no hard cuts without a transition.
Use Metricool analytics (brand 7637079) once videos have data. YouTube analytics reach Metricool with a **2–3 day lag**, so a Short
has no numbers until ~72 h after publishing — that is normal, not an error. Query `getAnalyticsDataByMetrics` with
`YTVP17,YTVP06,YTVP08,YTVP09` (title, views, avg view duration, likes) over a range that covers the publish dates, plus
`YTEV01,YTEV02` (subscribers, channel views) for totals; the `all videos` connector (YTVV*) currently returns no rows. Then compare views and retention by series, and write in `LEARNINGS.md` what the best ones have in common.

## Tools
- Voice: `pip install --break-system-packages kokoro-onnx soundfile`, model files from
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx and voices-v1.0.bin.
  Voice `af_heart`, speed ~1.05. See `pipeline/example_tts.py`.
- Render: Python + Pillow frames piped into ffmpeg; soft synth background music + pop/sparkle SFX.
  Working examples: `pipeline/example_guess_the_animal.py`, `pipeline/example_learn_colours.py` (copy, then change the scenes).
- Always check a contact sheet of key frames before publishing (text not clipped, characters recognisable).

## Publishing
0. Repo access: attach `hiufsitake/kidvideo` with `add_repo` (access "push") if that tool exists. If it doesn't, check whether
   `/home/claude/kidvideo` is already a clone with a working `origin` (`git fetch origin main`, then `git checkout -B main origin/main`);
   if fetch and push work, carry on — only report a problem if neither route gives push access.
1. Commit the MP4 to `shorts/<slug>.mp4` and push to `main`.
2. Public URL: `https://raw.githubusercontent.com/hiufsitake/kidvideo/main/shorts/<slug>.mp4` (check it returns 200).
3. Metricool brand id `7637079`, timezone `Asia/Kuching`, network `youtube`, youtubeData: title (with emoji + `#shorts`), type `short`,
   privacy `public`, tags, category `EDUCATION`, madeForKids `true`, isAiGeneratedContent `false`.
4. Append each topic, slug, title and post time to `topics.md`.
