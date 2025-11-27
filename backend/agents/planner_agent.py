
from backend.agents.base_agent import BaseAgent
from backend.models.plan import PlanResult, PlanAction
from backend.utils.llm_client import call_llm
import json

PLANNER_SYSTEM_PROMPT = """
You are a planning agent for an internal service desk.

You receive a JSON object representing the user intent and context.
You must decide which runbooks (automations) to call.

Available runbooks (ids):
- check_account_status(user_id)
- reset_password(user_id, reason)
- lookup_pto_balance(user_id)

Rules:
- For account_access_issue in IT:
  - Always start with check_account_status.
  - If account is locked or user clearly can't log in, consider reset_password.
- For pto_balance in HR:
  - Use lookup_pto_balance.

Output ONLY valid JSON in this format:
{
  "requires_human_approval": false,
  "actions": [
    {"runbook_id": "check_account_status", "inputs": {"user_id": "abc"}},
    {"runbook_id": "reset_password", "inputs": {"user_id": "abc", "reason": "self_service_reset"}}
  ]
}
"""

class PlannerAgent(BaseAgent):
    name = "planner"

    def describe(self) -> str:
        return "Decides which runbooks to call using an LLM."

    def create_plan(self, context: dict) -> PlanResult:
        user = context["user"]
        intent = context["intent"]

        user_prompt = json.dumps(
            {
                "user": user,
                "intent": intent,
            },
            indent=2,
        )

        raw = call_llm(PLANNER_SYSTEM_PROMPT, user_prompt)

        try:
            data = json.loads(raw)
        except Exception:
            # fallback: no actions
            data = {"requires_human_approval": False, "actions": []}

        actions = [
            PlanAction(runbook_id=a["runbook_id"], inputs=a.get("inputs", {}))
            for a in data.get("actions", [])
        ]

        return PlanResult(
            actions=actions,
            requires_human_approval=data.get("requires_human_approval", False),
        )

    def summarize_for_user(self, intent_result, runbook_results: list) -> str:
        # You can later also LLM-ify this if you want a nicer explanation.
        intent = intent_result.intent

        if intent == "account_access_issue":
            return "I checked your account and ran the appropriate recovery steps. Please follow the instructions you received (e.g., email or SMS) to complete your login."
        elif intent == "pto_balance":
            if runbook_results:
                days = runbook_results[0].get("details", {}).get("remaining_days", "N/A")
                return f"You currently have {days} days of PTO remaining."
        return "I processed your request and logged the results."
