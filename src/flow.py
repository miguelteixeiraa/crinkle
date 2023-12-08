import asyncio
from typing import (
    List,
    Optional,
    Callable,
    Union,
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


class Flow(BaseModel):
    name: str
    current_processor: Optional[str] = ""
    _processors: deque[AbstractProcessorBase] = deque()

    def __init__(
        self, name: str, processors: Optional[List[AbstractProcessorBase]] = None
    ):
        super().__init__(name=name)
        if processors is None:
            processors = []

        if any(
            not isinstance(processor, AbstractProcessorBase) for processor in processors
        ):
            raise ValueError(
                "Invalid processors iterable. Must be instance of AbstractProcessorBase"
            )
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
    ) -> Callable[[Union[TypeFunctionProcessor, TypeFunctionProcessorAsync]], None]:
        def decorator(
            function_processor: Union[
                TypeFunctionProcessor, TypeFunctionProcessorAsync
            ],
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
        if any(
            self._run_processor(func=processor, context=context)
            for processor in self._processors
        ):
            return

    def _run_processor(
        self,
        context: Context,
        func: Union[AbstractProcessorBase, FunctionProcessor, FunctionProcessorAsync],
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

    def get_processors(self) -> deque:
        return self._processors
