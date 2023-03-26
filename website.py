import streamlit as st 

import Scripts.rec_audio
import Scripts.audio_to_text
import Scripts.summary
import Scripts.text_to_speech

import requests
from PIL import Image
#import json
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Clear Speak")

st.write("<div style='text-align: center'><h1>Clear Speak</h1></div>", unsafe_allow_html=True)

col1,col2 = st.columns(2)

with col1:

    input_text = st.text_area("Enter script for the speech",placeholder="Your speech.....")
    
    #st.write(summary.summary)

    st.button("Record/Stop")

    st.audio('speech.wav')



with col2:

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url = "https://assets8.lottiefiles.com/packages/lf20_1pjemuh2.json"
    lottie = load_lottieurl(lottie_url)

    st_lottie(lottie, key="hello")


st.write("<div style='text-align: center'><h2>Analytics</h2></div>", unsafe_allow_html=True)


