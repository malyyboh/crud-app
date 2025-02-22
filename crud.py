from typing import List

from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()


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
async def get_all_messages() -> List[Message]:
    return messages_db


@app.get("/messages/{message_id}")
async def get_message(message_id: int) -> Message:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/messages", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if messages_db:
        message.id = max(messages_db, key=lambda m: m.id).id + 1
    else:
        message.id = 0
    messages_db.append(message)
    return "Message created!"


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
