from backend.agents.base_agent import BaseAgent
from backend.models.plan import PlanResult
from typing import Dict, Any 
import json 
import os 

class SafetyDecision(dict):
    @property
    def block(self) -> bool:
        return self.get("block", False)
    
    @property 
    def reason(self) -> str: 
        return self.get("reason", "")

class SafetyAgent(BaseAgent):
    name = "safety"

    def __init__(self): 
        # Load runbook catalog on init 
        catalog_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "config", 
            "runbook_catalog.json"
        )
        catalog_path = os.path.abspath(catalog_path)
        with open(catalog_path, "r") as f: 
            self.runbook_catalog: Dict[str, Any] = json.load(f) 

    def describe(self) -> str:
        return "Applies policy rules to planned actions."

    def evaluate(self, plan: PlanResult, context: dict) -> SafetyDecision:
        user = context["user"]
        actions = plan.actions

        # block if unknown user
        if not user:
            return SafetyDecision(block=True, reason="Unknown user")
        
        if not actions: 
            return SafetyDecision(block=True, reason="No actions in plan")
        
        # Example policy: block if any unknown or high-risk runbook 
        for action in actions: 
            meta = self.runbook_catalog.get(action.runbook_id)
            if not meta: 
                return SafetyDecision(
                    block=True, 
                    reason=f"Runbook {action.runbook_id} is not registered in catalog"
                )
            
            risk = meta.get("risk_level", "low") 
            if risk == "high": 
                # For now, block high-risk entirely (or require human approval) 
                return SafetyDecision(
                    block=True, 
                    reason=f"Runbook {action.runbook_id} is high-risk and not auto-executable"
                )
    
        # You can add:
        # - role checks
        # - rate limits
        # - high-risk runbook restrictions
        return SafetyDecision(block=False, reason="All actions allowed by policy")
