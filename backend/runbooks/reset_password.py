def run(inputs: dict) -> dict: 
    user_id = inputs.get("user_id") 
    reason =inputs.get("reason", "unspecified")
    # fake: we "reset" and return a masked password or a message 
    return {
        "status": "success", 
        "details": {
            "user_id": user_id, 
            "reason": reason, 
            "note": "Password reset via standard self-service flow."
        }
    }