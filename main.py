import streamlit as st 

# import Scripts.rec_audio
# import Scripts.summary
# import Scripts.text_to_speech

import os
from playsound import playsound
import plotly.graph_objects as go
import requests
from PIL import Image
import json
from streamlit_lottie import st_lottie

import Scripts.keyword_extract as keywrd
import Scripts.audio_to_text as transcribe
import Scripts.similarity as sim

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import pyaudio
import wave

st.set_page_config(page_icon=":computer:")
st.write("<div style='text-align: center'><h1>Clear <em style='text-align: center; color: #5192f5;'>Speak</em></h1></div>", unsafe_allow_html=True)

# AUDIO_PATH = "Audios"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FLAG = True

if "frames" not in st.session_state:
    st.session_state["frames"] = []

if "sample_width" not in st.session_state:
    st.session_state["sample_width"] = []

if "prev_score" not in st.session_state:
    st.session_state["prev_score"] = [0]

def record():
	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print("Start recording")
	st.session_state["sample_width"] = p.get_sample_size(FORMAT)
	st.session_state["frames"] = []

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

def record_to_file():
	record()

def mili_to_HMS(millis):
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    hours = int(hours)
    return f"{hours}:{minutes}:{seconds}"

def number_of_pauses():
    pauses = []
    # Load the audio file
    audio_file = AudioSegment.from_file("speech.wav", format="wav")

    # Set the minimum length of a silence that we want to detect (in milliseconds)
    silence_threshold = 1000

    # Detect all the non-silent parts of the audio file
    nonsilent_parts = detect_nonsilent(audio_file, min_silence_len=silence_threshold, silence_thresh=-50)

    # Calculate the length of each non-silent part
    nonsilent_durations = [part[1] - part[0] for part in nonsilent_parts]

    # Set the minimum duration of a pause that we want to detect (in milliseconds)
    pause_threshold = 3000

    # Find all the pauses that are longer than the pause threshold
    long_pauses = [i for i, duration in enumerate(nonsilent_durations) if duration > pause_threshold]

    # Print the start and end time of each long pause
    for pause_index in long_pauses:
        pause_start = nonsilent_parts[pause_index][1]
        pause_end = nonsilent_parts[pause_index][0]
        
        temp = f"Long pause from {mili_to_HMS(pause_start)}ms to {mili_to_HMS(pause_end)}ms"
        print(temp)
        pauses.append(temp)

    return pauses


def key_words(text):
    keyword_lst = keywrd.keywords_extract(text)
    return keyword_lst

def cal_score(sim_score, num_keywords_used, total_num_keyword):
    sim_score = sim_score/10
    k_used = num_keywords_used
    k_total = total_num_keyword

    k_score = (k_used/k_total) * 10
    total_score= int( (sim_score*35 + k_score* 65) /10)

    return total_score


def analytics(inp_txt):
    script_keywords = key_words(inp_txt.lower())
    keyword_cnt = len(script_keywords)
    speech_txt = transcribe.transcript()
    speech_keywords = key_words(speech_txt.lower())
    
    speech_lower = speech_txt.lower()
    
    not_spoken_keywords = []
    spoken_keywords_cnt = 0
    
    for i in script_keywords:
        if(i in speech_keywords):
            spoken_keywords_cnt += 1
        else:
            if(i not in speech_lower):
                not_spoken_keywords.append(i)
    
    similarity_score = sim.similarity_score(inp_txt,speech_txt)
    pauses = number_of_pauses()
    score = cal_score(similarity_score, spoken_keywords_cnt, keyword_cnt)
    
    output = f"""
The percentage of similarity with Script = {similarity_score} \n
The percentage of Keywords used = {int((spoken_keywords_cnt/keyword_cnt)*100)} \n
"""

    if(len(not_spoken_keywords) > 0):
        output += "Looks like you have missed out on the following keywords:\n"
        for i in not_spoken_keywords:
            output += i + "\n"
        output += "\n"
    
    if(len(pauses) > 0):
        output += "You took long pauses on the following ocassions:\n"
        for i in pauses:
            output += i + "\n"
    
    st.write("<div style='text-align: center'><h2>Analytics 📈</h2></div>", unsafe_allow_html=True)

    col1_anal, col2_anal = st.columns(2)

    with col1_anal:
        st.write("<h4>Suggestions: </h4>", unsafe_allow_html=True)
        st.write(output)
        
    with col2_anal:
        print("####################################")
        print(st.session_state["prev_score"][-1])
        print(score)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Speed", 'font': {'size': 24}},
            delta = {'reference': st.session_state["prev_score"][-1], 'increasing': {'color': "green"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "royalblue"},
                'bar': {'color': "royalblue"},
                
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score}}))

        fig.update_layout(font = {'color': "white", 'family': "Arial"})
        st.plotly_chart(fig, use_container_width=True)
        st.session_state["prev_score"].append(score)
        

st.sidebar.write("<div style='text-align: center'><h1>Instructions for use: 📄</h1></div>", unsafe_allow_html=True)
st.sidebar.write("")
st.sidebar.write("•	Clear Speak is a platform designed to improve your oration skills.", unsafe_allow_html=True)
st.sidebar.write("•	Click on the Start Recording button to record your speech when you're ready.", unsafe_allow_html=True)
st.sidebar.write("•	After recording,Enter your speech script into the provided space.", unsafe_allow_html=True)
st.sidebar.write("•	Click on the Analyze button to receive feedback on your speech delivery.", unsafe_allow_html=True)
st.sidebar.write("•	We recommend using Clear Speak in a focused and constructive manner.", unsafe_allow_html=True)
st.sidebar.write("•	Practicing regularly on Clear Speak can enhance your public speaking abilities.", unsafe_allow_html=True)
st.sidebar.write("•	By using Clear Speak, you can become a more confident, eloquent and effective communicator.", unsafe_allow_html=True)

col1_main,col2_main = st.columns(2)

with col1_main:
    
    #st.write(summary.summary)
    col1, col2 = st.columns(2)
    flag= False
    with col1:
        if st.button("Start recording"):
            FLAG = False
            record_to_file()
    with col2:
        if st.button("Stop recording"):
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
            flag= True

if(flag):
    st.audio("speech.wav")
    flag= False

input_text = st.text_area("Enter the script for your speech:",placeholder="Your speech.....")

if st.button("Analyze"):
    st.audio("speech.wav")
    if(input_text.strip()==""):
        st.write("No Script Entered, Please enter your Script :)")
        print("No Script Entered !!!")
    else:
        analytics(input_text)

with col2_main:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    lottie_url = "https://assets8.lottiefiles.com/packages/lf20_1pjemuh2.json"
    lottie_json= "lf20_1pjemuh2.json"
    lottie = load_lottiefile(lottie_json)

    # st_lottie(lottie, key="hello")
    st_lottie(
    lottie,
    speed=1,
    height=260,
    width=260,
    loop=True,
    key=None,
)
