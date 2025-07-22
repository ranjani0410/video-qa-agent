import streamlit as st
import subprocess
import os
import whisper
import time

# Title
st.title("🎥 Video Q&A Agent")
st.markdown("Upload a YouTube video URL. We'll transcribe it and generate questions!")

# Input field
video_url = st.text_input("Enter YouTube video URL")

# Function to download audio using yt-dlp
def download_video_audio(url):
    try:
        audio_file = "downloaded_audio.%(ext)s"
        command = [
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "-o", audio_file,
            url
        ]
        subprocess.run(command, check=True)
        return "downloaded_audio.mp3"
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

# Placeholder for generated questions
def generate_questions(transcript):
    st.markdown("### ✨ Sample Questions (via Gemini)")
    st.info("Note: Questions will be generated using Gemini in your backend.")

    # Simulated placeholders for now:
    st.write("- What is the main topic of the video?")
    st.write("- What examples were discussed?")
    st.write("- What is the conclusion of the video?")

    # You can replace above with actual Gemini API call logic
    # Or paste questions from your external Gemini script

# Main logic
if video_url:
    st.info("⏳ Downloading audio from the video...")
    audio_path = download_video_audio(video_url)

    if audio_path and os.path.exists(audio_path):
        st.success("✅ Audio downloaded successfully!")

        st.info("🎧 Transcribing audio using Whisper...")
        transcript = transcribe_audio(audio_path)

        if transcript:
            st.success("✅ Transcription completed!")
            st.markdown("### 📝 Transcript")
            st.write(transcript)

            generate_questions(transcript)
        else:
            st.warning("⚠ Transcription failed.")
    else:
        st.warning("⚠ Audio file not found. Transcription skipped.")
