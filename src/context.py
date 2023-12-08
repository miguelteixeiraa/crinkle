from typing import Generic, Optional, TypeVar, TypeAlias

from pydantic import BaseModel

T = TypeVar("T")
D = TypeVar("D")


class Context(BaseModel, Generic[T, D]):
    state: T
    additional_data: Optional[D]

    def __init__(self, initial_state: T, additional_data: Optional[D]):
        super().__init__(state=initial_state, additional_data=additional_data)


ContextType: TypeAlias = Context[T, D]
