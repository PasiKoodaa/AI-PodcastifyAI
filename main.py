import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import requests
from bs4 import BeautifulSoup
from StyleTTS2 import msinference
from scipy.io.wavfile import write
import os
from pydub import AudioSegment
import numpy as np
from tortoise.utils.text import split_and_recombine_text
import threading

def send_to_koboldcpp(text):
    url = "http://localhost:5001/api/v1/generate"
    
    system_prompt = "\nEND\n\nYour mission: Create a dialogue between two people in a podcast format based on the previous scientific paper. Melinda, the host, and Steve, the guest speaker is an expert in the field but not the author of the paper, should engage in a conversation to discuss and simplify the paper's content for the listeners. The aim is to make the scientific information accessible and understandable for the audience."
    
    full_text = text + system_prompt
    
    data = {
        "prompt": full_text,
        "max_context_length": 64000,
        "max_length": 32000,
        "temperature": 0.3
    }
    try:
        response = requests.post(url, json=data)
        return response.json()["results"][0]["text"]
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error fetching webpage: {str(e)}"

def create_audio(text, voice_file, output_file, max_chars=300):
    try:
        voice = msinference.compute_style(voice_file)
        
        if len(text) > max_chars:
            texts = split_and_recombine_text(text)
            audios = []
            for t in texts:
                wav = msinference.inference(t, voice, alpha=0.3, beta=0.7, diffusion_steps=7, embedding_scale=1)
                audios.append(wav)
            combined_wav = np.concatenate(audios)
        else:
            combined_wav = msinference.inference(text, voice, alpha=0.3, beta=0.7, diffusion_steps=7, embedding_scale=1)
        
        write(output_file, 24000, combined_wav)
        print(f"Created audio file: {output_file}")
    except Exception as e:
        print(f"Error creating audio for '{text}': {str(e)}")
        raise

def create_audiobook(dialogue):
    lines = dialogue.split('\n')
    audio_files = []
    current_speaker = None
    current_text = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith("Melinda:") or line.startswith("Steve:"):
            # Process the previous speaker's text if there is any
            if current_speaker and current_text:
                output_file = f'temp_{current_speaker.lower()}_{len(audio_files)}.wav'
                create_audio(current_text.strip(), f'{current_speaker.lower()}_voice.wav', output_file)
                audio_files.append(output_file)
            
            # Set the new current speaker and start new text
            current_speaker = line.split(':')[0]
            current_text = line.split(':', 1)[1].strip() + " "
        elif current_speaker:
            # If there's a current speaker, add this line to their text
            current_text += line + " "
        # Ignore lines that don't have a speaker and appear before any speaker is set
    
    # Process the last speaker's text if there is any
    if current_speaker and current_text:
        output_file = f'temp_{current_speaker.lower()}_{len(audio_files)}.wav'
        create_audio(current_text.strip(), f'{current_speaker.lower()}_voice.wav', output_file)
        audio_files.append(output_file)

    if not audio_files:
        print("No audio files were created successfully.")
        return

    combined = AudioSegment.empty()
    for audio_file in audio_files:
        try:
            segment = AudioSegment.from_wav(audio_file)
            combined += segment
            print(f"Added {audio_file} to the audiobook")
        except Exception as e:
            print(f"Error combining audio file {audio_file}: {str(e)}")
            continue

    try:
        combined.export("audiobook.mp3", format="mp3")
        print("Audiobook created successfully.")
    except Exception as e:
        print(f"Error exporting audiobook: {str(e)}")

    # Clean up temporary files
    for audio_file in audio_files:
        try:
            os.remove(audio_file)
        except Exception as e:
            print(f"Error removing temporary file {audio_file}: {str(e)}")

def create_audiobook_from_output():
    output_text = output_area.get("1.0", tk.END).strip()
    set_processing(True)
    threading.Thread(target=create_audiobook_thread, args=(output_text,)).start()

def create_audiobook_thread(output_text):
    create_audiobook(output_text)
    root.after(0, lambda: messagebox.showinfo("Audiobook Created", "Audiobook has been created and saved as 'audiobook.mp3'"))
    root.after(0, lambda: set_processing(False))

def process_input():
    input_text = input_area.get("1.0", tk.END).strip()
    set_processing(True)
    threading.Thread(target=process_input_thread, args=(input_text,)).start()

def process_input_thread(input_text):
    if input_text.startswith("http://") or input_text.startswith("https://"):
        content = fetch_webpage_content(input_text)
    else:
        content = input_text
    
    response = send_to_koboldcpp(content)
    root.after(0, lambda: update_output(response))
    root.after(0, lambda: set_processing(False))

def update_output(text):
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, text)

def set_processing(is_processing):
    if is_processing:
        process_button.config(state=tk.DISABLED)
        audiobook_button.config(state=tk.DISABLED)
        loading_label.pack()
        root.update_idletasks()
    else:
        process_button.config(state=tk.NORMAL)
        audiobook_button.config(state=tk.NORMAL)
        loading_label.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Text Processing GUI with Audiobook Creation")
root.geometry("800x700")

# Create input area
input_label = tk.Label(root, text="Enter text or webpage URL:")
input_label.pack(pady=5)
input_area = scrolledtext.ScrolledText(root, height=10)
input_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create process button
process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack(pady=10)

# Create output area
output_label = tk.Label(root, text="Output:")
output_label.pack(pady=5)
output_area = scrolledtext.ScrolledText(root, height=15)
output_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Create audiobook button
audiobook_button = tk.Button(root, text="Create Audiobook", command=create_audiobook_from_output)
audiobook_button.pack(pady=10)

# Create loading label
loading_label = tk.Label(root, text="Processing... Please wait.")
loading_label.pack_forget()

# Start the GUI event loop
root.mainloop()
