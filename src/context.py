from typing import Generic, Optional, ParamSpec, TypeAlias

from pydantic import BaseModel

T = ParamSpec("T")
D = ParamSpec("D")


class Context(BaseModel, Generic[T, D]):
    state: T
    additional_data: Optional[D]

    def __init__(self, initial_state: T, additional_data: Optional[D]):
        super().__init__(state=initial_state, additional_data=additional_data)


ContextType: TypeAlias = Context[T, D]
