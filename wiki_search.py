import json
import sys
import os
from difflib import get_close_matches

# --- 1. PATH FINDER FUNCTION ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WikiKnowledgeBase:
    def __init__(self, json_path):
        # 1. Initialize variables SAFELY at the very start
        # This prevents "AttributeError" if the file fails to load
        self.data = []
        self.index = {}
        self.titles = []
        
        # 2. Find the file
        real_path = resource_path(json_path) 
        print(f"--- DEBUG: Looking for JSON at: {real_path} ---") 

        # 3. Try to load it
        try:
            with open(real_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                
            # Create lookup index
            self.index = {entry['name'].lower(): entry['content'] for entry in self.data if 'name' in entry}
            self.titles = list(self.index.keys())
            print(f"✅ Loaded {len(self.titles)} wiki entries.")
            
        except Exception as e:
            # If loading fails, we print why, but self.titles is already [] so it won't crash
            print(f"❌ ERROR: Could not load JSON file.")
            print(f"❌ REASON: {e}")
            print("⚠️ App will run without Wiki knowledge.")

    def search(self, query, max_results=5):
        # Safety Check: If titles is empty (file failed), return nothing immediately
        if not self.titles:
            return "Wiki data unavailable (File load error)."

        if not query or len(query) < 3:
            return ""

        query_lower = query.lower()
        matches = get_close_matches(query_lower, self.titles, n=max_results, cutoff=0.4)
        
        context_text = ""
        for match in matches:
            # Grab the content, limit it to 800 chars
            content = self.index[match][:800] 
            context_text += f"\n--- WIKI ENTRY: {match.title()} ---\n{content}\n"
            
        if not context_text:
            return "No specific wiki data found for this topic."
            
        return context_text

# Initialize with the correct filename
wiki = WikiKnowledgeBase("terraria_master_knowledge.json")