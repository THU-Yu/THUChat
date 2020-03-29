import sounddevice as sd
from scipy.io import wavfile

fs = 44100
length = 5
recording = sd.rec(frames=fs * length, samplerate=fs, blocking=True, channels=1)
wavfile.write('recording.wav', fs, recording)