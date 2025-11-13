import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import json
from groq import Groq
from dotenv import load_dotenv
import os
import time
from scene_description import describe_scene
from navigation_assisstant import continuous_navigation
from text_reader import read_text_from_camera






# ───────────────────────────────
# CONTACTS LOADER
# ───────────────────────────────
def load_contacts():
    """Load WhatsApp contacts from contacts.json"""
    try:
        with open("contacts.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ contacts.json not found. Creating an empty one...")
        with open("contacts.json", "w") as f:
            json.dump({}, f)
        return {}
    except json.JSONDecodeError:
        print("⚠️ contacts.json is invalid. Please check its format.")
        return {}

def save_contact(name, number):
    """Save a new contact to contacts.json"""
    try:
        # Load existing contacts
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        contacts = {}

    # Add or update contact
    contacts[name.lower()] = number

    # Write updated contacts back to file
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)

    talk(f"Saved contact {name} with number {number}.")
    print(f"✅ Contact saved: {name} → {number}")

    # Refresh global CONTACTS so changes apply instantly
    global CONTACTS
    CONTACTS = contacts


CONTACTS = load_contacts()


# ───────────────────────────────
# LOAD CONFIG
# ───────────────────────────────
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY missing in .env file!")

client = Groq(api_key=GROQ_KEY)

# ───────────────────────────────
# VOICE SYSTEM
# ───────────────────────────────
listener = sr.Recognizer()
engine = pyttsx3.init(driverName='nsss')
engine.setProperty('rate', 170)
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')



import os

def talk(text):
    """Use macOS built-in voice for rock-solid output."""
    print("🗣️", text)
    os.system(f"say -v Alex '{text}'")


def greeting_message():
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good Morning!")
    elif hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")
    talk("I am your voice assistant powered by Groq. How can I assist you?")

def accept_command():
    try:
        with sr.Microphone() as source:
            print("🎙️ Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if command:
                command = command.lower()
                print(f"🧏 You said: {command}")
                return command
    except sr.UnknownValueError:
        talk("Sorry, I could not understand what you said.")
    except sr.RequestError:
        talk("Speech service error.")
    return None

# ───────────────────────────────
# GROQ CHAT FUNCTION
# ───────────────────────────────
def chat_with_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting Groq: {e}"

# ───────────────────────────────
# COMMAND FUNCTIONS
# ───────────────────────────────
def command_play_music(command):
    song = command.replace("play", "")
    talk("Playing " + song)
    pywhatkit.playonyt(song)

def command_get_current_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    talk("The time is " + time_now)

def command_search_wikipedia(command):
    person = command.replace("who is", "")
    info = wikipedia.summary(person, 2)
    talk(info)

def command_tell_joke():
    res = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
    joke = res.json()["joke"]
    talk(joke)

def command_tell_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": "us", "apiKey": "YOUR_NEWS_API_KEY"}
    res = requests.get(url, params=params)
    data = res.json()
    for article in data["articles"][:5]:
        title = article["title"]
        talk(title)
import pywhatkit as kit

import webbrowser
import urllib.parse

import webbrowser
import urllib.parse

import webbrowser
import urllib.parse

import webbrowser
import urllib.parse
import re

def command_send_whatsapp_message(command=None):
    try:
        if not command:
            talk("What should I send and to whom?")
            command = accept_command()
            if not command:
                talk("Sorry, I could not understand.")
                return

        # Normalize and clean up
        cmd = command.lower()

        # Remove filler words
        fillers = ["send", "message", "to", "on", "whatsapp", "saying", "through", "using"]
        for word in fillers:
            cmd = cmd.replace(word, "")
        cmd = cmd.strip()

        # Detect contact name
        contact_name = None
        for name in CONTACTS.keys():
            if name in cmd:
                contact_name = name
                break

        if not contact_name:
            talk("Who should I send the message to?")
            contact_name = accept_command()
            if not contact_name or contact_name not in CONTACTS:
                talk("Sorry, I don't have that contact saved.")
                return

        # Extract message text (everything except the name)
        message = cmd.replace(contact_name, "").strip()

        # Ask if message part is empty
        if not message:
            talk("What message should I send?")
            message = accept_command()
            if not message:
                talk("Sorry, I could not understand the message.")
                return

        number = CONTACTS[contact_name]
        encoded_message = urllib.parse.quote(message)

        url = f"https://wa.me/{number.replace('+', '')}?text={encoded_message}"

        talk(f"Opening WhatsApp Web to send '{message}' to {contact_name}.")
        webbrowser.open(url)
        talk("Your message is ready. Press Enter or Send on WhatsApp Web to confirm.")

    except Exception as e:
        talk(f"Sorry, I could not send the message. Error: {e}")




# ───────────────────────────────
# MAIN LOGIC
# ───────────────────────────────
def process_command(command):
    if "play" in command:
        command_play_music(command)
    elif "time" in command:
        command_get_current_time()
    elif "who is" in command:
        command_search_wikipedia(command)
    elif "joke" in command:
        command_tell_joke()
    elif "news" in command:
        command_tell_news()
    elif "send message" in command or "whatsapp" in command:
        command_send_whatsapp_message(command)
    elif "how are you" in command:
        talk("I am doing great, thank you for asking!")
    elif "describe" in command or "what do you see" in command or "surroundings" in command or "around" in command:
     describe_scene(talk)
    elif "read" in command or "text" in command or "document" in command or "what is written" in command:
     read_text_from_camera(talk)

    elif "navigate" in command or "guide" in command or "path" in command:
     def listen_for_stop():
        try:
            with sr.Microphone() as source:
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source, timeout=0.5, phrase_time_limit=2)
                cmd = listener.recognize_google(voice).lower()
                return "stop" in cmd or "exit" in cmd
        except:
            return False

     continuous_navigation(talk, listen_for_stop)


    elif "add contact" in command or "save contact" in command:
     talk("Please say the name of the contact.")
     name = accept_command()
     if not name:
        talk("Sorry, I didn't catch the name.")
        return

     talk("Now please say the phone number, including country code.")
     number = accept_command()
     if not number:
        talk("Sorry, I didn't catch the number.")
        return

     # Clean and normalize number
     number = number.lower().replace("plus", "+").replace(" ", "").replace("-", "")
     if not number.startswith("+"):
        talk("Please include the country code, like plus nine one.")
        return

     save_contact(name, number)

     # Object detection integration
    elif "detect" in command or "what is in front" in command:
        from object_detection import detect_objects_from_camera
        detect_objects_from_camera(talk)

    elif "where is my" in command:
        from object_detection import detect_objects_from_camera
        target = command.replace("where is my", "").strip()
        detect_objects_from_camera(talk, target)


    else:
        reply = chat_with_groq(command)
        talk(reply)


def run_voice_assistant():
    greeting_message()
    while True:
        cmd = accept_command()
        if not cmd:
            continue
        if any(word in cmd for word in ["exit", "quit", "stop"]):
            talk("Goodbye! Have a nice day.")
            break
        process_command(cmd)

if __name__ == "__main__":
    run_voice_assistant()
