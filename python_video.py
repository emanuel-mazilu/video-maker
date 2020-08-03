from googletrans import Translator
from gtts import gTTS

import moviepy.editor as mpy
import gizeh as gz
from math import pi
from mutagen.mp3 import MP3

VIDEO_SIZE = (1280, 720)
BLUE = (59/255, 89/255, 152/255)
GREEN = (176/255, 210/255, 63/255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
BlACK = (0, 0, 0)

traducator = Translator()
expresiiArray = []
FILENAME = "expresii.txt"


with open(FILENAME) as f:
    for line in f:
        expresiiArray.append(line.rstrip())

initial_language = "en"
translate_language = "ro"


i = 1
# For evrey individual line in file create a video with audio
for text_netradus in expresiiArray:
    #translate text
    tradus = traducator.translate(text_netradus, dest=translate_language)
    print(text_netradus, " --> ", tradus.text)
    text_tradus = tradus.text

    #make audio files for the translated text
    #original text slow
    myobj = gTTS(text=text_netradus, lang=initial_language, slow=True)
    myobj.save("netradus" + ".mp3")
    #tramslated text
    myobj2 = gTTS(text=tradus.text, lang=translate_language, slow=False)
    myobj2.save("tradus" + ".mp3")
    #original text
    myobj3 = gTTS(text=text_netradus, lang=initial_language, slow=False)
    myobj3.save("netradus_fast" + ".mp3")
    #load audio files  
    audio1 = MP3("netradus.mp3")
    audio2 = MP3("tradus.mp3")
    audio3 = MP3("netradus_fast.mp3")

    DURATION = audio1.info.length + audio2.info.length + audio3.info.length
    print(DURATION)

    def render_text(t):
        surface = gz.Surface(1280, 300, bg_color=WHITE_GIZEH)
        # add original text to screen
        text1 = gz.text(
            text_netradus, fontfamily="Charter",
            fontsize=40, fontweight='bold', fill=BLUE, xy=(640, 40))
        text1.draw(surface)
        # add translated text to screen
        text2 = gz.text(
            text_tradus, fontfamily="Charter",
            fontsize=40, fontweight='bold', fill=BLUE, xy=(640, 200))
        text2.draw(surface)
        return surface.get_npimage()

    # meke video
    text = mpy.VideoClip(render_text, duration=DURATION)

    # load audio files to add them to video
    silence_half = mpy.AudioFileClip("0.5-second-of-silence.mp3")
    silence_sec = mpy.AudioFileClip("1-second-of-silence.mp3")
    video_audio1 = mpy.AudioFileClip("netradus.mp3")
    video_audio2 = mpy.AudioFileClip("tradus.mp3")
    video_audio3 = mpy.AudioFileClip("netradus_fast.mp3")

    # put all sounds together
    video_audio = mpy.concatenate_audioclips([silence_half, video_audio1, silence_half, video_audio2, silence_half, video_audio3, silence_sec])

    video = mpy.CompositeVideoClip([text.set_position('center')],
        size=VIDEO_SIZE).on_color(color=WHITE, col_opacity=1).set_audio(video_audio)

    video.write_videofile("video-" + str(i) + ".mp4", fps=10)
    i = i + 1

# combine all videos in one
clips = []

for i in range(1,len(expresiiArray)+1):
    clips.append(mpy.VideoFileClip("video-" + str(i) + ".mp4"))

final_clip = mpy.concatenate_videoclips([*clips])
final_clip.write_videofile("final_clip.mp4")