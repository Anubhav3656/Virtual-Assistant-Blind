"""
Chat-Bot-for-the-Blind  (Groq Edition)
Offline voice I/O + Groq AI backend (LLaMA-3)
"""

import os
import json
import queue
import sounddevice as sd
import vosk
import pyttsx3
from dotenv import load_dotenv
from groq import Groq

# ───────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────
load_dotenv()  # load .env file automatically

MODEL_PATH = "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
GROQ_KEY = os.getenv("GROQ_API_KEY")  # key from Groq Console

if not GROQ_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY missing in .env file!")

# Initialize Groq client
client = Groq(api_key=GROQ_KEY)

# ───────────────────────────────────────────────
# VOICE SYSTEM INIT
# ───────────────────────────────────────────────
print("Loading Vosk model...")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"❌ Model folder '{MODEL_PATH}' not found. Download it from alphacephei.com/vosk/models"
    )

model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

engine = pyttsx3.init()
engine.setProperty("rate", 170)

audio_q = queue.Queue()

# ───────────────────────────────────────────────
# AUDIO I/O
# ───────────────────────────────────────────────
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_q.put(bytes(indata))


def listen():
    """Listen to microphone and return recognized text"""
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ):
        print("🎙️ Speak now...")
        while True:
            data = audio_q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    return text.lower()


def speak(text):
    """Speak text aloud"""
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()


# ───────────────────────────────────────────────
# GROQ CHAT FUNCTION
# ───────────────────────────────────────────────
def chat_with_groq(prompt):
    """Send user prompt to Groq API and return reply"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Groq’s current small fast model
# other: "mixtral-8x7b", "gemma-7b-it"
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant for the visually impaired."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting Groq: {e}"


# ───────────────────────────────────────────────
# MAIN LOOP
# ───────────────────────────────────────────────
def main():
    speak("Hello! I am your voice assistant powered by Groq. Say something.")
    while True:
        user_input = listen()
        print(f"You said: {user_input}")

        if any(word in user_input for word in ["exit", "quit", "stop"]):
            speak("Goodbye! Have a nice day.")
            break

        reply = chat_with_groq(user_input)
        speak(reply)


if __name__ == "__main__":
    main()
