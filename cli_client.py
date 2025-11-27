# cli_client.py
import httpx
import json
import argparse
from typing import Any, Dict
from colorama import init as colorama_init, Fore, Style

BASE_URL = "http://localhost:8000"

colorama_init(autoreset=True)


STEP_COLOR = {
    "triage": Fore.CYAN,
    "enrichment": Fore.BLUE,
    "planning": Fore.MAGENTA,
    "safety": Fore.YELLOW,
    "escalation": Fore.RED,
    "runbook_execution": Fore.GREEN,
}

def summarize_step(step: Dict[str, Any]) -> str:
    """Return a concise human-friendly summary for a step."""
    name = step.get("step", "unknown")
    data = step.get("result") or step.get("details") or {}

    try:
        if name == "triage":
            return f"intent={data.get('intent')} confidence={data.get('confidence')} domain={data.get('domain')}"
        if name == "enrichment":
            user = data.get("user", {})
            return f"user={user.get('id')} dept={user.get('department')} role={user.get('role')}"
        if name == "planning":
            actions = data.get("actions", [])
            return f"actions={[a.get('runbook_id') for a in actions]} human_approval={data.get('requires_human_approval')}"
        if name == "safety":
            return f"block={data.get('block')} reason={data.get('reason')}"
        if name == "escalation":
            return f"ticket_id={data.get('ticket_id')} status={data.get('status','created')}"
        if name == "runbook_execution":
            if isinstance(data, list):
                parts = [f"{r.get('runbook_id')}:{r.get('status')}" for r in data]
                return "results=" + ", ".join(parts)
        # Fallback generic
        return json.dumps(data)[:200]
    except Exception:
        # Safe fallback if unexpected structure
        return str(data)[:200]

def pretty_print_step(step: Dict[str, Any]) -> None:
    name = step.get("step", "unknown")
    color = STEP_COLOR.get(name, Fore.WHITE)
    summary = summarize_step(step)
    print(f" {color}• {name:<18}{Style.DIM}{summary}{Style.RESET_ALL}")

def print_activity_log(activity_log: Any, verbose: bool = False) -> None:
    print(Style.BRIGHT + "Activity Pipeline:" + Style.RESET_ALL)
    for step in activity_log:
        if verbose:
            # Pretty-print full JSON for each step
            name = step.get("step", "unknown")
            data = step.get("result") or step.get("details") or {}
            color = STEP_COLOR.get(name, Fore.WHITE)
            print(f" {color}• {name}{Style.RESET_ALL}")
            print(Style.DIM + json.dumps(data, indent=2) + Style.RESET_ALL)
        else:
            pretty_print_step(step)
    print()

def send_message(user_id: str, message: str):
    payload = {
        "user_id": user_id,
        "message": message,
    }
    # Use explicit serialization to avoid lint complaints about keyword args
    raw = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    with httpx.Client(timeout=10.0) as client:
        resp = client.post(f"{BASE_URL}/chat", content=raw, headers=headers)
        resp.raise_for_status()
        return resp.json()

def main():
    parser = argparse.ArgumentParser(description="Service Desk Autopilot CLI")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed JSON for activity log")
    args = parser.parse_args()

    print("Service Desk Autopilot CLI")
    user_id = input("Enter your user id (e.g. jv-123): ").strip() or "demo-user"

    print("Type 'quit' to exit.\n")

    while True:
        msg = input("> ")
        if msg.lower() in ("quit", "exit"):
            break

        try:
            data = send_message(user_id, msg)
        except Exception as e:
            print(f"[error] {e}")
            continue

        print(f"\n{Fore.GREEN}[assistant]{Style.RESET_ALL} {data['reply']}\n")

        print_activity_log(data.get("activity_log", []), verbose=args.verbose)
        print(Style.DIM + "=" * 60 + Style.RESET_ALL + "\n")

if __name__ == "__main__":
    main()
