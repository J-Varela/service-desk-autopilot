from backend.agents.base_agent import BaseAgent
from backend.models.plan import PlanResult

class SafetyDecision(dict):
    @property
    def block(self) -> bool:
        return self.get("block", False)

class SafetyAgent(BaseAgent):
    name = "safety"

    def describe(self) -> str:
        return "Applies policy rules to planned actions."

    def evaluate(self, plan: PlanResult, context: dict) -> SafetyDecision:
        user = context["user"]

        # VERY simple example:
        # block if unknown user or no actions
        if not user or not plan.actions:
            return SafetyDecision(block=True, reason="No actions or unknown user")

        # You can add:
        # - role checks
        # - rate limits
        # - high-risk runbook restrictions
        return SafetyDecision(block=False, reason="Allowed")
