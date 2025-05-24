import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import pyjokes
import random 
import datetime

# Motivational quotes list
motivational_quotes = [
    "You are stronger than you think.",
    "Believe in yourself, and you will be unstoppable.",
    "Every great journey begins with a single step.",
    "The harder you work, the luckier you get.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "Push yourself, because no one else is going to do it for you.",
    "Dream big, work hard, stay focused.",
    "Your only limit is your mind.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Stay positive, work hard, make it happen."
]

# pip install pocketsphinx

# Weather function
weather_api_key = "d0bebc59ce406c638d2aeb77b036ff4f"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            return f"Sorry, I couldn’t find weather info for {city}."
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        city_name = data["name"]
        
        weather_report = f"It’s {temp}°C with {description} in {city_name}."
        return weather_report
    except Exception as e:
        return "Sorry, I couldn’t fetch the weather right now."

# ---------------- To-Do List Functions ----------------

def add_reminder(task):
    with open("todo_list.txt", "a") as file:
        file.write(task + "\n")
    return f"Okay, I’ve added: {task}"

def get_reminders():
    try:
        with open("todo_list.txt", "r") as file:
            tasks = [line.strip() for line in file.readlines()]
        if not tasks:
            return "Your to-do list is empty."
        task_list = "\n".join(f"- {task}" for task in tasks)
        return f"Here’s your to-do list:\n{task_list}"
    except FileNotFoundError:
        return "You don’t have a to-do list yet."

def clear_reminders():
    open("todo_list.txt", "w").close()
    return "All reminders have been cleared."



recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "ca5018b114484bac81d0c3a009b6e4d6"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "joke" in c.lower():  # ← NEW JOKE FEATURE
        joke = pyjokes.get_joke()
        print(f"Joke: {joke}")
        speak(joke)
    elif "motivate" in c.lower():  # ← NEW MOTIVATIONAL FEATURE
        quote = random.choice(motivational_quotes)
        print(f"Motivation: {quote}")
        speak(quote)
    elif "what time is it" in c.lower() or "tell me the time" in c.lower():
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        response = f"The time is {current_time}."
        print(response)
        speak(response)

    elif "weather" in c.lower():  # ← NEW WEATHER FEATURE
        words = c.lower().split()
        if "in" in words:
            city_index = words.index("in") + 1
            if city_index < len(words):
                city = words[city_index]
                report = get_weather(city)
                print(f"Weather: {report}")
                speak(report)
            else:
                speak("Please tell me the city name.")
        else:
            speak("Please tell me which city you want the weather for.")

    elif "remind me to" in c.lower():
        task = c.lower().split("remind me to")[1].strip()
        response = add_reminder(task)
        print(f"Reminder Added: {response}")
        speak(response)

    elif "what's on my to-do list" in c.lower() or "what is on my to-do list" in c.lower():
        response = get_reminders()
        print(f"To-Do List: {response}")
        speak(response)

    elif "clear my to-do list" in c.lower():
        response = clear_reminders()
        print(response)
        speak(response)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=6)
            word = r.recognize_google(audio)
            if "hello" in word.lower():
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))



