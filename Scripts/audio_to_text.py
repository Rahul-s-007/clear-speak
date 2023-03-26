import openai

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG") 

#audio_file= open(f"{AUDIO_PATH}/speech.wav", "rb")
def transcript():
    audio_file= open("speech.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    #print(transcript)
    print(transcript['text'])
    return transcript['text']