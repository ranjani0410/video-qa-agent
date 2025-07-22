import streamlit as st
from pytube import YouTube
from faster_whisper import WhisperModel
from transformers import pipeline
import os

# Function to download audio from YouTube video
def download_video_audio(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            raise Exception("No audio stream found.")
        audio_path = stream.download(filename="downloaded_audio.mp3")
        return audio_path
    except Exception as e:
        raise Exception(f"Error downloading audio: {e}")

# Function to transcribe audio using faster-whisper
def transcribe_audio(audio_path):
    try:
        model = WhisperModel("base", compute_type="int8")
        segments, _ = model.transcribe(audio_path)
        transcription = " ".join(segment.text for segment in segments)
        return transcription
    except Exception as e:
        raise Exception(f"Error during transcription: {e}")

# Function to generate questions using HuggingFace transformers
def generate_questions(text):
    try:
        question_generator = pipeline("text2text-generation", model="iarfmoose/t5-base-question-generator")
        questions = question_generator(text, max_length=128, do_sample=False, num_return_sequences=5)
        return [q['generated_text'] for q in questions]
    except Exception as e:
        raise Exception(f"Error generating questions: {e}")

# Streamlit UI
st.title("🎥 Video Q&A Agent")
st.write("Enter a YouTube video URL. This agent will download the audio, transcribe it, and generate questions.")

video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    audio_path = None
    try:
        with st.spinner("📥 Downloading audio..."):
            audio_path = download_video_audio(video_url)
            st.success("✅ Audio downloaded!")
    except Exception as e:
        st.error(str(e))

    if audio_path and os.path.exists(audio_path):
        try:
            with st.spinner("📝 Transcribing..."):
                transcription = transcribe_audio(audio_path)
                st.success("✅ Transcription completed!")
                st.text_area("Transcript", transcription, height=300)

                with st.spinner("🧠 Generating questions..."):
                    questions = generate_questions(transcription)
                    st.success("✅ Questions generated!")
                    st.write("### Sample Questions:")
                    for i, q in enumerate(questions, 1):
                        st.write(f"{i}. {q}")

        except Exception as e:
            st.error(str(e))
    else:
        st.warning("⚠ Audio file not found. Transcription skipped.")
