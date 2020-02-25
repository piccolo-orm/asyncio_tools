import asyncio
from unittest import TestCase

from asyncio_tools import gather


async def good():
    return True


async def bad():
    raise Exception()


class TestGatheredResults(TestCase):

    async def contains(self):
        results = await gather(
            good(),
            bad(),
            good(),
        )

        self.assertTrue(Exception in results)

    def test_contains(self):
        asyncio.run(self.contains())
