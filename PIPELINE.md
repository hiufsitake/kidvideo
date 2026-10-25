# Kids Shorts pipeline

Daily job: make 2 new 15-second kids YouTube Shorts and schedule them in Metricool.

## Channel rules
- Audience: toddlers / preschoolers (about 2–6). Made for Kids = true. Public. Type = short. Category = EDUCATION.
- 15.0 s, 1080x1920, 30 fps, H.264 + AAC, `-preset veryfast -crf 20`.
- Structure: bright hook question in the first second → 3–4 quick beats with pop animations → happy ending ("Yay! Great job!").
- Original content only: no copyrighted characters (no Peppa, Cocomelon, Baby Shark, Bluey, KPop Demon Hunters, Sonic…), no copyrighted songs. Public-domain nursery rhymes are fine.
- Cartoon style drawn in code (flat, cute, faces on objects, thick dark outlines, confetti/sky backgrounds). Not realistic, so `isAiGeneratedContent` = false.
- Every Short must have real learning value (sounds, colours, counting, shapes, opposites, ABC, healthy habits…), not filler.

## Topic selection (high views)
Highest-viewed kids categories on YouTube: nursery rhymes / kids songs; animals & animal sounds;
learning basics (colours, ABC/phonics, counting, shapes); opposites / this-or-that (big vs small);
healthy habits (wash hands, brush teeth, eat veggies). Rotate across these, build series
(e.g. "Guess the Animal #2"), and never repeat a topic already in `topics.md`.
If Metricool analytics show a series doing best, make more of it.

## Tools
- Voice: `pip install --break-system-packages kokoro-onnx soundfile`, model files from
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx and voices-v1.0.bin.
  Voice `af_heart`, speed ~1.05. See `pipeline/example_tts.py`.
- Render: Python + Pillow frames piped into ffmpeg; soft synth background music + pop/sparkle SFX.
  Working examples: `pipeline/example_guess_the_animal.py`, `pipeline/example_learn_colours.py` (copy, then change the scenes).
- Always check a contact sheet of key frames before publishing (text not clipped, characters recognisable).

## Publishing
1. Commit the MP4 to `shorts/<slug>.mp4` and push to `main`.
2. Public URL: `https://raw.githubusercontent.com/hiufsitake/kidvideo/main/shorts/<slug>.mp4` (check it returns 200).
3. Metricool brand id `7637079`, timezone `Asia/Kuching`, network `youtube`, youtubeData: title (with emoji + `#shorts`), type `short`,
   privacy `public`, tags, category `EDUCATION`, madeForKids `true`, isAiGeneratedContent `false`.
4. Append each topic, slug, title and post time to `topics.md`.
