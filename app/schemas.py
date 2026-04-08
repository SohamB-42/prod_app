from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"
    due_datetime: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_datetime: Optional[datetime] = None

class EventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime

class EventResponse(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime

class NoteCreate(BaseModel):
    content: str

class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

class ProcessRequest(BaseModel):
    query: str

class ProcessResponse(BaseModel):
    tasks_created: List[TaskResponse] = []
    events_scheduled: List[EventResponse] = []
    notes_saved: List[NoteResponse] = []