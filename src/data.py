import subprocess
from yt_dlp import YoutubeDL
import os


# Step 1: Download the audio from YouTube
def download_audio(youtube_url, output_file):
    """
    Download audio from YouTube using yt-dlp.

    Parameters:
        youtube_url (str): URL of the YouTube video.
        output_file (str): Path to save the downloaded audio.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'ffmpeg_location': 'C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/',  # Path to FFmpeg binaries
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])        
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None

    print(f"Audio downloaded: {output_file}")
    return output_file


# Step 2: Split the audio into smaller segments
def split_audio(input_file, output_pattern, segment_time):
    """
    Split an audio file into smaller segments using FFmpeg.

    Parameters:
        input_file (str): Path to the input audio file.
        output_pattern (str): Pattern for output files (e.g., "segment_%03d.mp3").
        segment_time (int): Duration of each segment in seconds.
    """
    command = [
        'ffmpeg',
        '-i', input_file,
        '-f', 'segment',
        '-segment_time', str(segment_time),
        '-c', 'copy',
        output_pattern
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Audio split into segments with pattern: {output_pattern}")
    except subprocess.CalledProcessError as e:
        print(f"Error splitting audio: {e}")


# Step 3: Combine the audio segments into a single file
def combine_audio_files(segment_files, output_file):
    """
    Combine multiple audio files into a single file using FFmpeg.

    Parameters:
        segment_files (list): List of file paths to audio segments.
        output_file (str): Path to the combined output audio file.
    """
    try:
        # Create a temporary text file listing all segments
        list_file = "file_list.txt"
        with open(list_file, "w") as file_list:
            for segment in segment_files:
                file_list.write(f"file '{os.path.abspath(segment)}'\n")

        # FFmpeg command to concatenate audio files
        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",  # No re-encoding for faster processing
            output_file,
        ]

        subprocess.run(command, check=True)
        print(f"Successfully combined audio files into: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error while combining audio files: {e}")
    finally:
        # Clean up the temporary file list
        if os.path.exists(list_file):
            os.remove(list_file)


# Main Script
if __name__ == "__main__":
    # Input YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloaded_file = "full_audio.mp3"  # File to save the downloaded audio
    segment_pattern = "segment_%03d.mp3"  # Pattern for split segments
    combined_file = "combined_audio.mp3"  # Final output after merging
    segment_duration = 30  # Duration of each segment in seconds

    # Step 1: Download the audio
    audio_file = download_audio(youtube_url, downloaded_file)

    if audio_file:
        # Step 2: Split the audio into smaller batches
        split_audio(audio_file, segment_pattern, segment_duration)

        # Step 3: Gather segment files and combine them
        segment_files = sorted([f for f in os.listdir() if f.startswith("segment_") and f.endswith(".mp3")])
        combine_audio_files(segment_files, combined_file)

        # Optional: Cleanup individual segment files
        for segment in segment_files:
            os.remove(segment)
        print("All tasks completed successfully.")
