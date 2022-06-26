import requests
import argparse
from moviepy.editor import AudioFileClip, ImageClip
from pathlib import Path

def downloadImage(url):
    r = requests.get(url, allow_redirects=True)
    open('picture.jpg', 'wb').write(r.content)


def downloadMusic(url):
    r = requests.get(url, allow_redirects=True)
    title = url.split("filename=")[1]
    index = title.rfind("-")
    print(title[:index])
    open('music.mp3', 'wb').write(r.content)


def add_static_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after
    combining a static image that is located in `image_path`
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(filename=audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    print("shape",image_clip.img.shape[0:2])
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS
    video_clip.fps = 1
    # set the resolution
    video_clip = video_clip.resize((1920,1080))#(image_clip.img.shape[1],image_clip.img.shape[0]))

    # write the resuling video clip
    video_clip.write_videofile(output_path)


downloadImage("https://pixabay.com/get/gdb98b996250656a544c89778d0e701e1df0fbcf402caac12478fced60125c2a3507c11e3fdf2ec133978185426e3e87e.jpg")
downloadMusic(
    "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3")

add_static_image_to_audio('picture.jpg', 'music.mp3', "output.mp4")
