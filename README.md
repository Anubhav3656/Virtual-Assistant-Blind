# Virtual Assistant for the Visually Impaired

An advanced AI-powered assistant designed to support visually impaired users through real-time **object detection**, **scene description**, **navigation assistance**, **text reading**, and **voice interaction**. Powered by modern computer vision and speech technologies, the assistant runs on a laptop and provides instant spoken feedback.

---

## 🚀 Features

### 🔊 Voice Interaction

* Fully voice-controlled
* Offline speech recognition using **Vosk**
* Natural speech output using **pyttsx3**

### 👁️ Object Detection

* YOLOv8-n and YOLOv8-s integrated
* Detects objects in real time
* Announces detected objects via speech

### 🧭 Navigation Assistance

* Detects obstacles
* Estimates distance and direction
* Gives real-time navigation warnings

### 🖼️ Scene Description

* Uses AI to describe surroundings
* Helps users understand environments instantly

### 📖 Text Reader

* Reads documents, signs, boards, and screens
* Uses OCR + TTS for reading aloud

### 📏 Depth Estimation

* Measures object distance
* Alerts user about nearby hazards

---

## 🛠️ Tech Stack

* **Python**
* **OpenCV**
* **YOLOv8**
* **Vosk ASR** (offline speech recognition)
* **pyttsx3** (text-to-speech)
* **Flask** (for simple frontend)
* Optional AI API for scene understanding

---

## 📦 Project Structure

```
Chat-bot-for-the-Blind/
│── app.py
│── main.py
│── object_detection.py
│── navigation_assistant.py
│── scene_description.py
│── text_reader.py
│── depth_estimation.py
│── templates/
│   └── index.html
│── vosk-model-small/
│── yolov8n.pt
│── yolov8s.pt
│── requirements.txt
```

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the assistant

```bash
python3 main.py
```

---

## 👨‍💻 Author

**Anubhav Chaudhary**

