import pyaudio
import wave
import streamlit as st 

st.set_page_config(page_title="Clear Speak")

AUDIO_PATH = "Audios"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

FLAG = True

if "frames" not in st.session_state:
    st.session_state["frames"] = []

if "sample_width" not in st.session_state:
    st.session_state["sample_width"] = []

def record():
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print("Start recording")
	st.session_state["sample_width"] = p.get_sample_size(FORMAT)
	frames = []

	while(True):
		data = stream.read(CHUNK)
		st.session_state["frames"].append(data)
		#frames.append(data)
		if(FLAG == True):
			break
	
	print("Done recording")
	stream.stop_stream()
	stream.close()
	p.terminate()
	# return sample_width, frames	

def record_to_file(file_path):
	record()

print("Restarted")
if st.button("Start"):
    FLAG = False
    record_to_file("speech.wav")

if st.button("Stop"):
    FLAG = True
    print("Done")
    wf = wave.open("speech.wav", 'wb')
    wf.setnchannels(CHANNELS)
    frames = st.session_state["frames"]
    sample_width = st.session_state["sample_width"]
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
