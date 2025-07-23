import streamlit as st
import subprocess
import os
import whisper
import google.generativeai as genai

# Set your Gemini API key here
GEMINI_API_KEY = "AIzaSyDbBMZAZfCHp8fhqdw7-DXI9PQqwbtkJ4E"
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Video Q&A Agent", layout="centered")
st.title("🎥 Video Q&A Agent")
st.markdown("Transcribe YouTube video audio and generate questions using Gemini.")

youtube_url = st.text_input("Enter YouTube Video URL:")

if st.button("Transcribe and Generate Questions"):
    if youtube_url:
        st.info("🔽 Downloading audio from YouTube...")
        try:
            result = subprocess.run(
                ["yt-dlp", "-x", "--audio-format", "mp3", youtube_url],
                capture_output=True, text=True
            )
            output = result.stdout + result.stderr

            audio_file = None
            for line in output.splitlines():
                if "Destination:" in line and line.strip().endswith(".mp3"):
                    audio_file = line.split("Destination: ")[-1].strip()
                    break
                elif "has already been downloaded" in line and line.strip().endswith(".mp3"):
                    audio_file = line.split("]")[-1].strip()
                    break

            if audio_file and os.path.exists(audio_file):
                st.success(f"✅ Audio ready: `{audio_file}`")

                # Transcribe using Whisper
                st.info("🧠 Transcribing audio using Whisper...")
                model = whisper.load_model("base")
                result = model.transcribe(audio_file)
                transcript = result["text"]

                # Show transcription
                st.subheader("📄 Transcription Result")
                st.text_area("Transcript:", transcript, height=250)

                # Generate questions using Gemini
                st.info("🧠 Generating questions using Gemini Pro...")

                prompt = (
                    "You are an AI that generates quiz-style questions for video learners. "
                    "Given this transcript, generate a list of 5-7 relevant and thoughtful questions:\n\n"
                    f"{transcript}\n\n"
                    "Return only the questions, numbered."
                )

                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)

                st.subheader("❓ Generated Questions")
                st.text_area("Questions:", response.text, height=250)
            else:
                st.error("❌ Audio download failed. Please check the YouTube URL.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a valid YouTube URL.")
