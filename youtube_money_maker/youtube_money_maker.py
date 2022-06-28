import PySimpleGUI as sg
import requests
from moviepy.editor import AudioFileClip, ImageClip


class youtube_money_maker:

    def __init__(self):
        self.video_title = ""

    def downloadImage(self, url):
        try:
            r = requests.get(url, allow_redirects=True)
            open('picture.jpg', 'wb').write(r.content)
        except:
            return False
        return True

    def downloadMusic(self, url):
        try:
            r = requests.get(url, allow_redirects=True)
            title = url.split("filename=")[1]
            index = title.rfind("-")
            self.video_title = title[:index]
            open('music.mp3', 'wb').write(r.content)
        except:
            return False
        return True

    def add_static_image_to_audio(self):
        try:
            """Create and save a video file to `output_path` after
            combining a static image that is located in `image_path`
            with an audio file in `audio_path`"""
            # create the audio clip object
            audio_clip = AudioFileClip(filename="music.mp3")
            # create the image clip object
            image_clip = ImageClip("picture.jpg")
            # use set_audio method from image clip to combine the audio with the image
            video_clip = image_clip.set_audio(audio_clip)
            # specify the duration of the new clip to be the duration of the audio clip
            video_clip.duration = audio_clip.duration
            # set the FPS
            video_clip.fps = 1
            # set the resolution
            video_clip = video_clip.resize((1920, 1080)).add_mask()  # (image_clip.img.shape[1],image_clip.img.shape[0]))

            # write the resuling video clip
            file_name = f"OpenMusic - music for everyone [{self.video_title}].mp4"
            video_clip.write_videofile(file_name)
        except:
            return False
        return True, file_name

