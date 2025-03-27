from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Feedback(BaseModel):
    name: str
    message: str

app = FastAPI()

# Хранилище для отзывов
feedback_storage: List[Feedback] = []

# Маршрут для приема отзывов
@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    # Сохраняем отзыв в хранилище
    feedback_storage.append(feedback)
    # Формируем сообщение об успешном завершении
    response_message = {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }
    return response_message

@app.get("/read_feedback")
def read_root():
    return feedback_storage

# uvicorn main:app --reload