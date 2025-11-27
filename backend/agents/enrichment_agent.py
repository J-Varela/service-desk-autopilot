from backend.agents.base_agent import BaseAgent
from backend.models.intent import IntentResult
from backend.services.directory_service import get_user_profile

class EnrichmentAgent(BaseAgent):
    name = "enrichment"

    def describe(self) -> str:
        return "Enriches intent with user profile and context."

    def enrich(self, user_id: str, intent: IntentResult) -> dict:
        profile = get_user_profile(user_id)
        return {
            "user": profile,
            "intent": intent.dict(),
        }
