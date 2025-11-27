from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.orchestrator.agent_router import handle_chat
from backend.config import settings

app = FastAPI(title="SmartDesk")

# Allow local frontend (file:// or localhost) to call the API during demos
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",  # common live-server port
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "*"  # broaden for hackathon demo; tighten for production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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