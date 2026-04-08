# Multi-Agent AI Productivity Assistant

## 🚀 Overview

This project is a **multi-agent AI system** designed to manage tasks, schedules, and notes from natural language input. It demonstrates coordination between multiple agents, tool integration, and structured data storage in a cloud-deployed API.

---

## 🎯 Features

* Multi-agent architecture (Primary + Sub-agents)
* Natural language input processing
* Task extraction and scheduling
* Notes detection and storage
* Tool-based modular design
* SQLite database persistence
* REST API with FastAPI
* Deployed on Google Cloud Run

---

## 🧠 System Architecture

User -> API -> Primary Agent -> Sub Agents -> Tools -> Database

### Agents:

* **Primary Agent**: Orchestrates workflow
* **Task Extraction Agent**: Parses tasks, events, notes
* **Scheduling Agent**: Assigns time slots
* **Notes Agent**: Handles note storage

### Tools:

* TaskTool
* CalendarTool
* NotesTool

---

## ⚙️ Tech Stack

* Backend: FastAPI (Python)
* Database: SQLite
* ORM: SQLAlchemy
* Deployment: Google Cloud Run
* API Docs: Swagger UI

---

## 🔌 API Endpoints

### POST `/process`

Processes natural language input

#### Example:

```json
{
  "query": "Schedule gym at 6am, note buy groceries, meeting at 10am"
}
```

---

### GET `/tasks`

Retrieve stored tasks

### GET `/events`

Retrieve scheduled events

### GET `/notes`

Retrieve saved notes

---

## 🔄 Workflow

1. User sends natural language query
2. Primary Agent interprets intent
3. Sub-agents extract structured data
4. Tools store data in database
5. API returns structured response

---

## ☁️ Deployment

The project is deployed on Google Cloud Run:

👉 https://ai-agent-76363387430.asia-south1.run.app/

API Documentation:
👉 https://ai-agent-76363387430.asia-south1.run.app/docs

---

## 🖥️ Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/SohamB-42/prod_app
cd prod_app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
uvicorn app.main:app --reload
```

---

## 📌 Example Use Case

Input:

```json
{
  "query": "Schedule gym at 6am, note buy groceries, meeting at 10am"
}
```

Output:

* Tasks created
* Events scheduled
* Notes stored

---

## 📈 Advantages

* Modular and scalable architecture
* Deterministic rule-based parsing
* Easy to extend with additional agents
* Fully API-driven design

---

## 🔮 Future Improvements

* LLM-based semantic parsing
* Frontend UI integration
* Advanced scheduling optimization
* Voice input support

---
