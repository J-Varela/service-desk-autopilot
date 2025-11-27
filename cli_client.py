# cli_client.py
import httpx

BASE_URL = "http://localhost:8000"

def send_message(user_id: str, message: str):
    payload = {
        "user_id": user_id,
        "message": message
    }

    resp = httpx.post(f"{BASE_URL}/chat", json=payload, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()
    return data

def main():
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

        print(f"\n[assistant] {data['reply']}\n")

        # Optional: show activity log
        print("Activity log:")
        for step in data["activity_log"]:
            print(f" - {step['step']}: {step['details']}")
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()
