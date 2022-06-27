import PySimpleGUI as sg
import requests
from moviepy.editor import AudioFileClip, ImageClip


class youtube_money_maker:

    def __init__(self):
        self.video_title = ""

    def downloadImage(self, url):
        r = requests.get(url, allow_redirects=True)
        open('picture.jpg', 'wb').write(r.content)

    def downloadMusic(self, url):
        r = requests.get(url, allow_redirects=True)
        title = url.split("filename=")[1]
        index = title.rfind("-")
        self.video_title = title[:index]
        open('music.mp3', 'wb').write(r.content)

    def add_static_image_to_audio(self, image_path, audio_path):
        """Create and save a video file to `output_path` after
        combining a static image that is located in `image_path`
        with an audio file in `audio_path`"""
        # create the audio clip object
        audio_clip = AudioFileClip(filename=audio_path)
        # create the image clip object
        image_clip = ImageClip(image_path)
        # use set_audio method from image clip to combine the audio with the image
        video_clip = image_clip.set_audio(audio_clip)
        # specify the duration of the new clip to be the duration of the audio clip
        video_clip.duration = audio_clip.duration
        # set the FPS
        video_clip.fps = 1
        # set the resolution
        video_clip = video_clip.resize((1920, 1080)).add_mask()  # (image_clip.img.shape[1],image_clip.img.shape[0]))

        # write the resuling video clip
        video_clip.write_videofile(f"OpenMusic - music for everyone [{self.video_title}].mp4")


if __name__ == '__main__':
    ymm = youtube_money_maker()

    layout = [[sg.Text("Image URL"),sg.In(do_not_clear=False)],[sg.Text("Audio URL"),sg.In(do_not_clear=False)],[sg.Button("Generate Music Video")]]
    window = sg.Window(title="Youtube Money Maker", layout=layout, margins=(250, 250))

    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Generate Music Video':
            print(values[0])
            if values[0] != "" and values[0].endswith(".jpg") and values[1] != "" and values[1].endswith(".mp3"):
                ymm.downloadImage(url=values[0])
                ymm.downloadMusic(url=values[1])
                ymm.add_static_image_to_audio('picture.jpg', 'music.mp3')
                sg.Popup('Finish', keep_on_top=True)
                values[0] = ""
                values[1] = ""

    window.Close()


