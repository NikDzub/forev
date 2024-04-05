from moviepy.editor import (
    ImageClip,
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx,
)
import os
import random
from PIL import Image


clip_w = 1080 / 2
clip_h = 1920 / 2


all_folders = os.listdir("./products")
for index, folder in enumerate(all_folders):
    image_files = os.listdir(f"./products/{folder}")
    try:
        image_files.remove("info.txt")
        image_files.remove(".DS_Store")
    except:
        pass
    if len(image_files) < 3:
        continue

    images = []

    for img in image_files:

        # check transp
        img_mode = Image.open(f"./products/{folder}/{img}")
        img = ImageClip(f"./products/{folder}/{img}")
        img = img.resize(width=clip_w - 20)
        img = img.set_duration(5)
        # if img_mode.mode != "RGBA" or img_mode.mode != "P":
        #     img = img.fx(vfx.margin, 5)
        images.append(img)

    images_clip = concatenate_videoclips(images, method="compose")

    # music_clip = AudioFileClip("relax_music.mp3")
    # music_clip.set_duration(10)

    bg_clips = os.listdir(f"./bg_clips")
    print(bg_clips)

    bg_clip = VideoFileClip(f"./bg_clips/{random.choice(bg_clips)}")
    bg_duration = bg_clip.duration
    bg_clip = bg_clip.without_audio()
    bg_clip = bg_clip.rotate(90)
    bg_clip = bg_clip.resize(width=clip_w, height=clip_h)

    start = random.randint(0, int(bg_duration - images_clip.duration))
    end = start + int(images_clip.duration)
    print(start, end)
    bg_clip = bg_clip.subclip(start, end)

    print(bg_clip.size)
    final_clip = CompositeVideoClip(
        clips=[bg_clip, images_clip.set_position("center")], size=bg_clip.size
    )

    final_clip.write_videofile(f"output_video{index}.mp4", fps=10)

    print(f"output_video{index}.mp4")
