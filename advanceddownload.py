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



# Get the available video streams and prompt the user to select the resolution
#video_streams = yt.streams.filter(only_video=True, file_extension='mp4') #video no audio

video_streams = yt.streams.filter(progressive=True,file_extension='mp4').all()
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

#https://pypi.org/project/youtube-transcript-api/

# https://dev.to/azure/ai-using-whisper-to-convert-audio-to-text-from-my-podcast-episode-in-spanish-c96

transcript_yn = input("do you want to transcribe this video?\nThis takes a bit of time. (type 'y' and hit enter if you do.)")
if transcript_yn.lower() == 'y': 
    
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    import whisper

    import time
    
    sound_file = AudioSegment.from_mp3(f"/{base_file_name}_.mp3")
    audio_chunks = split_on_silence(sound_file, min_silence_len=1000, silence_thresh=-40 )
    count = len(audio_chunks)
    print("Audio split into " + str(count) + " audio chunks \n")

    # Call Whisper to transcribe audio
    model = whisper.load_model("base")
    transcript = ""
    for i, chunk in enumerate(audio_chunks):    
        if i < 10 or i > count - 10:
            out_file = "chunk{0}.wav".format(i)
            print("\r\nExporting >>", out_file, " - ", i, "/", count)
            chunk.export(out_file, format="wav")
            result = model.transcribe(out_file)
            transcriptChunk = result["text"]
            print(transcriptChunk)

            transcript += " " + transcriptChunk

    # Print transcript
    with open(f"{base_file_name}_transcript.txt", "w", encoding="utf-8") as file:
        file.write(transcript)

    print("\ntranscribed")

# also you can merge stuff with ffmpeg-python
# infile1 = ffmpeg.input("video.mp4")
# infile2 = ffmpeg.input("sound.mp3")

# merged  = ffmpeg.concat(infile1, infile2, v=1, a=1)
# output  = ffmpeg.output(merged[0], merged[1], "merged.mp4")