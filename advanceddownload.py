from pytube import YouTube


def parse_srt(srt_text):
    """
    This function parses the SRT caption and returns plain text
    """
    lines = srt_text.split('\n')
    text_lines = [line for line in lines if not (line.strip().isdigit() or '-->' in line)]
    return ' '.join(text_lines)


# Prompt the user to enter the URL of the YouTube video
url = input("Enter the URL of the YouTube video you want to download: ")

# Prompt the user to enter the base filename for saving the files
base_file_name = input("Enter the base filename for saving the files: ")

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

# Get the first audio stream available and download it
audio_stream = yt.streams.filter(only_audio=True).first()
print(f"Downloading Audio: {yt.title}")
audio_stream.download(filename=f"{base_file_name}_mp3")
print("Audio Download completed!")

# Get the available captions
captions = yt.captions

# Get the available captions
# Get the available captions
captions = yt.captions

try:
    # If captions are available, prompt the user to select one, then download and save it
    if captions:
        print("Available captions:")
        captions_list = [{'code': code, 'name': caption.name} for code, caption in captions.items()]
        for i, caption in enumerate(captions_list):
            print(f"{i + 1}. {caption['name']} [{caption['code']}]")

        selected = int(input("Enter the number of the caption you want to download: ")) - 1
        selected_caption_code = captions_list[selected]['code']
        selected_caption = captions[selected_caption_code]

        # Save the caption to a file in plain text format
        with open(f"{base_file_name}_caption.txt", "w", encoding="utf-8") as f:
            f.write(parse_srt(selected_caption.generate_srt_captions()))
        print("Caption Download completed!")
    else:
        print("No captions available for this video.")
except Exception as e:
    print(f"An error occurred while processing captions: {str(e)}")

