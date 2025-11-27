def run(inputs: dict) -> dict:
    user_id = inputs.get("user_id")
    # fake: static number
    return {
        "status": "success",
        "details": {
            "user_id": user_id,
            "remaining_days": 12
        },
    }
