from typing import Dict

import pytest
from pydantic import BaseModel
from crinkle import Context


def test_context_generics_case1():
    class State(BaseModel):
        dummy: str

    initial_state = State(dummy='dummy')
    additional_data = {'foo': 'bar'}

    context = Context(initial_state=initial_state, additional_data=additional_data)

    assert context.state == initial_state
    assert context.additional_data == additional_data


def test_context_generics_case2():
    initial_state = 'dummy'
    additional_data = {'foo': 'bar'}

    context = Context[str, dict](
        initial_state=initial_state, additional_data=additional_data
    )

    assert context.state == initial_state
    assert context.additional_data == additional_data


def test_context_generics_case3():
    class State(BaseModel):
        dummy: str

    initial_state = State(dummy='dummy')
    additional_data = {'foo': 'bar'}

    context = Context[State, Dict](
        initial_state=initial_state, additional_data=additional_data
    )

    assert context.state == initial_state
    assert context.additional_data == additional_data


def test_context_model_optional_additional_data():
    initial_state = 'example_state'

    context = Context(initial_state=initial_state, additional_data=None)

    assert context.state == initial_state
    assert context.additional_data is None


def test_context_model_invalid_additional_data():
    initial_state = 'this_should_be_an_int'
    invalid_data = 'this_should_be_a_dict'

    with pytest.raises(ValueError):
        Context[dict, int](initial_state=initial_state, additional_data=invalid_data)
