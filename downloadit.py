from pytube import YouTube

# Prompt the user to enter the URL of the YouTube video
url = input("Enter the URL of the YouTube video you want to download: ")

# Create a YouTube object
yt = YouTube(url)

# Get the highest resolution stream available
stream = yt.streams.get_highest_resolution()

# Download the video
print(f"Downloading: {yt.title}")
stream.download()
print("Download completed!")