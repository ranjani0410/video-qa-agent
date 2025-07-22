import streamlit as st
from pytube import YouTube
from faster_whisper import WhisperModel
from transformers import pipeline
import os

# 1. Function to download audio from YouTube
def download_video_audio(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream is None:
            st.error("⚠ No audio stream found.")
            return None
        audio_file = "downloaded_audio.mp4"
        audio_stream.download(filename=audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# 2. Function to transcribe audio using Whisper
def transcribe_audio_whisper(audio_file):
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_file)
        transcript = " ".join(segment.text for segment in segments)
        return transcript
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

# 3. Function to generate questions using HuggingFace pipeline
def generate_questions_from_text(text):
    try:
        qa_pipeline = pipeline("question-generation")
        questions = qa_pipeline(text)
        return [q['question'] for q in questions]
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

# 4. Streamlit UI
st.title("🎥 Video Q&A Chatbot Agent")

video_url = st.text_input("Paste YouTube Video URL")

if st.button("Generate Q&A"):
    if not video_url:
        st.warning("Please paste a YouTube video URL.")
    else:
        st.info("🔄 Downloading audio...")
        audio_path = download_video_audio(video_url)

        if audio_path and os.path.exists(audio_path):
            st.success("✅ Audio downloaded successfully!")
            st.info("🧠 Transcribing audio...")
            transcript = transcribe_audio_whisper(audio_path)

            if transcript:
                st.success("✅ Transcription complete!")
                st.write("**Transcript:**")
                st.write(transcript)

                st.info("🧾 Generating questions...")
                questions = generate_questions_from_text(transcript)

                if questions:
                    st.success("✅ Questions generated!")
                    for i, q in enumerate(questions, 1):
                        st.write(f"**Q{i}:** {q}")
                else:
                    st.warning("No questions generated.")
            else:
                st.warning("⚠ Audio transcription failed.")
        else:
            st.warning("⚠ Audio file not found. Transcription skipped.")
