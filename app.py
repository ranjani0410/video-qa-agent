from flask import Flask, request, jsonify
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import os
import requests

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/generate-qa', methods=['POST'])
def generate_qa():
    data = request.json
    video_url = data.get("url")

    # Download video
    yt = YouTube(video_url)
    video_path = yt.streams.filter(only_audio=True).first().download(filename="video.mp4")

    # Extract audio
    clip = VideoFileClip("video.mp4")
    clip.audio.write_audiofile("audio.mp3")

    # Transcribe
    result = model.transcribe("audio.mp3")
    transcript = result["text"]

    # Gemini API call
    api_key = os.environ.get("GEMINI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate 5 quiz questions with answers from the following transcript:\n{transcript}"
                    }
                ]
            }
        ]
    }
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
        headers=headers,
        json=payload
    )
    questions = response.json()['candidates'][0]['content']['parts'][0]['text']
    return jsonify({"questions": questions})
