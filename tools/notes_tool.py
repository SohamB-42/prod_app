from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Note
from tools.base_tool import BaseTool

class NotesTool(BaseTool):
    def __init__(self, db: Session):
        self.db = db

    def create_note(self, content: str) -> Note:
        note = Note(content=content, created_at=datetime.now())
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_notes(self) -> list[Note]:
        return self.db.query(Note).order_by(Note.created_at.desc()).all()

    def execute(self, input_data: dict) -> dict:
        action = input_data.get("action")
        if action == "create":
            note = self.create_note(content=input_data["content"])
            return {"id": note.id, "content": note.content, "created_at": note.created_at}
        elif action == "get_all":
            notes = self.get_notes()
            return [{"id": n.id, "content": n.content, "created_at": n.created_at} for n in notes]
        return {"error": "Unknown action"}