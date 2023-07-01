#!/usr/bin/env python

import streamlit as st
import sys
import yaml
import requests
from typing import Tuple

sys.path.append("./model")

with open("./model/language_roles.yaml", "r") as f:
    language_roles = yaml.safe_load(f)
languages = list(language_roles.keys())


BASE_URL = "http://127.0.0.1:8000"  # Update with your API's base URL


# Function to call the API and get the summary
def summarize_audio(file, language) -> Tuple[str, str, str]:
    url = f"{BASE_URL}/translate_summarize_audio/?language={language}"
    files = {"file": file}
    response = requests.post(url, files=files).json()
    summary = response["summary"]
    transcription = response["transcription"]
    audio_language = response["audio_language"]
    return summary, transcription, audio_language


def main():
    st.title("Meeting Summarizer")

    # File Uploader for audio file
    audio_file = st.file_uploader("Upload Audio File (MP3)")

    # Language selection
    language = st.selectbox("Select Language", languages)

    # Generate summary button
    if st.button("Generate Summary"):
        if audio_file is not None:
            summary, transcription, audio_language = summarize_audio(
                audio_file, language
            )
            st.subheader("Summary:")
            st.write(summary)
            st.subheader("Transcription:")
            st.write(transcription)
            st.subheader("Audio Language:")
            st.write(audio_language)


if __name__ == "__main__":
    main()
