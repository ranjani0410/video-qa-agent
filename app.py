import streamlit as st
import tempfile
import os
import yt_dlp
import whisper
import requests

# Gemini API setup
GEMINI_API_KEY = "AIzaSyCttlItCvXn5QYuFabAHuHrICddtMBBP7M"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

# Step 1: Download audio
def download_video_audio(video_url):
    try:
        st.info("⏳ Downloading audio from the video...")
        temp_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_audio_file.name,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        st.success("✅ Audio downloaded successfully!")
        return temp_audio_file.name
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# Step 2: Transcribe with Whisper
def transcribe_audio(audio_path):
    try:
        st.info("🎧 Transcribing audio using Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        st.success("✅ Transcription completed.")
        return result["text"]
    except Exception as e:
        st.error(f"Error in transcription: {e}")
        return None

# Step 3: Generate questions using Gemini
def generate_questions_from_text(text):
    st.info("🧠 Generating questions using Gemini Pro...")
    headers = {"Content-Type": "application/json"}
    prompt = f"Generate 5 simple and useful questions based on the following transcript:\n\n{text}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
        questions = parts[0]["text"].split('\n')
        st.success("✅ Questions generated.")
        return [q.strip() for q in questions if q.strip()]
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

# Streamlit UI
st.title("🎥 Video Q&A Agent")
video_url = st.text_input("Enter YouTube Video URL")

if st.button("🔍 Process Video"):
    if video_url:
        audio_path = download_video_audio(video_url)
        if audio_path:
            transcript = transcribe_audio(audio_path)
            if transcript:
                st.subheader("📝 Transcript")
                st.write(transcript)

                questions = generate_questions_from_text(transcript)
                st.subheader("❓ Generated Questions")
                for i, q in enumerate(questions, 1):
                    st.write(f"{i}. {q}")
            else:
                st.warning("⚠ Transcription failed.")
        else:
            st.warning("⚠ Audio file not found. Transcription skipped.")
    else:
        st.warning("⚠ Please enter a valid YouTube video URL.")
