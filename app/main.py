from fastapi import FastAPI, BackgroundTasks, Request
from logging import getLogger

from app.train import voice_train_process

logging = getLogger(__name__)
app = FastAPI()


# uvicorn app.main:app --reload --host=0.0.0.0 --port=8004
# 문자 챗봇
@app.post("/voice_train")
async def voice_train(background_tasks: BackgroundTasks, request: Request):
    request_json = await request.json()
    background_tasks.add_task(voice_train_process, request_json)
    return {"message":"success"}

