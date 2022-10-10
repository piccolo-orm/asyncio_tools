from __future__ import annotations
import asyncio
from functools import cached_property
import typing as t


__VERSION__ = "1.0.0"


class CompoundException(Exception):
    """
    Is used to aggregate several exceptions into a single exception, with a
    combined message. It contains a reference to the constituent exceptions.
    """

    def __init__(self, exceptions: t.List[Exception]):
        self.exceptions = exceptions

    def __str__(self):
        return (
            f"CompoundException, {len(self.exceptions)} errors ["
            + "; ".join(
                [
                    f"{i.__class__.__name__}: {i.__str__()}"
                    for i in self.exceptions
                ]
            )
            + "]"
        )

    @cached_property
    def exception_types(self) -> t.List[t.Type[Exception]]:
        """
        Returns the constituent exception types.

        Useful for checks like this:

        if TransactionError in compound_exception.exception_types:
            some_transaction_cleanup()

        """
        return [i.__class__ for i in self.exceptions]


class GatheredResults:

    # __dict__ is required for cached_property
    __slots__ = ("__results", "__dict__")

    def __init__(self, results: t.List[t.Any]):
        self.__results = results

    ###########################################################################

    @property
    def results(self):
        return self.__results

    @property
    def all(self) -> t.List[t.Any]:
        """
        Just a proxy.
        """
        return self.__results

    ###########################################################################

    @cached_property
    def exceptions(self) -> t.List[t.Type[Exception]]:
        """
        Returns all exception instances which were returned by asyncio.gather.
        """
        return [i for i in self.results if isinstance(i, Exception)]

    def exceptions_of_type(
        self, exception_type: t.Type[Exception]
    ) -> t.List[t.Type[Exception]]:
        """
        Returns any exceptions of the given type.
        """
        return [i for i in self.exceptions if isinstance(i, exception_type)]

    @cached_property
    def exception_types(self) -> t.List[t.Type[Exception]]:
        """
        Returns the exception types which appeared in the response.
        """
        return [i.__class__ for i in self.exceptions]

    @cached_property
    def exception_count(self) -> int:
        return len(self.exceptions)

    ###########################################################################

    @cached_property
    def successes(self) -> t.List[t.Any]:
        """
        Returns all values in the response which aren't exceptions.
        """
        return [i for i in self.results if not isinstance(i, Exception)]

    @cached_property
    def success_count(self) -> int:
        return len(self.successes)

    ###########################################################################

    def compound_exception(self) -> t.Optional[CompoundException]:
        """
        Create a single exception which combines all of the exceptions.

        A function instead of a property to leave room for some extra args
        in the future.

        raise gathered_response.compound_exception()
        """
        if not self.exceptions:
            return False

        return CompoundException(self.exceptions)


async def gather(*coroutines: t.Sequence[t.Coroutine]) -> GatheredResults:
    """
    A wrapper on top of asyncio.gather which makes handling the results
    easier.
    """
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    return GatheredResults(results)
