from __future__ import unicode_literals
import youtube_dl
import sys
import os
import speech_recognition as sr
import subprocess as sp

print 'YouTube Transcriptor'
print '---------------------'


class MyLogger(object):
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass

    def error(self, msg):
        print msg

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting...')

def download_as_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': 'transcript.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_to_text():
    print 'Transcribing....'
    print '----------------'

    cmdline = [
            'avconv',
            '-i',
            'transcript.mp3',
            '-vn',
            '-f',
            'wav',
            'text.wav'
            ]

    sp.call(cmdline)
    
    r = sr.Recognizer()
    with sr.AudioFile('text.wav') as source:
        audio = r.record(source)

    text = r.recognize_sphinx(audio)
    file_object = open('transcript.txt', 'w')
    file_object.write(text)

def remove_existing_transcript_files():
    array_files = ['transcript.mp3', 'text.wav']
    for f in array_files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    remove_existing_transcript_files()
    download_as_mp3(str(sys.argv[1]))
    transcribe_to_text()
