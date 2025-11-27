from pydantic import BaseModel 
from typing import List, Dict, Any 

class PlanAction(BaseModel): 
    runbook_id: str 
    inputs: Dict[str, Any] 

class PlanResult(BaseModel): 
    actions: List[PlanAction] 
    requires_human_approval: bool = False 
    