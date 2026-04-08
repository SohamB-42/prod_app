class NotesAgent:
    def extract(self, query: str) -> list[str]:
        notes = []
        segments = query.split(",")
        
        for segment in segments:
            segment = segment.strip().lower()
            keywords = ["note", "remember", "don't forget", " remind", "idea", "thought"]
            
            if any(kw in segment for kw in keywords):
                text = segment
                for kw in keywords:
                    text = text.replace(kw, "")
                text = text.strip(".,!? ")
                if text and len(text) > 2:
                    notes.append(text)
        
        return notes