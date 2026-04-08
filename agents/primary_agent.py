from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from agents.task_agent import TaskExtractionAgent
from agents.scheduler_agent import SchedulingAgent
from agents.notes_agent import NotesAgent
from tools.task_tool import TaskTool
from tools.calendar_tool import CalendarTool
from tools.notes_tool import NotesTool
from app.schemas import TaskResponse, EventResponse, NoteResponse

class PrimaryAgent:
    def __init__(self, db: Session):
        self.db = db
        self.task_extractor = TaskExtractionAgent()
        self.scheduler = SchedulingAgent()
        self.notes_agent = NotesAgent()
        self.task_tool = TaskTool(db)
        self.calendar_tool = CalendarTool(db)
        self.notes_tool = NotesTool(db)

    def process(self, query: str) -> dict:
        extraction_result = self.task_extractor.extract(query)
        
        tasks = extraction_result.get("tasks", [])
        notes = extraction_result.get("notes", [])
        
        existing_events = self.calendar_tool.get_events()
        existing_events_data = [{"start_time": e.start_time, "end_time": e.end_time} for e in existing_events]
        
        if tasks:
            tasks = self.scheduler.assign_time_slot(tasks, existing_events_data)
        
        tasks_created = []
        events_scheduled = []
        
        for task in tasks:
            dt = task.get("datetime")
            due_dt = None
            if dt:
                try:
                    due_dt = datetime.fromisoformat(dt)
                    end_dt = due_dt + timedelta(hours=1)
                    event = self.calendar_tool.create_event(
                        title=task["title"],
                        start_time=due_dt,
                        end_time=end_dt
                    )
                    events_scheduled.append(event)
                except Exception as e:
                    pass
            
            created_task = self.task_tool.create_task(
                title=task["title"],
                priority=task.get("priority", "medium"),
                due_datetime=due_dt
            )
            tasks_created.append(created_task)
        
        notes_saved = []
        for note_text in notes:
            note = self.notes_tool.create_note(content=note_text)
            notes_saved.append(NoteResponse(id=note.id, content=note.content, created_at=note.created_at))
        
        response_tasks = [
            TaskResponse(id=t.id, title=t.title, priority=t.priority, due_datetime=t.due_datetime)
            for t in tasks_created
        ]
        response_events = [
            EventResponse(id=e.id, title=e.title, start_time=e.start_time, end_time=e.end_time)
            for e in events_scheduled
        ]
        
        return {
            "tasks_created": response_tasks,
            "events_scheduled": response_events,
            "notes_saved": notes_saved
        }