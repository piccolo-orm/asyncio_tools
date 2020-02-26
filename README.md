# asyncio_tools

Useful utilities for working with asyncio.

## gather

Provides a convenient wrapper around `asyncio.gather`.

```python
from asyncio_tools import gather, CompoundException


async def good():
    return 'OK'


async def bad():
    raise ValueError()


async def main():
    response = await gather(
        good(),
        bad(),
        good()
    )

    # Check if a particular exception was raised.
    ValueError in response.exception_types
    # >>> True

    # To get all exceptions:
    print(response.exceptions)
    # >>> [ValueError()]

    # To get all instances of a particular exception:
    response.exceptions_of_type(ValueError)
    # >>> [ValueError()]

    # To get the number of exceptions:
    print(response.exception_count)
    # >>> 1

    # You can still access all of the results:
    print(response.all)
    # >>> ['OK', ValueError(), 'OK']

    # And can access all successes (i.e. non-exceptions):
    print(response.successes)
    # >>> ['OK', 'OK']

    # To get the number of successes:
    print(response.success_count)
    # >>> 2

    try:
        # To combines all of the exceptions into a single one, which merges the
        # messages.
        raise response.compound_exception()
    except CompoundException as compound_exception:
        print("Caught it")

        if ValueError in compound_exception.exception_types:
            print("Caught a ValueError")

```

Read some background on why `gather` is useful:

- https://www.piccolo-orm.com/blog/exception-handling-in-asyncio/
- https://www.piccolo-orm.com/blog/asyncio-gather/
