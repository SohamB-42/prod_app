from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Event
from tools.base_tool import BaseTool

class CalendarTool(BaseTool):
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, title: str, start_time: datetime, end_time: datetime) -> Event:
        event = Event(title=title, start_time=start_time, end_time=end_time)
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_events(self, date: datetime = None) -> list[Event]:
        query = self.db.query(Event)
        if date:
            query = query.filter(
                datetime.year == date.year,
                datetime.month == date.month,
                datetime.day == date.day
            )
        return query.all()

    def execute(self, input_data: dict) -> dict:
        action = input_data.get("action")
        if action == "create":
            event = self.create_event(
                title=input_data["title"],
                start_time=input_data["start_time"],
                end_time=input_data["end_time"]
            )
            return {"id": event.id, "title": event.title, "start_time": event.start_time, "end_time": event.end_time}
        elif action == "get_all":
            events = self.get_events()
            return [{"id": e.id, "title": e.title, "start_time": e.start_time, "end_time": e.end_time} for e in events]
        return {"error": "Unknown action"}