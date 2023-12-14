from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar('T')
D = TypeVar('D')


class Context(BaseModel, Generic[T, D]):
    state: T
    additional_data: Optional[D]

    model_config = ConfigDict(arbitrary_types_allowed=True)
    def __init__(self, initial_state: T, additional_data: Optional[D]):
        super().__init__(state=initial_state, additional_data=additional_data)
