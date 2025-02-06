from utilties.mp3_to_web_converter import wav_converter
from utilties.trancripter import Transcriber
from yt_dlp import YoutubeDL
import yt_dlp
import os
from pytube import YouTube 
import sys
print(sys.path)


def get_video_title(youtube_url):  
    ydl_opts = {
        'quiet': True,  
        'format': 'best' 
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video information
            video_info = ydl.extract_info(youtube_url, download=False)

            # Retrieve and print the title
            video_title = video_info.get('title', 'Unknown Title')
            return "".join(video_title.split())+".mp3"
        except Exception as e:
            print(f"An error occurred: {e}")
def download_audio(youtube_url, output_file):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': rf"C:\Users\Naman Agrawal\OneDrive\Documents\Final_year project\Clipscript\vedio_data\{output_file}",
    'ffmpeg_location': 'C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/',  # Path to FFmpeg binaries
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])        
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading audio: {e}")
            sys.exit()
        

    return output_file

# Usage
youtube_url = "https://youtube.com/shorts/k5Y1n7VPbeM?si=pLPCQp1-ydVY77By"
audio_file = get_video_title(youtube_url=youtube_url)
print(audio_file)

audio_file = download_audio(youtube_url, audio_file)
file = wav_converter(audio_file)
data = Transcriber(file)


