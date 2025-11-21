import streamlit as st 
from pydub import AudioSegment
import tempfile
import os
import speech_recognition as sr

def transcribe(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                file_path = tmpfile.name
                tmpfile.write(uploaded_file.read())

    c1.audio(uploaded_file, format="audio/wav")

    # Convert to WAV (Google API requires WAV)
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(file_path, format="wav")

    # Recognize speech
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        st.write("🔄 Transcribing... Please wait!")
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.success("✅ Transcription Complete!")
            c2.text_area("Transcribed Text:", text, height=100)
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ API error. Check internet connection.")

    # Clean up temp file
    os.remove(file_path)
    return "error"

text=""
st.set_page_config(page_title='Simply! Translate', 
                   page_icon='translator-icon.png', 
                   layout='wide', 
                   initial_sidebar_state='expanded')
st.markdown("<h1 style='text-align: center; color: grey;'>Speach to text transcriber</h1>", unsafe_allow_html=True)

c1,c2=st.columns(2)

uploaded_file2 = c2.audio_input("Record a voice message")
uploaded_file1 = c1.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
if uploaded_file1 is not None:
    # Save uploaded file temporarily
    if c1.button('transcibe', key='transcribe_btn_upload'):
        text=transcribe(uploaded_file1)

if uploaded_file2 is not None:
    # Save uploaded file temporarily
    if c2.button('transcibe',key='transcribe_btn_record'):
        text=transcribe(uploaded_file2)        
