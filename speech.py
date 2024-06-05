import subprocess
import pyttsx3
import json
import random
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from urllib.request import urlopen
import sys
import multiprocessing

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def wikipedia_search(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("Conform Wikipedia")
        print(results + "\n")
        speak(results)
    except wikipedia.exceptions.PageError:
        speak("Scuze, nu am putut găsi niciun rezultat pentru întrebarea ta pe Wikipedia.")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Există mai multe rezultate pentru întrebarea ta. Te rog să fii mai specific.")
        print(f"Opțiuni: {e.options}\n")
def typingPrint(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir !")
    else:
        speak("Good Evening Sir !")
    assname = "Jarvis 1 point o"
    speak("I am your Assistant")
    speak(assname)

def username():
    time.sleep(5)
    speak("What should I call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns
    typingPrint("Welcome Mr. ")
    typingPrint(uname + "\n")
    speak("How can I help you, Sir")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        typingPrint("Listening...\n")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        typingPrint("Recognizing...\n")
        query = r.recognize_google(audio, language='en-in')
        typingPrint(f"User said: {query}\n")
    except Exception as e:
        typingPrint("Unable to Recognize your voice.\n")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()
def background_process():
    os.system("python sound_viewer.py")
if __name__ == '__main__':
    clear = lambda: os.system('cls')
    background = multiprocessing.Process(target=background_process)
    background.start()
    clear()
    wishMe()
    username()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                typingPrint(results + "\n")
                speak(results)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find any results for your query on Wikipedia.")
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results for your query. Please be more specific.")
                typingPrint(f"Options: {e.options}\n")

        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Here you go to Stack Overflow. Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query or "play song" in query:
            speak("Here you go with music")
            music_dir = "C:\\Users\\GAURAV\\Music"
            songs = os.listdir(music_dir)
            typingPrint(str(songs) + "\n")
            random_song = random.choice(songs)
            os.startfile(os.path.join(music_dir, random_song))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("% H:% M:% S")
            speak(f"Sir, the time is {strTime}")

        elif 'open opera' in query:
            codePath = r"C:\\Users\\GAURAV\\AppData\\Local\\Programs\\Opera\\launcher.exe"
            os.startfile(codePath)

        elif 'email to gaurav' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Receiver email address"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                typingPrint(str(e) + "\n")
                speak("I am not able to send this email")

        elif 'send a mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Whom should I send it to?")
                to = input("Enter the recipient's email: ")
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                typingPrint(str(e) + "\n")
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that you're fine")

        elif "change my name to" in query:
            query = query.replace("change my name to", "").strip()
            assname = query

        elif "change name" in query:
            speak("What would you like to call me, Sir?")
            assname = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in query or "what is your name" in query:
            speak("My friends call me")
            speak(assname)
            typingPrint(f"My friends call me {assname}\n")

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Robert.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())
        elif 'search' in query or 'play' in query:
            query = query.replace("search", "").replace("play", "").strip()
            webbrowser.open(query)

        elif "who am i" in query:
            speak("If you talk, then definitely you're human.")

        elif "why you came to world" in query:
            speak("Thanks to Robert. It's a secret though.")

        elif 'power point presentation' in query:
            speak("Opening Power Point presentation")
            power = r"C:\\Users\\GAURAV\\Desktop\\Minor Project\\Presentation\\Voice Assistant.pptx"
            os.startfile(power)

        elif "who are you" in query:
            speak("I am your virtual assistant created by Robert")

        elif 'reason for you' in query:
            speak("I was created as a minor project by Robert")

        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, "Location of wallpaper", 0)
            speak("Background changed successfully")

        elif 'news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=YOUR_API_KEY''')
                data = json.load(jsonObj)
                i = 1
                speak('Here are some top news from the Times of India')
                typingPrint('=============== TIMES OF INDIA ============' + '\n')
                for item in data['articles']:
                    typingPrint(str(i) + '. ' + item['title'] + '\n')
                    typingPrint(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                typingPrint(str(e) + "\n")

        elif 'lock window' in query:
            speak("Locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Hold On a Sec! Your system is on its way to shut down")
            subprocess.call('shutdown /p /f')

        elif "don't listen" in query or "stop listening" in query:
            speak("For how much time do you want to stop Jarvis from listening commands?")
            a = int(takeCommand())
            time.sleep(a)
            typingPrint(f"Stopped listening for {a} seconds\n")

        elif "where is" in query:
            query = query.replace("where is", "").strip()
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera", "img.jpg")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown /h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all applications are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in query:
            speak("What should I write, sir?")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, should I include date and time?")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
            file.close()
        elif "update assistant" in query:
            speak("After downloading the file, please replace this file with the downloaded one")
            url = '# url after uploading file'
            r = requests.get(url, stream=True)
            with open("Voice.py", "wb") as Pypdf:
                total_length = int(r.headers.get('content-length'))
                for ch in progress.bar(r.iter_content(chunk_size=2391975), expected_size=(total_length / 1024) + 1):
                    if ch:
                        Pypdf.write(ch)

        elif "jarvis" in query:
            wishMe()
            speak("Jarvis 1 point o in your service, Mister")
            speak(assname)

        elif "weather" in query:
            api_key = "Your OpenWeatherMap API Key"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak("City name")
            typingPrint("City name: ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                typingPrint(f"Temperature (in kelvin unit) = {current_temperature}\n"
                            f"Atmospheric pressure (in hPa unit) = {current_pressure}\n"
                            f"Humidity (in percentage) = {current_humidity}\n"
                            f"Description = {weather_description}\n")
                speak(f"Temperature is {current_temperature} kelvin. "
                      f"Atmospheric pressure is {current_pressure} hPa. "
                      f"Humidity is {current_humidity} percent. "
                      f"Weather description: {weather_description}.")
            else:
                speak("City Not Found")

        elif "Good Morning" in query:
            speak("A warm" + query)
            speak("How are you, Mister")
            speak(assname)

        elif "how are you" in query:
            speak("I'm fine, glad you asked")

        elif "what is" in query or "who is" in query or "who was" in query:
            query = query.replace("what is", "").replace("who is", "").replace("who was", "").strip()
            wikipedia_search(query)
        elif "thank you" in query or 'thanks' in query:
            speak("You're welcome!")
            typingPrint("You're welcome!")
