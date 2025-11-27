from backend.agents.base_agent import BaseAgent
from backend.models.intent import IntentResult
from backend.utils.llm_client import call_llm
import json

TRIAGE_SYSTEM_PROMPT = """
You are an intent classification assistant for an internal service desk.

Given a user's message, classify:

- intent: a short snake_case label like:
  - account_access_issue
  - pto_balance
  - hr_policy_question
  - device_issue
  - payroll_question
  - unknown

- domain: one of: "it", "hr", "finance", "facilities", "general"

- urgency: one of: "low", "normal", "high"

Respond ONLY with valid JSON in this format:
{
  "intent": "...",
  "domain": "...",
  "urgency": "...",
  "confidence": 0.0
}
"""
class TriageAgent(BaseAgent):
    name = "triage"

    def describe(self) -> str:
        return "Classifies user intent and domain using an LLM."

    def infer_intent(self, user_id: str, message: str) -> IntentResult:
        user_prompt = f"User message: {message}"

        raw = call_llm(TRIAGE_SYSTEM_PROMPT, user_prompt)

        try:
            data = json.loads(raw)
        except Exception:
            # fallback if the LLM misbehaves
            data = {
                "intent": "unknown",
                "domain": "general",
                "urgency": "normal",
                "confidence": 0.3,
            }

        return IntentResult(
            user_id=user_id,
            raw_message=message,
            intent=data.get("intent", "unknown"),
            domain=data.get("domain", "general"),
            confidence=float(data.get("confidence", 0.3)),
            urgency=data.get("urgency", "normal"),
        )
