# 🎙️ Meeting Helper

This program provides functionality to record meetings and then generate summaries of the transcribed audio using OpenAI's GPT-3 language model.

## 🚀 Prerequisites

To run this program, you will need:

- `Python 3.7` or higher
- `ffmpeg` installed on your system




<details>
<summary>## 🔧 Installation

  1. Clone this repository
  2. Install the required Python modules using `pip install -r requirements.txt`
    1. `python3 -m venv .venv`
    2. `source .venv/bin/activate`
    3. `pip install -r requirements.txt`
  3. Create a ENVIROMENT VARIABLE and add your OpenAI API key as described below

</details>

2. Install the required Python modules using `pip install -r requirements.txt`

## 🛠️ Usage

### Record

To record a meeting, run:

```
python program.py record <output_file_name>.mp3
```

This will record the audio and save it to a file with the specified name.

### Summarize

To generate a summary of an audio file, run:

```
python program.py summarize <audio_file_name>.mp3
```

This will generate a summary of the transcribed audio using OpenAI's GPT-3 language model.

### Translate and Summarize

To generate a summary of an audio file and translate it into English, run:

```
python program.py translate_and_summarize <audio_file_name>.mp3
```

This will generate a summary of the transcribed audio using OpenAI's GPT-3 language model and translate it into English.

## 🔑 Required Environment Variables

This program requires an OpenAI API key to function. To set up your environment variables:

1. Create a new file named `.env` in the root of this directory
2. Add the following line to your `.env` file: `OPEN_API_KEY=<your_api_key>`
3. Replace `<your_api_key>` with your actual OpenAI API key.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💼 Variables to Tune

This program has several variables that can be tuned to change its behavior. These variables are declared at the beginning of the program:

- `OS`: Set this to `"linux"` or `"MAC"` depending on your operating system.
- `DEVICE`: Set this to `"cuda:0"` if you have an NVIDIA GPU and want to use it to accelerate processing, or `"cpu"` to use the CPU instead.
- `WHISPER_MODEL`: The name of the pre-trained Whisper model to use for transcribing the audio.
- `ENV_OPENAI_KEY`: The name of the environment variable that contains your OpenAI API key.
- `TEMPERATURE`: The "temperature" parameter to use when generating summaries with GPT-3. Higher values will generate more diverse summaries, while lower values will generate more conservative summaries.
- `GPT_MODEL`: The name of the GPT-3 language model to use for generating summaries.
- `GPT_ENCODER`: The name of the GPT-3 tokenizer to use for encoding text.
- `COMMAND_PROMPT`: The prompt to use when requesting a summary from GPT-3.
- `COMMAND_ROLE`: The role of the user in the GPT-3 conversation (e.g., "helpful assistant").
- `SIZE_CHUNK`: The size of each "chunk" of text to send to GPT-3 for summarization. Larger chunks will result in fewer requests to the API, but may be slower to process.
