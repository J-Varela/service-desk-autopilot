def run(inputs: dict) -> dict: 
    user_id = inputs.get("user_id") 
    # fake logic 
    return {
        "status": "success", 
        "details": { 
            "user_id": user_id, 
            "account_status": "locked", 
            "reason": "too_many_failed_attempts",
        },
    }