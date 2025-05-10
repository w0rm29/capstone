# Import standard libraries
import datetime
import os.path
from typing import Optional, List
from uuid import UUID, uuid4

# Google API libraries for OAuth and Calendar access
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# FastAPI for API development
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# LMQL and HTTPX for async communication with AI model
import lmql
import httpx

# Define Google Calendar access scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for a todo item
class TodoItem(BaseModel):
    id: Optional[UUID] = None
    todo: str
    tag: str
    start_date: datetime.datetime

# Authenticate and create Google Calendar API service
def get_service():
    """Authenticate and return a Google Calendar service object."""
    creds = None

    # Check if token already exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "auth_cred_desktop.json", SCOPES
            )
            creds = flow.run_local_server(port=0)  # Launch local server for auth
        # Save credentials to file
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# Retrieve all events from Google Calendar for the current day
def get_all_calendar_entries():
    """Retrieve all Google Calendar events for today."""
    try:
        service = get_service()

        # Define time range for today
        now = datetime.datetime.utcnow()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + "Z"

        # Request calendar events
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_today,
            timeMax=end_of_today,
            maxResults=20,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_result.get("items", [])
        if not events:
            return {"message": "No events found for today."}

        # Format event data
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

# Call AI model to prioritize tasks
async def task_prioritization(task_list: list[dict]):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:  # Set timeout here explicitly
            response = await client.post(
                "http://localhost:8001/prioritize",  # Replace with actual endpoint
                json={"tasks": task_list}
            )
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx

        data = response.json()
        return data.get("prioritized_tasks", [])  # Safely extract

    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Task prioritization service timed out.")
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error from task prioritization service: {exc.response.text}"
        )
    
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to task prioritization service: {str(exc)}"
        )

    # Parse response
    prioritized_tasks = []
    for task, priority in zip(tasks, priorities):
        # Example: "- Task: High"
        task_name, task_priority = priority.split(":")
        prioritized_tasks.append((task_name.strip(), task_priority.strip()))

    return prioritized_tasks

# Test route
@app.get("/")
async def test():
    return {"message": "Hello world"}

# API to fetch all calendar entries and prioritize them
@app.get("/get_todos")
async def get_all_todos():
    """Fetch Google Calendar events and use AI for prioritization."""
    calendar_entries = get_all_calendar_entries()

    if "message" in calendar_entries:
        return calendar_entries

    task_list = [event["summary"] for event in calendar_entries]

    if not task_list:
        return {"message": "No tasks available"}

    prioritized_tasks = await task_prioritization(task_list)

    return {"todos": prioritized_tasks}

# Expose prioritization as a POST endpoint for custom tasks
@app.post("/prioritize_tasks/")
async def prioritize_tasks(tasks: List[str]):
    """Accept list of tasks and return prioritized results."""
    prioritized_tasks = await task_prioritization(tasks)
    return {"prioritized_tasks": prioritized_tasks}

# Add a new todo to Google Calendar
@app.post("/todo/create")
async def insert_todo(task: TodoItem):
    """Create a new task and add it to Google Calendar."""
    if task.id is None:
        task.id = uuid4()

    # Define calendar event format
    event_data = {
        "summary": task.todo,
        "description": f"Tag: {task.tag}",
        "start": {
            "dateTime": task.start_date.isoformat(),
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": (task.start_date + datetime.timedelta(hours=1)).isoformat(),
            "timeZone": "UTC",
        },
    }

    try:
        service = get_service()
        created_event = service.events().insert(calendarId="primary", body=event_data).execute()
        return {"message": "Todo created", "calendar_event": created_event}
    except HttpError as error:
        return {"error": f"An error occurred: {error}"}
