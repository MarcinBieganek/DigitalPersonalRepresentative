from abc import ABC, abstractmethod

class Tool(ABC):
    @property
    @abstractmethod
    def json_schema(self):
        pass

    @abstractmethod
    def run(self, **kwargs):
        pass

    def get_required(self, kwargs, key, expected_type=str, default=None):
        value = kwargs.get(key, default)

        if value is None:
            raise ValueError(f"Missing '{key}'")
        if expected_type and not isinstance(value, expected_type):
            raise ValueError(f"'{key}' must be of type {expected_type}")
        
        return value
