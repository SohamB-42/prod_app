from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.schemas import ProcessRequest, ProcessResponse, TaskResponse, EventResponse, NoteResponse
from agents.primary_agent import PrimaryAgent
from tools.task_tool import TaskTool
from tools.calendar_tool import CalendarTool
from tools.notes_tool import NotesTool

app = FastAPI(title="Multi-Agent Productivity Assistant")

@app.get("/")
def root():
    return {"message": "AI Agent is running 🚀"}

@app.on_event("startup")
def startup():
    init_db()

@app.post("/process", response_model=ProcessResponse)
def process_query(request: ProcessRequest, db: Session = Depends(get_db)):
    agent = PrimaryAgent(db)
    result = agent.process(request.query)
    return result

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tool = TaskTool(db)
    tasks = tool.get_tasks()
    return [TaskResponse(id=t.id, title=t.title, priority=t.priority, due_datetime=t.due_datetime) for t in tasks]

@app.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    tool = CalendarTool(db)
    events = tool.get_events()
    return [EventResponse(id=e.id, title=e.title, start_time=e.start_time, end_time=e.end_time) for e in events]

@app.get("/notes", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    tool = NotesTool(db)
    notes = tool.get_notes()
    return [NoteResponse(id=n.id, content=n.content, created_at=n.created_at) for n in notes]