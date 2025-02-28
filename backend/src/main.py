import lmql
import datetime
import os.path
from typing import Optional, List
from uuid import UUID, uuid4

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Define Google Calendar API Scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# FastAPI setup
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task storage (for demo purposes)
todos = []


class TodoItem(BaseModel):
    id: Optional[UUID] = None
    todo: str
    tag: str
    start_date: datetime.datetime


def get_service():
    """Authenticate and return a Google Calendar service object."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "auth_cred_desktop.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("calendar", "v3", credentials=creds)


def add_event_to_calendar(event_data: TodoItem):
    """Add an event to Google Calendar."""
    try:
        service = get_service()
        event = {
            "summary": event_data.todo,
            "description": f"Tag: {event_data.tag}",
            "start": {
                "dateTime": event_data.start_date.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": (event_data.start_date + datetime.timedelta(hours=1)).isoformat(),
                "timeZone": "UTC",
            },
        }
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        return created_event
    except HttpError as error:
        return {"error": f"An error occurred: {error}"}


def get_all_calendar_entries():
    """Retrieve events from Google Calendar."""
    try:
        service = get_service()
        now = datetime.datetime.utcnow().isoformat() + "Z"

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return {"message": "No upcoming events found."}

        event_list = []
        for event in events:
            event_info = {
                "summary": event.get("summary", "No Title"),
                "start": event["start"].get("dateTime", event["start"].get("date")),
                "end": event["end"].get("dateTime", event["end"].get("date")),
                "description": event.get("description", ""),
            }
            event_list.append(event_info)
        return event_list
    except HttpError as error:
        return {"error": f"An error occurred: {error}"}


async def prioritize_tasks_with_lmql(tasks: List[str]):
    """Use LMQL to prioritize tasks using Ollama's LLM."""
    lmql.model("mistral", backend="ollama")
    @lmql.query
    async def task_prioritization():
        '''
        argmax "Reorder these tasks by priority: {tasks}\nPrioritized List: " 
        from "ollama/llama3.2"
        '''

    response = await task_prioritization(tasks=tasks)
    return response[0]  # Return the best-ranked response

@app.get("/")
async def test():
    return {"message": "Hello worlds"}

@app.get("/get_todos")
async def get_all_todos_1():
    return {"todos": todos}

@app.get("/todos")
async def get_all_todos():
    """Fetch Google Calendar events and use LMQL for AI prioritization."""
    calendar_entries = get_all_calendar_entries()

    if "message" in calendar_entries:  # No tasks found
        return calendar_entries

    task_list = [event["summary"] for event in calendar_entries]

    if not task_list:
        return {"message": "No tasks available"}

    prioritized_tasks = await prioritize_tasks_with_lmql(task_list)

    return {"todos": prioritized_tasks}


@app.post("/prioritize_tasks/")
async def prioritize_tasks(tasks: List[str]):
    """Expose LMQL prioritization as an API endpoint."""
    prioritized_tasks = await prioritize_tasks_with_lmql(tasks)
    return {"prioritized_tasks": prioritized_tasks}


@app.post("/todo/create")
async def insert_todo(task: TodoItem):
    """Create a new task and add it to Google Calendar."""
    if task.id is None:
        task.id = uuid4()
    
    todos.append(task)
    added_event = add_event_to_calendar(task)
    
    return {"message": "Todo created", "calendar_event": added_event}
