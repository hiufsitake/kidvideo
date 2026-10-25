import sys, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("kokoro.onnx", "voices.bin")
lines = {
 "l0": "Can you guess the animal?",
 "l1": "Who says... moo?",
 "l2": "It's a cow! Moo!",
 "l3": "Who says... quack?",
 "l4": "A duck! Quack quack!",
 "l5": "Who says... oink?",
 "l6": "A piggy! Oink oink!",
 "l7": "Yay! Great job!",
}
for n,t in lines.items():
    s, sr = k.create(t, voice="af_heart", speed=1.05, lang="en-us")
    sf.write(f"/home/claude/short01/{n}.wav", s, sr)
    print(n, round(len(s)/sr,2))
