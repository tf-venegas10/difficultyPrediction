import sys
from aubio import source, pitch

if len(sys.argv) < 2:
    print "not enough arguments"
    sys.exit(1)

filename = sys.argv[1]

downsample = 1
samplerate = int(sys.argv[2])

win_s = 4096 // downsample
hop_s = 512 // downsample

src = source(filename, samplerate, hop_s)
samplerate = src.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

total_frames = 0
while True:
    samples, read = src()
    pitch = pitch_o(samples)[0]
    # pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    # if confidence < 0.8: pitch = 0.
    print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s:
        break
