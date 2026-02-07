# GamepAInion

**GamepAInion** is a hybrid edge-AI assistant that allows users to interact with multimodal AI (voice, text, and images) through an Android application, while leveraging a Snapdragon-powered laptop for heavier AI workloads such as speech-to-text (Whisper), vision processing, and large language model reasoning.

The system is designed to showcase **multi-device collaboration**, **edge AI**, and **low-latency human-computer interaction** using Snapdragon hardware.

---

## Application Description

The project consists of two main components:

### 1. Android Application (Client)
- Captures:
  - Voice input (push-to-talk)
  - Text prompts
  - Images (camera or gallery)
- Scans a QR code to connect to a local server
- Sends user input to the server over HTTP
- Displays the **final AI response only**

### 2. Laptop Server (Backend)
- Runs on a Snapdragon-powered Windows laptop
- Handles:
  - Whisper speech-to-text
  - Image processing
  - LLM reasoning
  - Game analysis pipelines
- Returns a clean, final response to the phone

---

## Team Members

- Melvin Estudillo – mestudillo01@manhattan.edu

- Matheo Villada - mvillada01@manhattan.edu

- Justin Balbuena – jbalbuena02@manhattan.edu 

---

## Repository Structure

```
.
├── android-app/
├── server/
│   ├── index.py
│   ├── ollama_image_test.py
│   └── requirements.txt
├── README.md
└── LICENSE
```

---

## Setup Instructions

### Prerequisites

- Android Studio
- Android phone (Android 10+)
- Python 3.10+
- Llama (gemma3:4b)
- Windows 11 Snapdragon laptop

---

### Server Setup

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python index.py
```

---

### Android App Setup

1. Open project in Android Studio
2. Sync Gradle
3. Run on device or install APK

---

## Running the Application

1. Start the server
2. Open the Android app
3. Scan the QR code
4. Send text, voice, or image input
5. View the final response on the phone

---

## License

MIT License
