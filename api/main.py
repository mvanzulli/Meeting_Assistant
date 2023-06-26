import uvicorn
import sys
import os
from fastapi import FastAPI
from fastapi import UploadFile

sys.path.append(os.path.abspath('./model/'))
from model import summarize_and_translate, transcribe_audio

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "Record, transcribe, translate and summarize your meetings"}

@app.post("/transcribe/")
async def transcribe(file: UploadFile) -> dict:
    """
    Transcribes the audio file and returns the transcription and language.

    Args:
        file (UploadFile): The audio file to transcribe.

    Returns:
        A tuple containing the transcription and the language.
    """
    # Save the file to disk
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio
    transcript, language = transcribe_audio(file.filename)
    
    # Return the results as a tuple
    return {"text":transcript, "language":language}

@app.get("/translate&summarize_text/")
def summarize_text(text:str, language:str ="en") -> dict:
    text = summarize_and_translate(text, language)
    return {"text": text}

@app.post("/translate&summarize_audio/")
async def summarize_audio(file: UploadFile, language: str = "en") -> dict:
    """
    Transcribes an audio file and generates a summary of the resulting text.

    Args:
        file (UploadFile): The audio file to transcribe and summarize.
        language (str): The language of the text to summarize.

    Returns:
        A summary of the transcribed text.
    """
    # Transcribe the audio
    transcription = await transcribe(file)

    # Generate a summary of the text
    summary = summarize_text(transcription["text"], language)

    # Return the summary
    return summary

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="127.0.0.1")
