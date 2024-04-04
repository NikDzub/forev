from moviepy.editor import *
import os

all_folders = os.listdir("./products")
for folder in all_folders:

    image_files = os.listdir(f"./products/{folder}")
    try:
        image_files.remove("info.txt")
        image_files.remove(".DS_Store")
    except:
        pass

    print(image_files)

    if len(image_files) < 2:
        continue

    # Load images
    images = [
        ImageClip(f"./products/{folder}/{img}").set_duration(2) for img in image_files
    ]  # Set duration for each image (2 seconds in this case)

    # Concatenate images into a video clip
    video_clip = concatenate_videoclips(images, method="compose")

    # Load background music
    music_clip = AudioFileClip("starlilpeep.mp3")
    music_clip.set_duration(10)

    # Set the audio for the video clip
    video_clip = video_clip.set_audio(music_clip)

    # Write the final video file
    video_clip.write_videofile("output_video.mp4", fps=24)  # Adjust fps if needed

    print("break")
    break
