from pydantic import BaseModel 

class IntentResult(BaseModel): 
    user_id: str 
    raw_message: str 
    intent: str
    domain: str 
    confidence: float
    urgency: str 

    