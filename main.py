import speech_recognition as sr
import subprocess
import os
import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')

from pydub import AudioSegment
import os



FOLDER_AUDIO = "audios"
FOLDER_VIDEOS = "videos"
FOLDER_TEXT = "texts"
LANGUAGE = ""

print("Iniciando...")

# Load the video file
videoFolderAndVideo = '{}'.format(FOLDER_VIDEOS)

videosPaths = [os.path.join(FOLDER_VIDEOS, nome) for nome in os.listdir(FOLDER_VIDEOS)]
files = [arq for arq in videosPaths if os.path.isfile(arq)]
mp4_files = [arq for arq in files if arq.lower().endswith(".mp4")]
print("Convertendo video em audio..")
for filename in mp4_files:
    audioFileName = filename.split(FOLDER_VIDEOS+"/")[1].split(".mp4")[0]
    print("Convertendo ",audioFileName)
    audioFileName = '{}/{}.wav'.format(FOLDER_AUDIO, audioFileName)
    video = AudioSegment.from_file(filename, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(audioFileName, format="wav")
print("Videos convertidos")

if not os.path.isdir(FOLDER_AUDIO):
    os.mkdir(FOLDER_AUDIO)
    
if not os.path.isdir(FOLDER_TEXT):
    os.mkdir(FOLDER_TEXT)

paths = [os.path.join(FOLDER_AUDIO, nome) for nome in os.listdir(FOLDER_AUDIO)]
files = [arq for arq in paths if os.path.isfile(arq)]
wav_files = [arq for arq in files if arq.lower().endswith(".wav")]

print("Iniciando transcrição...")

for filename in wav_files:
    print("Iniciando",filename)
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("Audio",source)
        audio = r.record(source)

    command = r.recognize_google(audio, language=LANGUAGE)

    print("Trabalhando o arquivo {}".format(filename))

    filefinal = filename.split("audios/")[1].split(".wav")[0]
    filefinal = '{}/{}.txt'.format(FOLDER_TEXT, filefinal)
    with open(filefinal, 'w') as arq:
        arq.write((command))

    print("Novo arquivo terminado {}".format(filefinal))

print("Tudo pronto")