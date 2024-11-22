import datetime
import os.path
from typing import Optional, Union
from uuid import UUID, uuid4

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# FastAPI setup
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

todos = []


class TodoItem(BaseModel):
    id: Optional[UUID] = None
    todo: str
    tag: str
    start_date: datetime.datetime
    end_date: datetime.datetime


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


@app.get("/test")
async def test():
    return {"message": "Hello World"}


@app.get("/todos")
def get_all_todos():
    return {"todos": todos}


@app.post("/todo/create")
def insert_todo(task: TodoItem):
    if task.id is None:
        task.id = uuid4()
    todos.append(task)
    added_event = add_event_to_calendar(task)
    return {"message": "Todo created", "calendar_event": added_event}
