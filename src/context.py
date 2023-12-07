from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

T = TypeVar("T")
D = TypeVar("D")


class Context(BaseModel, Generic[T, D]):
    state: T
    additional_data: Optional[D]

    def __init__(self, initial_state: T, additional_data: Optional[D]):
        super().__init__(state=initial_state, additional_data=additional_data)
