from abc import ABC, abstractmethod

class Tool(ABC):
    @property
    @abstractmethod
    def json_schema(self):
        pass

    @abstractmethod
    def run(self, **kwargs):
        pass
