# ollama_image_test.py
import base64
import requests
import re
from pathlib import Path

MODEL = "gemma3:4b" # Or the model you have downloaded
OLLAMA_URL = "http://localhost:11434/api/chat"

def analyze_image(img_path_str, user_question, wiki_context=""):
    """Refactored core logic for use in other scripts."""
    img_path = Path(img_path_str)
    if not img_path.exists():
        return {"error": "File not found"}

    # Use your existing detailed prompt if none is provided
    img_path = Path(img_path_str)
    
    # This prompt tells the AI to use the image as support for the user's text
    prompt = (
        f"USER QUESTION: {user_question}\n\n"
        f"OFFICIAL WIKI DATA (Facts/Stats):\n"
        f"{wiki_context}\n\n"
        "You are a high-precision Terraria Expert System. Your goal is to provide a grounded, evidence-based answer.\n\n"
        "Follow this logical sequence in your internal analysis:\n"
        "1. OBSERVATION: Look at the blocks, background, and vegetation. Note the specific colors and shapes (e.g., Are the blocks mud or dirt? Is the grass bright neon or standard green?).\n"
        "2. DIFFERENTIATION: Use those observations to rule out similar biomes. (Example: Forest has brown bark and standard green leaves; Jungle has darker bark, vines, and brighter greens).\n"
        "3. DIRECT ANSWER: Answer the user's question based on your observation. **If the WIKI DATA above contains relevant stats, recipes, or drop rates, you MUST quote them in your answer.**\n"
        "4. VISUAL PROOF: Cite the specific pixels or background elements that confirmed your answer.\n"
        "5. STRATEGY: Give one piece of expert advice relevant to that specific area or item.\n\n"
        "IMPORTANT: If you are unsure, describe what you see literally (e.g., 'I see green blocks and brown trees') rather than guessing a biome name."
    )
    def b64_image(path):
        return base64.b64encode(path.read_bytes()).decode("utf-8")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [b64_image(img_path)],
            }
        ],
        "stream": False,
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        r.raise_for_status()
        full_text = r.json()["message"]["content"]

        # === NEW FILTERING LOGIC ===
        # Use Regex to capture text specifically between "DIRECT ANSWER:" and "VISUAL PROOF:"
        # This handles variations like "**DIRECT ANSWER:**" or "3. DIRECT ANSWER:"
        match = re.search(
            r"DIRECT ANSWER:[\s\*]*(.*?)(?=(?:4\.|VISUAL PROOF|5\.|STRATEGY|$))", 
            full_text, 
            re.DOTALL | re.IGNORECASE
        )

        if match:
            # Found the clean answer! Return just that part.
            return match.group(1).strip()
        else:
            # Fallback: If AI didn't follow format, return the whole thing so we don't return nothing.
            return full_text

    except Exception as e:
        return f"Error: {str(e)}"

# This keeps your original CLI functionality intact
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        print(analyze_image(sys.argv[1]))