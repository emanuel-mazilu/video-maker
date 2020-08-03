from googletrans import Translator
from gtts import gTTS

import moviepy.editor as mpy
import gizeh as gz
from mutagen.mp3 import MP3

VIDEO_SIZE = (1280, 720)
BLUE = (59/255, 89/255, 152/255)
GREEN = (176/255, 210/255, 63/255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
BlACK = (0, 0, 0)

translator = Translator()
word_list = []
FILENAME = "words.txt"

with open(FILENAME) as f:
    for line in f:
        word_list.append(line.rstrip())

initial_language = "en"
translate_language = "ro"

# video counter (used in nameing the files)
v_counter = 1
# For evrey individual line in file create a video with audio
for untranslated_text in word_list:
    # translate text
    translator_object = translator.translate(untranslated_text, dest=translate_language)
    print(untranslated_text, " --> ", translator_object.text)
    translated_text = translator_object.text

    # make audio files for the translated text
    # original text slow
    myobj = gTTS(text=untranslated_text, lang=initial_language, slow=True)
    myobj.save("untranslated" + ".mp3")
    # tramslated text
    myobj2 = gTTS(text=translator_object.text, lang=translate_language, slow=False)
    myobj2.save("translated" + ".mp3")
    # original text
    myobj3 = gTTS(text=untranslated_text, lang=initial_language, slow=False)
    myobj3.save("untranslated_fast" + ".mp3")
    # load audio files  
    audio1 = MP3("untranslated.mp3")
    audio2 = MP3("translated.mp3")
    audio3 = MP3("untranslated_fast.mp3")

    DURATION = audio1.info.length + audio2.info.length + audio3.info.length

    def render_text(t):
        surface = gz.Surface(1280, 300, bg_color=WHITE_GIZEH)
        # add original text to screen
        text1 = gz.text(
            untranslated_text, fontfamily="Charter",
            fontsize=40, fontweight='bold', fill=BLUE, xy=(640, 40))
        text1.draw(surface)
        # add translated text to screen
        text2 = gz.text(
            translated_text, fontfamily="Charter",
            fontsize=40, fontweight='bold', fill=BLUE, xy=(640, 200))
        text2.draw(surface)
        return surface.get_npimage()

    # meke video
    text = mpy.VideoClip(render_text, duration=DURATION)

    # load audio files to add them to video
    silence_half = mpy.AudioFileClip("0.5-second-of-silence.mp3")
    silence_sec = mpy.AudioFileClip("1-second-of-silence.mp3")
    video_audio1 = mpy.AudioFileClip("untranslated.mp3")
    video_audio2 = mpy.AudioFileClip("translated.mp3")
    video_audio3 = mpy.AudioFileClip("untranslated_fast.mp3")

    # put all sounds together
    video_audio = mpy.concatenate_audioclips([silence_half, video_audio1, silence_half, video_audio2,
                                              silence_half, video_audio3, silence_sec])

    video = mpy.CompositeVideoClip([text.set_position('center')],
        size=VIDEO_SIZE).on_color(color=WHITE, col_opacity=1).set_audio(video_audio)

    video.write_videofile("video-" + str(v_counter) + ".mp4", fps=10)
    v_counter = v_counter + 1

# combine all videos in one
clips = []

for i in range(1,len(word_list)+1):
    clips.append(mpy.VideoFileClip("video-" + str(v_counter) + ".mp4"))

final_clip = mpy.concatenate_videoclips([*clips])
final_clip.write_videofile("final_clip.mp4")