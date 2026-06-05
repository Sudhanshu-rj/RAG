import streamlit as st
from pytubefix import YouTube
from pydub import AudioSegment
import os

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url: str) -> str:
    # use_po_token=True is the magic trick that bypasses the 403 Forbidden error!
    yt = YouTube(url, use_po_token=True)
    
    # Grab the highest quality audio-only stream
    audio_stream = yt.streams.get_audio_only()
    
    # Download the raw file (usually .m4a or .mp4)
    downloaded_file = audio_stream.download(output_path=DOWNLOAD_DIR)
    
    # Send it directly to your existing converter to make it a clean 16kHz WAV!
    wav_file = convert_to_wav(downloaded_file)
    
    # Optional: Delete the original downloaded file to save server space
    try:
        os.remove(downloaded_file)
    except:
        pass
        
    return wav_file


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        try:
            wav_path = download_youtube_audio(source)
        except Exception as e:
            # If YouTube blocks the cloud server, stop the pipeline gracefully
            st.error("🚨 YouTube aggressively blocked this cloud server's IP address. Please download the video/audio to your computer and upload the local file using the box on the left instead!")
            st.stop() # Stops the rest of the code from running and crashing
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks