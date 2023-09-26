from pytube import YouTube

# not used
def parse_srt(srt_text):
    """
    This function parses the SRT caption and returns plain text
    """
    lines = srt_text.split('\n')
    text_lines = [line for line in lines if not (line.strip().isdigit() or '-->' in line)]
    return ' '.join(text_lines)


# Prompt the user to enter the URL of the YouTube video
url = input("Enter the URL of the YouTube video you want to download: ")
import re

# Create a YouTube object
yt = YouTube(url)

# Set the base_file_name with the name of the video file with illegal or difficult characters removed
current_file_name = re.sub(r'[\\/*?:"<>|]', "", yt.title)


# Prompt the user to enter the base filename for saving the files
base_file_name = input("Enter the base filename for saving the files (hit enter for default): ")
if base_file_name == '':
    base_file_name = current_file_name

# Create a YouTube object
yt = YouTube(url)

# Get the available video streams and prompt the user to select the resolution
video_streams = yt.streams.filter(only_video=True, file_extension='mp4')
print("Available video resolutions:")
for i, stream in enumerate(video_streams):
    print(f"{i + 1}. {stream.resolution}")

selected = int(input("Enter the number of the resolution you want to download: ")) - 1
video_stream = video_streams[selected]

print(f"Downloading Video: {yt.title} in {video_stream.resolution} resolution")
video_stream.download(filename=f"{base_file_name}_.mp4")
print("Video Download completed!")

# Get the available audio streams and prompt the user to select the preferred one
audio_streams = yt.streams.filter(only_audio=True)
print("Available audio codecs:")
audio_streams_list = list(audio_streams)
for i, stream in enumerate(audio_streams_list):
    print(f"{i + 1}. {stream.abr} - {stream.audio_codec}")

selected = int(input("Enter the number of the audio codec you want to download: ")) - 1
audio_stream = audio_streams_list[selected]

print(f"Downloading Audio: {yt.title} in {audio_stream.abr} - {audio_stream.audio_codec}")
audio_stream.download(filename=f"{base_file_name}_.mp3")
print("Audio Download completed!")
