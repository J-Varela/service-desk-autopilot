import uuid 

_FAKE_TICKETS = {} 

def create_ticket(summary: str, details: dict) -> str: 
    ticket_id = str(uuid.uuid4())[:8]
    _FAKE_TICKETS[ticket_id] = {"summary": summary, "details": details}

    return ticket_id 