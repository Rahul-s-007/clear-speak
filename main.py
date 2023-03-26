import streamlit as st

import os
import shutil

import Scripts.rec_audio
import Scripts.audio_to_text as audio_to_text
import Scripts.summary
import Scripts.text_to_speech

import plotly.graph_objects as go

import requests
from PIL import Image
from streamlit_lottie import st_lottie

USER_AUDIO = "speech.wav"
COMP_AUDIO = "comp.wav"

def app():
    col1_main,col2_main = st.columns(2)

    with col1_main:
        input_text = st.text_area("Enter script for the speech",placeholder="Your speech.....")
        
        #st.write(summary.summary)
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("Start recording")
        with col2:
            if st.button("Stop recording"):
                st.audio("speech.wav")

    with col2_main:

        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_url = "https://assets8.lottiefiles.com/packages/lf20_1pjemuh2.json"
        lottie = load_lottieurl(lottie_url)

        st_lottie(lottie, key="hello")


    st.write("<div style='text-align: center'><h2>Analytics</h2></div>", unsafe_allow_html=True)

    col1_anal, col2_anal = st.columns(2)

    with col1_anal:
        st.write("<h4>Suggestions: </h4>", unsafe_allow_html=True)
        
    with col2_anal:
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

def main():
    # if os.path.exists(USER_AUDIO):
    #     shutil.rmtree(path = USER_AUDIO, ignore_errors = True)
    #     print("USER AUDIO DELETED")

    # if os.path.exists(COMP_AUDIO):
    #     shutil.rmtree(path = COMP_AUDIO, ignore_errors = True)
    #     print("COMP AUDIO DELETED")
    app()

if __name__ == "__main__":
    st.set_page_config(page_icon=":computer:", layout = "wide")
    st.write("<div style='text-align: center'><h1>Clear <em style='text-align: center; color: #238636;'>Speak</em></h1></div>", unsafe_allow_html=True)
    main()