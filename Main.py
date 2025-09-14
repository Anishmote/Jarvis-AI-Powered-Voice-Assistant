import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
import pygame
import os
import time
from openai import OpenAI
from gtts import gTTS

recognition = sr.Recognizer()
engine = pyttsx3.init()
# newsapi = "7cbd4458bb19604add2e4d78bb71665f"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    # unique filename
    filename = f"temp_{int(time.time())}.mp3"

    # gTTS save karega
    tts = gTTS(text ,lang="en",tld="co.in")
    tts.save(filename)

    # mixer init
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # agar pehle se kuch play ho raha hai to stop karo
    pygame.mixer.music.stop()

    # load aur play
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # wait until finished
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # file unload aur delete karo
    pygame.mixer.music.unload()
    os.remove(filename) 

def aiprocess(command):

    client = OpenAI(api_key="<ENTER YOUR API KEY HERE>")

    response = client.responses.create(
    model="gpt-4o-mini",
    input=f"{command}. Give short responses.",
    store=True,
)

    return(response.output_text)


def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")

    elif c.lower().startswith("play"):
        songg = c.lower().replace("play ", "")
        try:
            link = MusicLibrary.music[songg]
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I don't know that song.")
    elif "news" in c.lower():
        r = requests.get(f"<ENTER YOUR API KEY HERE>")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
        else:
            speak("Faild To Fetch News")
    else:
        output = aiprocess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis....!")
    while True:

        r =sr.Recognizer()


        try:
            with sr.Microphone() as scorce:
                print("Listening..!")
                audio = r.listen(scorce,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if ("jarvis" in word.lower()):
                speak("Yaa")
                

                with sr.Microphone() as scorce:
                    print("Jarvis Active...")
                    audio = r.listen(scorce)
                    command = r.recognize_google(audio)

                processcommand(command)
        except Exception as e:
            print(f"Error; {e}")