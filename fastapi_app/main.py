from my_agent.agent import graph
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from my_agent.chat import chat


class Request(BaseModel):
    user_input: str
    thread: str


app = FastAPI()


@app.post("/agent")
async def query_agent(request: Request):
    try:
        response = chat(request.user_input, request.thread)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Agent API is running"}