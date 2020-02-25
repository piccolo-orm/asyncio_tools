import asyncio
from unittest import TestCase

from asyncio_tools import gather, CompoundException, GatheredResults


async def good():
    return "OK"


async def bad():
    raise ValueError("Bad value")


class TestGatheredResults(TestCase):
    def test_exceptions(self):
        response: GatheredResults = asyncio.run(gather(good(), bad(), good()))
        self.assertTrue(ValueError in response.exception_types)
        self.assertTrue(response.exception_count == 1)

    def test_successes(self):
        response: GatheredResults = asyncio.run(gather(good(), bad(), good()))
        self.assertTrue(response.successes == ["OK", "OK"])
        self.assertTrue(response.success_count == 2)

    def test_compound_exception(self):
        response: GatheredResults = asyncio.run(
            gather(good(), bad(), good(), bad())
        )

        with self.assertRaises(CompoundException):
            raise response.compound_exception()

        exception = response.compound_exception()
        self.assertTrue(ValueError in exception.exception_types)

    def test_set(self):
        results = GatheredResults([])
        with self.assertRaises(ValueError):
            results.results = None
