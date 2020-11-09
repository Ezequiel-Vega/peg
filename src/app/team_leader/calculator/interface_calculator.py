from abc import ABC
from abc import abstractmethod

class ICalculator(ABC):
    """
        Interface del contructor Calculator
    """
    @abstractmethod
    def action(self, data: dict) -> dict:
        pass
