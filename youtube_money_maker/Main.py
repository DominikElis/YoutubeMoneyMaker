import PySimpleGUI as sg
import requests
from moviepy.editor import AudioFileClip, ImageClip
from moviepy.video.VideoClip import VideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


class youtube_money_maker:

    def __init__(self):
        self.video_title = ""

    def downloadImage(self, url):
        r = requests.get(url, allow_redirects=True)
        open('picture.jpg', 'wb').write(r.content)

    def downloadMusic(self, url):
        r = requests.get(url, allow_redirects=True)
        if "filename=" in url:
            title = url.split("filename=")[1]
            index = title.rfind("-")
            self.video_title = title[:index]
        open('music.mp3', 'wb').write(r.content)

    def downloadVideo(self, url):
        r = requests.get(url, allow_redirects=True)
        open('video.mp4', 'wb').write(r.content)

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
       

    def add_video_loop_to_audio(self, video_path, audio_path):
        """Create and save a video file to `output_path` after
        combining a static image that is located in `image_path`
        with an audio file in `audio_path`"""
        # create the audio clip object
        audio_clip = AudioFileClip(filename=audio_path)
        # create the image clip object
        video_clip = VideoFileClip(video_path)
        print("fps",video_clip.fps)
        print("res", video_clip.size)
        # loop the video
        video_clip = video_clip.loop(duration=audio_clip.duration)
        # use set_audio method from image clip to combine the audio with the image
        video_clip = video_clip.set_audio(audio_clip)
        # specify the duration of the new clip to be the duration of the audio clip
        video_clip.duration = audio_clip.duration
        # set the FPS
        #video_clip.fps = 60
        # set the resolution
        #video_clip = video_clip.resize((1920, 1080)).add_mask()  # (image_clip.img.shape[1],image_clip.img.shape[0]))

        # write the resuling video clip
        video_clip.write_videofile(filename=f"OpenMusic - music for everyone [{self.video_title}].mp4")


if __name__ == '__main__':
    ymm = youtube_money_maker()

    layout = [
        [
            [
                [sg.Text("Image URL"),sg.In(do_not_clear=False),sg.FileBrowse(key="image",button_text="Image")]
            ],
            [
                [sg.Text("Video URL"), sg.In(do_not_clear=False), sg.FileBrowse(key="video", button_text="Video")]
            ],
            [
                [sg.Text("Audio URL"),sg.In(do_not_clear=False),sg.FileBrowse(key="audio",button_text="Audio")]
            ],
            [
                [sg.Button("Generate Music Video"),sg.Button("Reset")]
            ]
        ]
    ]
    window = sg.Window(title="Youtube Money Maker", layout=layout, margins=(250, 250))
    valid_data_video = True
    valid_data_image = True
    while True:  # Event Loop

        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Generate Music Video':
            print(values[0])
            url_image = ""
            url_audio = ""
            url_video = ""
            if (values["image"] != "" and values["audio"] != ""):
                url_image = values["image"]
                url_audio = values["audio"]
                valid_data_image = True
                valid_data_video = False
            elif values["video"] != "" and values["audio"] != "":
                url_video = values["video"]
                url_audio = values["audio"]
                valid_data_video = True
                valid_data_image = False
            elif values[0] != "" and values[2] != "": #image
                url_image = values[0]
                url_audio = values[2]
                valid_data_image = True
                valid_data_video = False
            elif values[1] != "" and values[2] != "": #video
                url_video = values[1]
                url_audio = values[2]
                valid_data_video = True
                valid_data_image = False
            else:
                valid_data_image = False
                valid_data_video = False
            if valid_data_image:
                if url_image.startswith("http"):
                    ymm.downloadImage(url=url_image)
                    ymm.downloadMusic(url=url_audio)
                    url_image = 'picture.jpg'
                    url_audio = 'music.mp3'
                ymm.add_static_image_to_audio(url_image, url_audio)

                sg.Popup('Finish', keep_on_top=True)
            elif valid_data_video:
                if url_video.startswith("http"):
                    ymm.downloadVideo(url=url_video)
                    url_video = 'video.mp4'
                if url_audio.startswith("http"):
                    ymm.downloadMusic(url=url_audio)
                    url_audio = 'music.mp3'
                ymm.add_video_loop_to_audio(url_video,url_audio)
    window.Close()


