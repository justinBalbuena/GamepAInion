import json
from difflib import get_close_matches

class WikiKnowledgeBase:
    def __init__(self, json_path):
        print("📚 Loading Terraria Wiki Data... (this may take a second)")
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Create a quick lookup index
        self.index = {entry['name'].lower(): entry['content'] for entry in self.data if 'name' in entry}
        self.titles = list(self.index.keys())
        print(f"✅ Loaded {len(self.titles)} wiki entries.")

    def search(self, query, max_results=5):
        """
        Finds relevant wiki entries based on the user's search query.
        """
        if not query or len(query) < 3:
            return ""

        # 1. Try exact match (e.g. "Night's Edge")
        query_lower = query.lower()
        results = []

        # 2. Fuzzy match keywords (finds "Blade of Grass" if user types "grass blade")
        matches = get_close_matches(query_lower, self.titles, n=max_results, cutoff=0.4)
        
        context_text = ""
        for match in matches:
            # Grab the content, truncate it if it's massive (limit to 500 chars per entry)
            content = self.index[match][:800] 
            context_text += f"\n--- WIKI ENTRY: {match.title()} ---\n{content}\n"
            
        if not context_text:
            return "No specific wiki data found for this topic."
            
        return context_text

# Singleton instance to be used by other files
# (Make sure the filename matches your uploaded file exactly)
wiki = WikiKnowledgeBase("terraria_master_knowledge.json")