# from ollama import chat

# stream = chat(
#     model='llama3.2',
#     messages=[{'role': 'user', 'content': 'How to integrate OLLAMA to my calender app. I have the APIs and I am using google calender?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)

from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/prioritize_tasks/")
async def prioritize_tasks(tasks: list):
    prompt = f"Reorder these tasks by priority: {tasks}"
    
    response = requests.post(OLLAMA_URL, json={"model": "llama3.2", "prompt": prompt, "stream": False})
    
    if response.status_code == 200:
        return {"prioritized_tasks": response.json()["response"]}
    else:
        raise HTTPException(status_code=500, detail="Error processing request with Ollama")
