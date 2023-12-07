from abc import ABC, abstractmethod
from typing import Callable, Optional
from src.context import Context


class Processor(ABC):
    name: Optional[str] = ""

    @abstractmethod
    def process(self, context: Context) -> bool:
        pass


TypeFunctionProcessor = Callable[[Context], bool]


class FunctionProcessor(Processor):
    def __init__(self, func: TypeFunctionProcessor, name: Optional[str] = ""):
        self.func = func
        self.name = name

    def process(
        self,
        context: Context,
    ) -> bool:
        return self.func(context)
