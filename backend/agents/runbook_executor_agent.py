from backend.agents.base_agent import BaseAgent
from backend.models.plan import PlanAction
from backend.runbooks import check_account_status, reset_password, lookup_pto_balance

RUNBOOK_MAP = {
    "check_account_status": check_account_status.run,
    "reset_password": reset_password.run,
    "lookup_pto_balance": lookup_pto_balance.run,
}

class RunbookExecutorAgent(BaseAgent):
    name = "runbook_executor"

    def describe(self) -> str:
        return "Executes runbooks and returns structured results."

    def execute(self, action: PlanAction, context: dict) -> dict:
        fn = RUNBOOK_MAP.get(action.runbook_id)
        if not fn:
            return {
                "runbook_id": action.runbook_id,
                "status": "error",
                "details": {"error": "Runbook not found"},
            }
        result = fn(action.inputs)
        result["runbook_id"] = action.runbook_id
        return result
