# crinkle - WIP

**crinkle** is a simple, yet elegant, python implementation of the Chain of Responsibility pattern, inspired by the [Apache Commons Chain library](https://commons.apache.org/dormant/commons-chain/).

### Examples

```python
from typing import Dict, List
from pydantic import BaseModel
from crinkle import Context, Flow

class Order(BaseModel):
    items: List = []
    discounts: List = []

order = Order()
additional_data = {'foo': 'bar'}

context = Context[Order, Dict](
    initial_state=order,
    additional_data=additional_data  # Optional
)

flow = Flow(flow_name="Promotions/Discounts Flow")

@flow.processor(name="Manufacturer Discounts Processor")
def manufacturer_discounts_processor(context: Context[Order, Dict]) -> bool:
    # do stuff with context
    return False

@flow.processor(name="Buy one get one Processor")
async def bogo_processor(context: Context[Order, Dict]) -> bool:
     # do stuff with context
    return False

# Just like Apache Commons Chain, the Flow will be forced to terminate
# if a processor returns True (this would mean processing is complete).

flow.execute(context)

```
