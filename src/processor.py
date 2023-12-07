from abc import ABC, abstractmethod
from typing import (
    Callable,
    Optional,
    Awaitable,
    TypeAlias,
    ParamSpec,
)

from src.context import Context

ContextSpec: TypeAlias = ParamSpec("ContextSpec", bound=Context)
TypeFunctionProcessor: TypeAlias = Callable[[ContextSpec], bool]
TypeFunctionProcessorAsync: TypeAlias = Callable[[ContextSpec], Awaitable[bool]]


class AbstractProcessorBase(ABC):
    name: Optional[str] = ""

    @abstractmethod
    def process(self, context: ContextSpec) -> bool:
        pass


class Processor(AbstractProcessorBase):
    pass


class ProcessorAsync(AbstractProcessorBase):
    @abstractmethod
    async def process(self, context: ContextSpec) -> bool:
        pass


class FunctionProcessor(Processor):
    def __init__(self, func: TypeFunctionProcessor, name: Optional[str] = ""):
        self.func = func
        self.name = name

    def process(
        self,
        context: Context,
    ) -> bool:
        return self.func(context)


class FunctionProcessorAsync(ProcessorAsync):
    def __init__(self, func: TypeFunctionProcessorAsync, name: Optional[str] = ""):
        self.func = func
        self.name = name

    async def process(self, context: Context) -> bool:
        return await self.func(context)
