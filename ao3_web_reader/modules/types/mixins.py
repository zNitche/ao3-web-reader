from typing import Any


class SerializableObjectMixin:
    def to_dict(self) -> dict[str, Any]:
        d = {}

        for key, value in self.__dict__.items():
            if value is not None:
                d[key] = value

        return d
    
    @classmethod
    def from_dict(cls, **kwargs):
        target_kwargs = {}

        for key, value in kwargs.items():
            target_kwargs[key] = value

        return cls(**target_kwargs)

    
    def __str__(self) -> str:
        return str(self.__dict__)
