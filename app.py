import streamlit as st
from pytube import YouTube
from faster_whisper import WhisperModel
from transformers import pipeline
import subprocess
import os

st.title("🎥 Video Q&A Agent")

option = st.radio("Choose video source:", ["Upload video", "Paste YouTube Link"])
video_path = ""

if option == "Upload video":
    video_file = st.file_uploader("Upload MP4 file", type=["mp4"])
    if video_file:
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        st.success("Video uploaded successfully.")

elif option == "Paste YouTube Link":
    yt_link = st.text_input("Paste YouTube URL")
    if yt_link:
        try:
            yt = YouTube(yt_link)
            video_stream = yt.streams.filter(file_extension="mp4").first()
            video_path = "yt_video.mp4"
            video_stream.download(filename=video_path)
            st.success("YouTube video downloaded successfully.")
        except Exception as e:
            st.error(f"Error downloading video: {e}")

if video_path and os.path.exists(video_path):
    st.video(video_path)

if st.button("Generate Questions from Video") and video_path:
    try:
        st.info("Extracting audio with ffmpeg...")

        audio_path = video_path.replace(".mp4", ".wav")
        subprocess.run(['ffmpeg', '-i', video_path, audio_path], check=True)

        st.success("Audio extracted.")

        st.info("Transcribing audio with Whisper...")
        model = WhisperModel("base")
        segments, _ = model.transcribe(audio_path)
        transcript = " ".join([seg.text for seg in segments])
        st.text_area("📝 Transcript:", transcript, height=200)

        st.info("Generating questions using FLAN-T5...")
        qg_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")
        input_text = f"Generate questions from this text: {transcript}"
        result = qg_pipeline(input_text, max_length=256)
        questions = result[0]['generated_text']

        st.markdown("## 🧠 Generated Questions:")
        for i, q in enumerate(questions.split("?")):
            q = q.strip()
            if q:
                st.write(f"**Q{i+1}:** {q}?")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
