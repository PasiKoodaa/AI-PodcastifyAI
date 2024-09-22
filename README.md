# AI PodcastifyAI

AI PodcastifyAI is an application that transforms scientific papers and web content into engaging podcast-style conversations using artificial intelligence. This tool leverages advanced language models and text-to-speech technology to create informative and accessible audio content from complex textual information.

## Features

- **Text Input**: Enter scientific text or a webpage URL directly into the application.
- **AI-Powered Dialogue Generation**: Utilizes KoboldCPP to generate a natural conversation between two speakers based on the input content.
- **Text-to-Speech Conversion**: Employs StyleTTS2 to convert the generated dialogue into lifelike speech.
- **Multi-Voice Support**: Creates a dynamic listening experience with distinct voices for different speakers.
- **Audiobook Creation**: Combines individual audio segments into a cohesive MP3 audiobook.
- **User-Friendly GUI**: Offers an intuitive interface for easy interaction and processing.

## Requirements

- Python 3.7+
- tkinter
- requests
- BeautifulSoup4
- StyleTTS2
- scipy
- pydub
- numpy
- tortoise-tts

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/PasiKoodaa/ai-podcastify.git
   cd ai-podcastify
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have KoboldCPP running locally on port 5001.

4. Prepare voice samples named `melinda_voice.wav` and `steve_voice.wav` for the two speakers.

## Usage

1. Run the application:
   ```
   python ai_podcastify.py
   ```

2. In the GUI:
   - Enter the text of a scientific paper or a webpage URL in the input area.
   - Click "Process" to generate the podcast dialogue.
   - Once processing is complete, click "Create Audiobook" to generate the MP3 file.

3. The resulting audiobook will be saved as `audiobook.mp3` in the same directory.

## How It Works

1. **Text Processing**: The app fetches content from the provided text or URL.
2. **Dialogue Generation**: KoboldCPP generates a conversational dialogue based on the input.
3. **Text-to-Speech**: StyleTTS2 converts the dialogue into speech for each speaker.
4. **Audio Compilation**: Individual audio segments are combined into a single MP3 file.

## Limitations

- Requires a local instance of KoboldCPP running on port 5001.
- Processing time may vary based on input length and system capabilities.
- Internet connection required for webpage content fetching.

## Acknowledgments

- KoboldCPP for dialogue generation
- StyleTTS2 for text-to-speech conversion
- All other open-source libraries used in this project

