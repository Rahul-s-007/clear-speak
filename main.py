import streamlit as st

import os
import shutil

import Scripts.summary
import Scripts.record_speech
import Scripts.audio_to_text
import Scripts.text_to_speech

USER_AUDIO = "speech.wav"
COMP_AUDIO = "comp.wav"

st.set_page_config(page_icon=":computer:", layout = "wide")

st.write("<div style='text-align: center'><h1>Clear <em style='text-align: center; color: #238636;'>Speak</em></h1></div>", unsafe_allow_html=True)

def app():
    # call all impprts one by one 
    pass
    

def main():
    if os.path.exists(USER_AUDIO):
        shutil.rmtree(path = USER_AUDIO, ignore_errors = True)
        print("USER AUDIO DELETED")

    if os.path.exists(COMP_AUDIO):
        shutil.rmtree(path = COMP_AUDIO, ignore_errors = True)
        print("COMP AUDIO DELETED")

    app()

if __name__ == "__main__":
    main()