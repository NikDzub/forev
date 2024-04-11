#!/usr/bin/env python3

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

# int(1080 / 2)
clip_w = int(1080)
clip_h = int(1920)

bg_clips = os.listdir(f"./bg_clips")
ol_clips = os.listdir(f"./overlay_clips")
all_folders = os.listdir("./products")


for index, folder in enumerate(all_folders):
    image_files = os.listdir(f"./products/{folder}")
    #
    #
    #
    removes = [
        "info.txt",
        ".DS_Store",
        "product_video.mp4",
        "icons_info.png",
        "product_video_0.mp4",
    ]
    for r in removes:
        try:
            image_files.remove(r)
        except:
            pass
    if len(image_files) < 3:
        continue
    #
    #
    #
    # ------------- images clip -------------
    images = []
    for img in image_files:
        img = ImageClip(f"./products/{folder}/{img}")
        img = img.resize(width=clip_w - 100).set_duration(4)

        # check transp
        # img_mode = Image.open(f"./products/{folder}/{img}")
        # if img_mode.mode != "RGBA" or img_mode.mode != "P":
        #     img = img.fx(vfx.margin, 5)
        images.append(img)

    random.shuffle(images)
    images_clip = concatenate_videoclips(images, method="compose")
    images_clip = images_clip.rotate(random.randint(-5, 5))
    # ------------- images clip -------------
    #
    #
    #
    # ------------- bg clip -------------
    bg_clip = VideoFileClip(f"./bg_clips/{random.choice(bg_clips)}")
    bg_start = random.randint(10, int(bg_clip.duration - images_clip.duration))
    bg_end = bg_start + int(images_clip.duration)

    bg_clip = (
        bg_clip.without_audio()
        .rotate(90)
        .resize(width=clip_w, height=clip_h)
        .subclip(bg_start, bg_end)
    )
    # ------------- bg clip -------------
    #
    #
    #
    # ------------- overlay clip -------------
    ol_clip = VideoFileClip(f"./overlay_clips/{random.choice(ol_clips)}")
    ol_clip = (
        ol_clip.rotate(90)
        .set_opacity(0.2)
        .without_audio()
        .resize(width=clip_w, height=clip_h)
        .subclip(0, int(images_clip.duration))
    )
    # ------------- overlay clip -------------
    #
    #
    #
    # ------------- icons_info clip -------------
    icons_info = ImageClip(f"./products/{folder}/icons_info.png")
    icons_info = (
        icons_info.resize(width=clip_w - 100)
        .set_duration(images_clip.duration)
        .resize(width=clip_w)
        .fx(vfx.margin, bottom=1, color=(0, 0, 0))
        # .fx(vfx.rotate, 90)
    )
    # ------------- icons_info clip -------------
    #
    #
    #
    # ------------- wave clip -------------
    waves_clip = VideoFileClip(f"./etc/waves.mp4")
    waves_clip = concatenate_videoclips([waves_clip] * 3)
    waves_clip = (
        waves_clip.rotate(90)
        .set_opacity(0.1)
        .without_audio()
        .resize(width=clip_w, height=clip_h)
        .subclip(0, int(images_clip.duration))
    )
    # ------------- wave clip -------------
    #
    #
    #
    # ------------- bg music -------------
    music_clip = AudioFileClip("./etc/bg_music.mp3")
    music_start = random.randint(
        10, int(music_clip.duration) - int(images_clip.duration)
    )
    music_end = music_start + int(images_clip.duration)
    music_clip = music_clip.subclip(music_start, music_end)
    bg_clip = bg_clip.set_audio(music_clip)
    # ------------- bg music -------------
    #
    #
    #
    final_clip = CompositeVideoClip(
        clips=[
            bg_clip.set_position("center"),
            waves_clip.set_position("center"),
            images_clip.set_position("center"),
            icons_info.set_position("top"),
            ol_clip.set_position("center"),
        ],
        size=(clip_w, clip_h),
    )
    #
    #
    #
    final_clip.write_videofile(f"./products/{folder}/product_video_1.mp4", fps=30)
    # final_clip.write_videofile(f"./trash/product_video{index}.mp4", fps=10)
    print(f"./products/{folder}/product_video.mp4")
