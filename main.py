import speech_recognition as sr
import os
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold= 1
        audio=r.listen(source)

while 1:
    print('Enter the word you want to speak by computer')
    s=input()
    speaker.Speak(s)