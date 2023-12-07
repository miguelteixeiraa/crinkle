from collections import deque

import pytest

from src.context import Context
from src.flow import Flow
from src.processor import Processor

@pytest.fixture
def dummy_processor():
    class DummyProcessor(Processor):
        def process(self, context: Context) -> bool:
            return True
    return DummyProcessor

def test_flow_constructor_with_processors(dummy_processor):
    processors = [
        dummy_processor(),
        dummy_processor(),
        dummy_processor(),
    ]
    flow = Flow(name="Dummy", processors=processors)

    assert flow.name == "Dummy"
    assert flow.get_processors() == deque(processors)


def test_flow_constructor_without_processors():
    flow = Flow(name="Dummy")

    assert flow.name == "Dummy"
    assert flow.get_processors() == deque()


def test_flow_constructor_with_invalid_processors():
    invalid_processors = [1, "not_a_processor", {}]

    #with pytest.raises(ValueError):
    flow = Flow(name="Invalid Processors Flow", processors=[1])


def test_flow_constructor_with_optional_parameters():
    additional_data = {"key": "value"}
    flow = Flow(name="Optional Params Flow", processors=[], additional_data=additional_data)

    assert flow.name == "Optional Params Flow"
    assert flow.get_processors() == []


def test_flow_add_processor_should_add_processor_to_flow():
    flow = Flow(name="Dummy")

    class DummyProcessor(Processor):
        def process(self, context: Context) -> bool:
            return True

    dummy_processor = DummyProcessor()
    flow.add_processor(dummy_processor)

    assert flow.get_processors()[0] == dummy_processor


def test_flow_processor_method_should_work_as_an_annotation_factory_to_add_processors():
    flow = Flow(name="Dummy")

    @flow.processor(name="Dummy Processor")
    def dummy_processor(_: Context) -> bool:
        return True

    assert flow.get_processors()[0].name == "Dummy Processor"


def test_get_processors_should_return_processors():
    flow = Flow(name="Dummy")

    @flow.processor(name="Dummy Processor")
    def dummy_processor(context: Context) -> bool:
        return True

    assert len(flow.get_processors())


def test_execute_should_execute_all_processors_until_one_return_true_case1():
    flow = Flow(name="Dummy")

    @flow.processor(name="Dummy Processor 1")
    def dummy_processor_1(_: Context) -> bool:
        return False

    @flow.processor(name="Dummy Processor 2")
    def dummy_processor_2(_: Context) -> bool:
        return False

    @flow.processor(name="Dummy Processor 3")
    def dummy_processor_3(_: Context) -> bool:
        return False

    initial_state = "dummy state"
    additional_data = "dummy additional data"
    context = Context[str, str](
        initial_state=initial_state, additional_data=additional_data
    )

    flow.execute(context=context)

    assert flow.get_current_processor() == "Dummy Processor 3"


def test_execute_should_execute_all_processors_until_one_return_true_case2():
    flow = Flow(name="Dummy")

    @flow.processor(name="Dummy Processor 1")
    def dummy_processor_1(_: Context) -> bool:
        return False

    @flow.processor(name="Dummy Processor 2")
    def dummy_processor_2(_: Context) -> bool:
        return True

    @flow.processor(name="Dummy Processor 3")
    def dummy_processor_3(_: Context) -> bool:
        return False

    initial_state = "dummy state"
    additional_data = "dummy additional data"
    context = Context[str, str](
        initial_state=initial_state, additional_data=additional_data
    )

    flow.execute(context=context)

    assert flow.get_current_processor() == "Dummy Processor 2"
