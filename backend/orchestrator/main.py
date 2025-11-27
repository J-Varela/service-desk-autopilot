from fastapi import FastAPI 
from pydantic import BaseModel 
from backend.orchestrator.agent_router import handle_chat 
from backend.config import settings

app = FastAPI(title="SmartDesk")

class ChatRequest(BaseModel): 
    user_id: str
    message: str

class ChatResponse(BaseModel): 
    reply: str 
    activity_log: list

@app.get("/health")
def health_check(): 
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "azure_configured": bool(settings.AZURE_OPENAI_ENDPOINT)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest): 
    reply, activity_log = handle_chat(req.user_id, req.message) 
    return ChatResponse(reply=reply, activity_log=activity_log)