from typing import Generic, TypeVar, List, Optional, Any, Callable
from pydantic import BaseModel
from collections import deque

from src.context import Context
from src.processor import Processor, TypeFunctionProcessor, FunctionProcessor

T = TypeVar("T")


class Flow(BaseModel, Generic[T]):
    name: str
    current_processor: Optional[str] = ""
    _processors: deque[Processor] = deque()

    def __init__(
        self, name: str, processors: Optional[List[Processor]] = None, **data: Any
    ):
        super().__init__(**data)
        if processors is None:
            processors = []
        self._processors.extend(processors)
        self._name = name

    def add_processor(self, processor: Processor):
        if not isinstance(processor, Processor):
            raise TypeError(
                f"Invalid processor type: {type(processor)}. Expected inheritance from Processor."
            )
        self._processors.append(processor)

    def processor(self, name: str) -> Callable[[TypeFunctionProcessor], None]:
        def decorator(function_processor: TypeFunctionProcessor) -> None:
            self.add_processor(
                processor=FunctionProcessor(function_processor, name=name)
            )

        return decorator

    def execute(self, context: Context):
        if any(
            self._set_current_processor(processor.name)
            or processor.process(context=context)
            for processor in self._processors
        ):
            return

    def get_current_processor(self) -> str:
        return self.current_processor or ""

    def _set_current_processor(self, current_processor: str) -> False:
        self.current_processor = current_processor
        return False
