from wiki_search import wiki
import asyncio
import socket
from flask import Flask, render_template, request, jsonify
from ollama_image_test import analyze_image # Import your new function
from get_terraria_window import capture_terraria_window
from flask import Flask, render_template, request
from flask_qrcode import QRcode
import os
from werkzeug.utils import secure_filename
from flask import request, jsonify 
import base64 
import tempfile
from faster_whisper import WhisperModel 
import webbrowser
from threading import Timer

# Load once at startup 
whisper_model = WhisperModel( 
    "base",            # or "small", "medium" 
    device="cpu",     # "cuda" if GPU, else "cpu" 
    compute_type="int8" 
) 



app = Flask(__name__)
QRcode(app)

def get_local_ip():
    """Auto-detects the laptop's local Wi-Fi IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect, just determines the route to the internet
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@app.route("/")
def index():
    # Dynamically generate the URL for the phone to connect to
    local_ip = get_local_ip()
    port = 5000
    # The phone will be directed to the /connected page
    connect_url = f"http://{local_ip}:{port}/connected"
    
    print(f"Server running at: {connect_url}") # Print to console for verification
    return render_template('index.html', qr_data=connect_url)

@app.route("/connected")
def connected():
    # Capture device info
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    # Format a readable device name
    device_type = "Android Device" if "Android" in user_agent else "iOS Device" if "iPhone" in user_agent else "PC/Unknown"
    
    print("\n" + "="*40)
    print(f"📱 NEW CONNECTION DETECTED")
    print(f"IP Address: {user_ip}")
    print(f"Device:     {device_type}")
    print(f"Details:    {user_agent}")
    print("="*40 + "\n")
    
    return render_template('connected.html')

# Placeholder routes for your buttons (to prevent 404 errors during testing)
@app.route('/scan_screen', methods=['POST'])
async def scan_screen():
    # Extract question from JSON body
    data = request.get_json(silent=True) or {}
    user_question = data.get('prompt', "")

    wiki_context = wiki.search(user_question)
    
    test_image_path = "./background_capture.png"
    capture_success = await asyncio.to_thread(capture_terraria_window, test_image_path)

    if not capture_success:
        return jsonify({"status": "error", "message": "Terraria window not found"})

    # Pass question to analyze_image
    analysis_result = await asyncio.to_thread(analyze_image, test_image_path, user_question, wiki_context)
    return jsonify({"status": "success", "analysis": analysis_result})


# Ensure you have a folder to save phone uploads
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_phone', methods=['POST'])
async def upload_phone():
    # Extract question from FormData
    user_question = request.form.get('prompt', "")
    wiki_context = wiki.search(user_question)

    print(F"HEY LOOK AT ME IM THE PROMPT: {user_question}")

    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"})
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        analysis_result = await asyncio.to_thread(analyze_image, file_path, user_question, wiki_context)
        return jsonify({"status": "success", "analysis": analysis_result})
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route("/process_audio", methods=["POST"]) 
async def process_audio(): 
    data = request.get_json(force=True) 
    if "wav_base64" not in data: 
        return jsonify({"error": "No audio provided"}), 400 

    # Decode audio 
    wav_bytes = base64.b64decode(data["wav_base64"]) 

    # Save to temp WAV file 
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f: 
        f.write(wav_bytes) 
        wav_path = f.name 

    try: 
        # 🔊 Whisper transcription 
        segments, info = whisper_model.transcribe( 
            wav_path, 
            language="en" 
        ) 

        transcript = " ".join(segment.text for segment in segments).strip() 

        if not transcript: 
            return jsonify({"final_response": "I didn't hear anything."}) 

        print(F"HEY LOOK AT ME IM THE PROMPT: {transcript}")
        wiki_context = wiki.search(transcript)
    
        test_image_path = "./background_capture.png"
        capture_success = await asyncio.to_thread(capture_terraria_window, test_image_path)

        if not capture_success:
            return jsonify({"status": "error", "message": "Terraria window not found"})

        # Pass question to analyze_image
        analysis_result = await asyncio.to_thread(analyze_image, test_image_path, transcript, wiki_context)

        return jsonify({"status": "success", "analysis": analysis_result})

    finally:
        os.remove(wav_path) 


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000") # Or your 0.0.0.0 address

if __name__ == "__main__":
    # Wait 1 second for server to start, then open browser
    Timer(1, open_browser).start() 
    app.run(host='0.0.0.0', port=5000)