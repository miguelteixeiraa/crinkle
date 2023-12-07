import asyncio
from typing import (
    Generic,
    TypeVar,
    List,
    Optional,
    Callable,
)
from pydantic import BaseModel
from collections import deque

from src.context import Context
from src.processor import (
    TypeFunctionProcessorAsync,
    TypeFunctionProcessor,
    FunctionProcessor,
    FunctionProcessorAsync,
    AbstractProcessorBase,
)

T = TypeVar("T")


class Flow(BaseModel, Generic[T]):
    name: str
    current_processor: Optional[str] = ""
    _processors: deque[AbstractProcessorBase] = deque()

    def __init__(self, name: str, processors: Optional[List[Processor]]):
        super().__init__(name=name)
        if processors is None:
            processors = []
        self._processors.extend(processors)
        self._name = name

    def add_processor(self, processor: AbstractProcessorBase) -> None:
        if not isinstance(processor, AbstractProcessorBase):
            raise TypeError(
                f"Invalid processor type: {type(processor)}. Expected inheritance from Processor."
            )
        self._processors.append(processor)

    def processor(
        self, name: str
    ) -> Callable[[TypeFunctionProcessor | TypeFunctionProcessorAsync], None]:
        def decorator(
            function_processor: TypeFunctionProcessor | TypeFunctionProcessorAsync,
        ) -> None:
            if asyncio.iscoroutinefunction(function_processor):
                self.add_processor(
                    processor=FunctionProcessorAsync(func=function_processor, name=name)
                )
                return

            self.add_processor(
                processor=FunctionProcessor(func=function_processor, name=name)
            )

        return decorator

    def execute(self, context: Context):
        loop = asyncio.get_event_loop()
        if any(
            self._run_procssor(func=processor, context=context)
            for processor in self._processors
        ):
            return

    def _run_processor(
        self, context: Context, func: FunctionProcessorAsync | FunctionProcessor
    ):
        self.current_processor = func.name
        if not (asyncio.iscoroutinefunction(func.process)):
            return func.process(context=context)

        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(func.process(context=context))

        loop.run_until_complete(task)

        result = task.result()
        return result

    def get_current_processor(self) -> str:
        return self.current_processor or ""
<<<<<<< Updated upstream

    def get_processors(self):
        return self._processors

    def _set_current_processor(self, current_processor: str) -> False:
        self.current_processor = current_processor
        return False
=======
>>>>>>> Stashed changes
