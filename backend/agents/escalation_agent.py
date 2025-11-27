from backend.agents.base_agent import BaseAgent 
from backend.services.ticketing_service import create_ticket 

class EscalationAgent(BaseAgent): 
    name = "escalation" 

    def describe(self) -> str: 
        return "Create tickets and hands off to human agents." 
    
    def create_ticket(self, user_id: str, message: str, context: dict, plan) -> dict: 
        summary = f"User {user_id} requested help: {message}"
        details = {
            "user": context.get("user"), 
            "intent": context.get("intent"),
            "plan": plan.dict() if hasattr(plan, "dict") else plan,
        }
        ticket_id = create_ticket(summary, details) 
        return {"ticket_id": ticket_id, "summary": summary}