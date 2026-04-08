from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        pass