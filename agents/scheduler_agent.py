from datetime import datetime, timedelta
from typing import Optional

class SchedulingAgent:
    def __init__(self):
        self.default_duration = timedelta(hours=1)

    def assign_time_slot(self, tasks: list, existing_events: list) -> list:
        for task in tasks:
            if not task.get("datetime"):
                start_time = self._find_next_available_slot(existing_events)
                task["datetime"] = start_time.isoformat()
                task["end_datetime"] = (start_time + self.default_duration).isoformat()
        return tasks

    def _find_next_available_slot(self, existing_events: list) -> datetime:
        now = datetime.now()
        slot = datetime(now.year, now.month, now.day, now.hour + 1, 0, 0)
        
        for event in existing_events:
            event_start = event.get("start_time")
            event_end = event.get("end_time")
            if event_start and event_end:
                if isinstance(event_start, str):
                    event_start = datetime.fromisoformat(event_start)
                if isinstance(event_end, str):
                    event_end = datetime.fromisoformat(event_end)
                    
                if event_start <= slot < event_end:
                    slot = event_end
        
        return slot

    def check_conflicts(self, start_time: datetime, end_time: datetime, existing_events: list) -> bool:
        for event in existing_events:
            event_start = event.get("start_time")
            event_end = event.get("end_time")
            if event_start and event_end:
                if isinstance(event_start, str):
                    event_start = datetime.fromisoformat(event_start)
                if isinstance(event_end, str):
                    event_end = datetime.fromisoformat(event_end)
                
                if not (end_time <= event_start or start_time >= event_end):
                    return True
        return False

    def resolve_conflict(self, start_time: datetime, end_time: datetime, existing_events: list) -> datetime:
        new_start = end_time
        new_end = new_start + self.default_duration
        
        while self.check_conflicts(new_start, new_end, existing_events):
            new_start = new_end
            new_end = new_start + self.default_duration
            
        return new_start