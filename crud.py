from typing import List

from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Message(BaseModel):
    id: int | None = None
    text: str
    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "text": "Simple message",
                    }
                ]
        }
    }


messages_db = []


@app.get("/messages")
async def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "message.html", {"messages": messages_db})


@app.get("/messages/{message_id}")
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse(request, "message.html", {"message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/messages", status_code=status.HTTP_201_CREATED)
async def create_message(request: Request, message: str = Form()) -> HTMLResponse:
    if messages_db:
        max_id_message = max(messages_db, key=lambda m: m.id).id + 1
    else:
        max_id_message = 0
    messages_db.append(Message(id=max_id_message, text=message))
    return templates.TemplateResponse(request, "message.html", {"messages": messages_db})


@app.put("/messages/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return "Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/messages/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/messages")
async def delete_all_message() -> str:
    messages_db.clear()
    return "All messages deleted"
