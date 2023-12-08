# Crinkle

**Crinkle** is a framework for organizing the execution of complex processing flows by implementing the “Chain of Responsability” pattern (:battery: included).

**Merchan**:

- **Minimalist**: Translate complex computational requirements into simple, yet elegant. _and less_ code.
- **Grow large**: Grow large while keep everything maintainable and fast
- **Empower testability**: Make things more testable by breaking large processes into small, specialized pieces with composition.
- **Opinionated Yet Intuitive**: Quickly understand and work with.

---

## Requirements

A recent and currently supported version of [Python](https://www.python.org/downloads/").

## Installation

```console
$ pip install crinkle
```

## Example

For an introduction to the Chain of Responsability Pattern and its use cases, see
[Chain of Responsibility by Refactoring Guru](https://refactoring.guru/design-patterns/chain-of-responsibility)

```Python hl_lines="18  21  23-27"
from pydantic import BaseModel
from typing import Dict, List
from crinkle import Context, Flow


class Order(BaseModel):
    loyalty: bool  # just to simplify the example
    items: List
    discounts: List


context = Context[Order, Dict](
    initial_state=Order(),
    additional_data={},  # Optional
)

flow = Flow(name='Promotions/Discounts Flow')


@flow.processor(name='Discounts pre-conditions Processor')
def discounts_pre_conditions_processor(context) -> bool:
    """
    **context** has code autocompletion for
    class Context(BaseModel, Generic[T, D]):
        state: T
        additional_data: Optional[D]

    which in this case is:

    class Context:
        state: Order
        additional_data: Dict
    """
    if context.state.loyalty:
        return False  # Go to next processor

    return True  # Stop flow without going to next processors


@flow.processor(name='Manufacturer Coupons Processor')
def manufacturer_coupons_processor(context) -> bool:
    # do stuff with context
    return False  # Go to next processor


# Async is also supported
@flow.processor(name='Buy one get one Processor')
async def bogo_processor(context) -> bool:
    # do stuff with context
    return False  # This is the last processor, so end of flow


# Just like Apache Commons Chain, the Flow will be forced to terminate
# if a processor returns True (this would mean processing is complete).

flow.execute(context)

# **context.state** has the state of the Order after all processing
```

### Using Object Oriented Programming (OOP)

Crinkle has flavors for all tastes! OOP is also supported, see example:

```Python hl_lines="15-18"
from typing import Dict, List
from crinkle import ProcessorBase, ProcessorBaseAsync, flow, Context


class Order(BaseModel):
    loyalty: bool  # just to simplify the example
    items: List
    discounts: List


context = Context[Order, Dict](
    initial_state=Order(),
    additional_data={},  # Optional
)


class DiscountsPreConditionsProcessor(ProcessorBase):
    def __init__(self, name: str):
        self.name = name

    def process(self, context: Context[Order, Dict]) -> bool:
        # Go to next processor
        if context.state.loyalty:
            return False

        return True  # Stop flow without going to next processors


class ManufacturerCouponsProcessor(ProcessorBase):
    def __init__(self, name: str):
        self.name = name

    def process(self, context: Context[Order, Dict]) -> bool:
        # do stuff with context
        return False  # Go to next processor


class BOGOProcessor(ProcessorBaseAsync):
    def __init__(self, name: str):
        self.name = name

    # Async is also supported
    async def process(self, context: Context[Order, Dict]) -> bool:
        # do stuff with context
        return False  # This is the last processor, so end of flow


flow = Flow(
    flow_name='Promotions/Discounts Flow',
    processors=[
        DiscountsPreConditionsProcessor(name='...'),
        ManufacturerCouponsProcessor(name='...'),
        BOGOProcessor(name='...'),
    ],
)
# OR
flow.add_processor(DiscountsPreConditionsProcessor(name='...'))
flow.add_processor(ManufacturerCouponsProcessor(name='...'))
flow.add_processor(BOGOProcessor(name='...'))


# Just like Apache Commons Chain, the Flow will be forced to terminate
# if a processor returns True (this would mean processing is complete).

flow.execute(context)

# **context.state** has the state of the Order after all processing

```

## License

This project is licensed under the terms of the [MIT license](https://github.com/miguelteixeiraa/crinkle/blob/main/LICENSE).
