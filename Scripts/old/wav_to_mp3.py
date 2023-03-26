from pydub import AudioSegment
sound = AudioSegment.from_wav('speech.wav')
sound.export('speech.mp3', format='mp3')