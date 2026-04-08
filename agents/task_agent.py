import re
from datetime import datetime, timedelta
from typing import Optional

class TaskExtractionAgent:
    def __init__(self):
        self.priority_keywords = {
            "high": ["urgent", "important", "critical", "asap", "immediately", "priority"],
            "low": ["whenever", "sometime", "optional", "low priority", "eventually"]
        }
        self.time_patterns = [
            r"(\d{1,2})\s*(am|pm)",
            r"(\d{1,2}):(\d{2})\s*(am|pm)?",
            r"at\s+(\d{1,2})\s*(am|pm)",
            r"at\s+(\d{1,2}):(\d{2})\s*(am|pm)?",
            r"(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",
        ]

    def extract(self, query: str) -> dict:
        tasks = []
        notes = []
        
        query_lower = query.lower()
        
        if "remember" in query_lower or "note" in query_lower or "note that" in query_lower:
            notes.append(query)
        
        sentences = re.split(r'[,\n]|\s+and\s+', query_lower)
        
        task_keywords = ["schedule", "remind", "task", "do", "finish", "complete", "start", "meeting", "appointment", "gym", "work"]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            is_task = any(kw in sentence for kw in task_keywords)
            is_note = not is_task and len(sentence.split()) > 2
            
            if is_task or ("remind" in sentence) or ("schedule" in sentence):
                title = self._extract_title(sentence)
                dt = self._extract_datetime(sentence)
                priority = self._extract_priority(sentence)
                
                if title:
                    tasks.append({
                        "title": title,
                        "datetime": dt.isoformat() if dt else None,
                        "priority": priority
                    })
            elif is_note or ("note" in sentence):
                note_text = self._extract_title(sentence)
                if note_text and len(note_text) > 2:
                    notes.append(note_text)
        
        return {"tasks": tasks, "notes": notes}

    def _extract_title(self, sentence: str) -> str:
        removals = ["remind me to", "remind me", "schedule", "at", "please", "can you", "i need to", "i want to", "to"]
        title = sentence.lower()
        for word in removals:
            title = title.replace(word, "")
        return title.strip().strip(".,!?").capitalize()

    def _extract_datetime(self, sentence: str) -> Optional[datetime]:
        now = datetime.now()
        
        for pattern in self.time_patterns:
            match = re.search(pattern, sentence)
            if match:
                groups = match.groups()
                try:
                    if "today" in sentence:
                        hour = int(groups[0]) if groups[0] else 12
                        minute = int(groups[1]) if groups[1] and groups[1].isdigit() else 0
                        ampm = groups[2] if len(groups) > 2 else None
                        if ampm == "pm" and hour != 12:
                            hour += 12
                        elif ampm == "am" and hour == 12:
                            hour = 0
                        return datetime(now.year, now.month, now.day, hour, minute)
                    elif "tomorrow" in sentence:
                        tomorrow = now + timedelta(days=1)
                        hour = int(groups[0]) if groups[0] else 12
                        minute = int(groups[1]) if groups[1] and groups[1].isdigit() else 0
                        return datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute)
                    else:
                        hour = int(groups[0])
                        minute = int(groups[1]) if len(groups) > 1 and groups[1] and groups[1].isdigit() else 0
                        ampm = groups[2] if len(groups) > 2 and groups[2] else None
                        if ampm == "pm" and hour != 12:
                            hour += 12
                        elif ampm == "am" and hour == 12:
                            hour = 0
                        return datetime(now.year, now.month, now.day, hour, minute)
                except:
                    pass
        return None

    def _extract_priority(self, sentence: str) -> str:
        for p, keywords in self.priority_keywords.items():
            if any(kw in sentence for kw in keywords):
                return p
        return "medium"