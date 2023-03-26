import streamlit as st 

import Scripts.rec_audio
import Scripts.audio_to_text as audio_to_text
import Scripts.summary
import Scripts.text_to_speech
import plotly.graph_objects as go
from playsound import playsound
import requests
from PIL import Image
import json
from streamlit_lottie import st_lottie

#audio_file = "intro.mp3"

st.set_page_config(page_title="Clear Speak")

#playsound(audio_file)
st.write("<div style='text-align: center'><h1>Clear Speak</h1></div>", unsafe_allow_html=True)

col1_main,col2_main = st.columns(2)

with col1_main:

    input_text = st.text_area("Enter script for the speech",placeholder="Your speech.....")
    
    #st.write(summary.summary)
    col1, col2 = st.columns(2)
    flag= False
    with col1:
        st.button("Start recording")
    with col2:
        if st.button("Stop recording"):
            flag= True
    
    if(flag):
        st.audio("speech.wav")
        flag= False

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


st.write("<div style='text-align: center'><h2>Analytics 📈</h2></div>", unsafe_allow_html=True)



col1_anal, col2_anal = st.columns(2)

with col1_anal:
    st.write("<h4>Suggestions: </h4>", unsafe_allow_html=True)
    

with col2_anal:
    

    # fig = go.Figure(go.Indicator(
    #     mode = "gauge+number",
    #     value = 270,
    #     domain = {'x': [0, 1], 'y': [0, 1]},
    #     title = {'text': "Speed"}))

    # fig = go.Figure(go.Indicator(
    #     mode = "gauge+number+delta",
    #     value = 90,
    #     domain = {'x': [0, 1], 'y': [0, 1]},
    #     title = {'text': "Speed", 'font': {'size': 24}},
    #     delta = {'reference': 75, 'increasing': {'color': "RebeccaPurple"}},
    #     gauge = {
    #         'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
    #         'bar': {'color': "darkblue"},
            
    #         'borderwidth': 2,
    #         'bordercolor': "gray",
    #         'steps': [
    #             {'range': [75, 100], 'color': 'royalblue'}],
    #         'threshold': {
    #             'line': {'color': "red", 'width': 4},
    #             'thickness': 0.75,
    #             'value': 90}}))

    # fig.update_layout(font = {'color': "darkblue", 'family': "Arial"})
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 90,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed", 'font': {'size': 24}},
        delta = {'reference': 75, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "royalblue"},
            'bar': {'color': "royalblue"},
            
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))

    fig.update_layout(font = {'color': "white", 'family': "Arial"})

    st.plotly_chart(fig, use_container_width=True)
    
    
st.sidebar.write("<div style='text-align: center'><h1>Instructions for use: 📖</h1></div>", unsafe_allow_html=True)
#= Image.open("C:\Users\siddh\Desktop\clear-speak\usermanual.png")
st.sidebar.write("")
st.sidebar.write("•	Clear Speak is a platform designed to improve your oration skills.", unsafe_allow_html=True)
st.sidebar.write("•	To get started, enter your speech script into the provided space.", unsafe_allow_html=True)
st.sidebar.write("•	Click on the Start Recording button to record your speech when you're ready.", unsafe_allow_html=True)
st.sidebar.write("•	After recording, click on the Analyze button to receive feedback on your speech delivery.", unsafe_allow_html=True)
st.sidebar.write("•	We recommend using Clear Speak in a focused and constructive manner.", unsafe_allow_html=True)
st.sidebar.write("•	Practicing regularly on Clear Speak can enhance your public speaking abilities.", unsafe_allow_html=True)
st.sidebar.write("•	By using Clear Speak, you can become a more confident, eloquent and effective communicator.", unsafe_allow_html=True)
