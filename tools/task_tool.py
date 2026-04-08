from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Task
from tools.base_tool import BaseTool

class TaskTool(BaseTool):
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, title: str, priority: str = "medium", due_datetime: Optional[datetime] = None) -> Task:
        task = Task(title=title, priority=priority, due_datetime=due_datetime)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_tasks(self) -> list[Task]:
        return self.db.query(Task).all()

    def delete_task(self, task_id: int) -> bool:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def execute(self, input_data: dict) -> dict:
        action = input_data.get("action")
        if action == "create":
            task = self.create_task(
                title=input_data["title"],
                priority=input_data.get("priority", "medium"),
                due_datetime=input_data.get("due_datetime")
            )
            return {"id": task.id, "title": task.title, "priority": task.priority, "due_datetime": task.due_datetime}
        elif action == "get_all":
            tasks = self.get_tasks()
            return [{"id": t.id, "title": t.title, "priority": t.priority, "due_datetime": t.due_datetime} for t in tasks]
        elif action == "delete":
            return {"success": self.delete_task(input_data["task_id"])}
        return {"error": "Unknown action"}