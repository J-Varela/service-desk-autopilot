def get_user_profile(user_id: str) -> dict: 
    # For now, return a fake user 
    return {
        "id": user_id, 
        "name": "Test User", 
        "department": "Engineering", 
        "location": "US", 
        "role": "Employee",
    }