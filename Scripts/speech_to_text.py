import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

AUDIO_PATH = "Audios"

freq = 44100 # Sampling frequency usually between 44100 or 48000
duration = 15 # Recording duration

# Start recorder with the given values of duration and sample frequency
recording = sd.rec(int(duration * freq),
				samplerate=freq, channels=2)

sd.wait() # Record audio for the given number of seconds

# This will convert the NumPy array to an audio file with the given sampling frequency
#write("recording0.wav", freq, recording)
wv.write(f"{AUDIO_PATH}/speech.wav", recording, freq, sampwidth=2)
