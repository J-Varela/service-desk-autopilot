from backend.agents.triage_agent import TriageAgent
from backend.agents.enrichment_agent import EnrichmentAgent
from backend.agents.planner_agent import PlannerAgent
from backend.agents.safety_agent import SafetyAgent
from backend.agents.runbook_executor_agent import RunbookExecutorAgent
from backend.agents.escalation_agent import EscalationAgent
from backend.models.intent import IntentResult
from backend.models.plan import PlanResult


triage_agent = TriageAgent()
enrichment_agent = EnrichmentAgent()
planner_agent = PlannerAgent()
safety_agent = SafetyAgent()
runbook_executor = RunbookExecutorAgent()
escalation_agent = EscalationAgent()

def handle_chat(user_id: str, message: str):
    activity_log = []

    # 1) Triage
    intent: IntentResult = triage_agent.infer_intent(user_id, message)
    activity_log.append({"step": "triage", "details": intent.dict()})

    # 2) Enrichment (user profile, history...)
    enriched_context = enrichment_agent.enrich(user_id, intent)
    activity_log.append({"step": "enrichment", "details": enriched_context})

    # 3) Planning (which runbooks, which checks)
    plan: PlanResult = planner_agent.create_plan(enriched_context)
    activity_log.append({"step": "planning", "details": plan.dict()})

    # 4) Safety check
    safety_decision = safety_agent.evaluate(plan, enriched_context)
    activity_log.append({"step": "safety", "details": safety_decision})

    if safety_decision.block:
        # Escalate immediately
        ticket = escalation_agent.create_ticket(user_id, message, enriched_context, plan)
        activity_log.append({"step": "escalation", "details": ticket})
        reply = (
            "I couldn't safely automate this. "
            f"I created a ticket for a human agent: {ticket.get('ticket_id')}"
        )
        return reply, activity_log

    # 5) Execute runbooks
    runbook_results = []
    for action in plan.actions:
        result = runbook_executor.execute(action, enriched_context)
        runbook_results.append(result)

    activity_log.append({"step": "runbook_execution", "details": runbook_results})

    # 6) Final reply to user (simple version for now)
    reply = planner_agent.summarize_for_user(intent, runbook_results)

    return reply, activity_log
