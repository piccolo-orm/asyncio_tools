import asyncio

import typing as t


class GatheredResults:

    __slots__ = ("results", "exceptions")

    def __init__(self, results):
        self.results = results
        self.exceptions = [
            i for i in results if isinstance(i, Exception)
        ]

    def has_exception(self, exception_class: Exception):
        for i in self.exceptions:
            if isinstance(i, exception_class):
                return True

    def __contains__(self, exception_class: Exception):
        return self.has_exception(exception_class)


async def gather(*coroutines: t.Sequence[t.Coroutine]) -> GatheredResults:
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    return GatheredResults(results)
