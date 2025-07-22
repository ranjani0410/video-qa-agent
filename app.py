import streamlit as st

st.title("🎥 Video Q&A Chatbot")

video_url = st.text_input("Enter YouTube video URL:")

if video_url:
    with st.spinner("Downloading and processing..."):
        audio_path = download_video_audio(video_url)
        transcript = transcribe_audio(audio_path)
        questions = generate_questions(transcript)

    st.success("Transcript and questions ready!")
    st.subheader("Transcript")
    st.write(transcript)

    st.subheader("Generated Questions")
    st.write(questions)

    st.chat_input("Ask a question about the video:")
