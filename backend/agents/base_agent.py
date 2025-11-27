from abc import ABC, abstractmethod 

class BaseAgent(ABC): 
    name: str = "base" 

    @abstractmethod 
    def describe(self) -> str: 
        """Return a description of the agent.""" 
        pass