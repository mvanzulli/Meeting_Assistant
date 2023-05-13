import os
import sys
import time
import threading
import signal
import subprocess

import ffmpeg
import openai
import tiktoken
import torch
import whisper
from dotenv import load_dotenv

# 
OS = "linux"

# Model ann prompt to open ai 
WHISPER_MODEL = "base"

# Set the environment variable OPEN_API_KEY to your OpenAI API key
ENV_OPENAI_KEY = 'OPEN_API_KEY'

# GPT 3.5 Turbo
TEMPERATURE = 0.6
GPT_MODEL = "gpt-3.5-turbo"
GPT_ENCODER = "cl100k_base"
COMMAND_PROMPT = "Create clear and concise unlabelled bullet points summarizing the key information. Take notes if any future work has been mentioned"
COMMAND_ROLE = "You are a helpful assistant that summarizes text to small paragraphs"
SIZE_CHUNK = 2000

# Init clock
stop_timer = False

def record_meeting(output_filename):
    """
    Record a meeting using ffmpeg and display a ticker on the console.

    This function records the audio and saves it to a file specified by output_filename.
    It also displays a timmer on the console showing the elapsed time since the recording started.
    The clock updates every second until the recording is stopped by the user or an error occurs. 
    This function uses two threads to accomplish this.

    Args:
        output_filename (str): The name of the output file, including the file extension.

    Returns:
        None
    """   
    try:

        global stop_timer

        # Start the moving timmer in a different thread
        stop_timer = False
        timer_thread = threading.Thread(target=display_clock)
        timer_thread.start()

        # Record the audio using ffmpeg
        output_format = "mp3"

        if OS == "linux":
            stream = (
                ffmpeg
                .input('default', f='alsa', ac=2, video_size=None)
                .output(output_filename, acodec="libmp3lame", format=output_format)  # Specify the output format as 'mp3'
                .overwrite_output()
            )
        elif OS == "MAC":
            stream = (
                ffmpeg
                .input(":0", f="avfoundation", video_size=None)  # Use 'default'
                .output(output_filename, acodec="libmp3lame", format="mp3")  # Specify the output format as 'mp3'
                .overwrite_output()
            )


        # Start the process
        process = ffmpeg.run_async(stream, pipe_stdin=True, pipe_stderr=True)

        # Wait for the process to finish or be interrupted
        while process.poll() is None:
            time.sleep(1)

    except KeyboardInterrupt:

        stop_timer = True
        timer_thread.join()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait()

        print("Recording stopped.")
    except Exception as e:
        print(e)


def display_clock():
    """
    Displays a clock on the console showing the elapsed time since the function was called.
    The ticker updates every second until the global variable stop_timer is set to True.

    Args: None

    Returns: None
    """
    start_time = time.time()
    while not stop_timer:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        sys.stdout.write(f'\rRecording: {minutes:02d}:{seconds:02d}')
        sys.stdout.flush()
        time.sleep(1)


def transcribe_audio(filename):
    """Transcribe the audio from a file using a pre-trained whisper model.

    This function loads a pre-trained whisper model, loads the audio from a file specified by filename,
    and transcribes the audio using the model. The function then returns the transcribed text.

    Args:
        filename (str): The name of the audio file to transcribe.

    Returns:
        str: The transcribed text as a string.
    """
    # load model
    devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = whisper.load_model(WHISPER_MODEL, device=devices)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)

    print("Beginning Transcribing Process With Automatic Language Detection...")

    result = model.transcribe(audio, verbose=False, fp16=False, task="translate")

    return result['text']


def summarize_transcript(transcript):
    """
    Generate a summary of a transcript using OpenAI's GPT-3 language model.

    This function takes in a transcript (a string) and generates a summary of the text using OpenAI's GPT-3 language model.
    The transcript is broken up into smaller chunks of text to improve performance with the GPT-3 API.
    The summary is returned as a string.

    Args:
        transcript (str): The transcript to summarize.

    Returns:
        A string containing the summary of the transcript.
    """

    def generate_summary(prompt):
        """
        Generate a summary prompt using OpenAI's GPT-3 language model.

        This function takes in a prompt (a string) and generates a summary of the text using OpenAI's GPT-3 language model.
        The summary is returned as a string.

        Args:
            prompt (str): The prompt to summarize.

        Returns:
            A string containing the summary of the prompt.
        """
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": f"{COMMAND_ROLE}"},
                {"role": "user", "content": f"{COMMAND_PROMPT}: {prompt}"}
            ],
            temperature=TEMPERATURE,
        )
        return response.choices[0].message['content'].strip()

    # Initialize a list to store the smaller chunks of text
    chunks = []

    # Add a prompt to the beginning of the text, to be used in the GPT-3 request
    prompt = "Please summarize the following text:\n\n"

    # Add the prompt and transcript together to form the full text to summarize
    text = prompt + transcript

    # Encode the text into tokens using the GPT-3 tokenizer
    tokenizer = tiktoken.get_encoding(GPT_ENCODER)
    tokens = tokenizer.encode(text)

    # Split the tokens into smaller chunks to better fit the GPT-3 API's request size limit
    while tokens:
        chunk_tokens = tokens[:SIZE_CHUNK]
        # Convert the chunk back into text
        chunk_text = tokenizer.decode(chunk_tokens) 
        # Add the chunk to the list of chunks
        chunks.append(chunk_text)  
        # Move on to the next set of tokens
        tokens = tokens[SIZE_CHUNK:]

    summary = "\n".join([generate_summary(chunk) for chunk in chunks])

    return summary


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} [record|summarize] <output_file_name>.mp3")
        sys.exit(1)


    load_dotenv()
    api_key = os.getenv('OPEN_API_KEY')
    if api_key is None:
        print("Environment variable OPEN_API_KEY not found. Exiting...")
        sys.exit(1)

    openai.api_key = api_key

    action = sys.argv[1]
    output_filename = sys.argv[2]

    if action == "record":
        record_meeting(output_filename)
    elif action == "summarize":
        transcript = transcribe_audio(output_filename)
        summary = summarize_transcript(transcript)
        print(f"TRANSCRIPT:{transcript}\n")
        print(f"SUMMARY_START:\n{summary}\nSUMMARY_END\n")
    else:
        print(f"Invalid action. Usage: python {sys.argv[0]} [record|summarize] output.mp3")
        sys.exit(1)
