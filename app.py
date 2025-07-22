import streamlit as st
from pytube import YouTube
import os
from faster_whisper import WhisperModel

# Define function to download audio
def download_video_audio(video_url):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    output_file = stream.download(filename="audio.mp4")
    return output_file

# Define function to transcribe audio
def transcribe_audio(audio_path):
    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    transcription = " ".join([segment.text for segment in segments])
    return transcription

# Streamlit UI
st.title("🎧 Video Q&A Agent")
video_url = st.text_input("Enter YouTube video URL:")

if video_url:
    with st.spinner("Downloading audio..."):
        try:
            audio_path = download_video_audio(video_url)
            st.success("Audio downloaded successfully.")
        except Exception as e:
            st.error(f"Error downloading audio: {e}")

    with st.spinner("Transcribing..."):
        try:
            transcription = transcribe_audio(audio_path)
            st.text_area("Transcription", transcription, height=300)
        except Exception as e:
            st.error(f"Error in transcription: {e}")

    # Placeholder for Q&A generation using Gemini (coming next)
    st.info("Q&A generation will be added next.")
