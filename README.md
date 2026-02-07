# GamepAInion
gamepAInion is a hybrid edge-AI assistant that allows users to interact with multimodal AI (voice, text, and images) through an Android application, while leveraging a Snapdragon-powered laptop for heavier AI workloads such as speech-to-text (Whisper), vision processing, and large language model reasoning.

The system is designed to showcase multi-device collaboration, edge AI, and low-latency human-computer interaction using Snapdragon hardware.

Application Description

The project consists of two main components:

1. Android Application (Client)

Captures:

Voice input (push-to-talk)

Text prompts

Images (camera or gallery)

Scans a QR code to connect to a local server

Sends user input to the server over HTTP

Displays the final AI response only, keeping the phone lightweight and responsive

2. Laptop Server (Backend)

Runs on a Snapdragon-powered Windows laptop

Handles:

Whisper speech-to-text

Image processing

LLM reasoning

Game analysis and decision pipelines

Returns a clean, final response to the phone

This architecture allows:

Minimal compute load on the phone

Heavy AI workloads on an edge device

Fast iteration and modular expansion

Team Members

Melvin Estudillo – mestudillo01@manhattan.edu

Matheo Villada - mvillada01@manhattan.edu

Justin Balbuena – jbalbuena02@manhattan.edu
