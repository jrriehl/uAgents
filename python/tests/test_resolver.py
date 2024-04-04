import asyncio
import unittest
from uagents.resolver import RulesBasedResolver


class TestRulesBasedResolver(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.resolver = RulesBasedResolver(
            rules={
                "agent1qt0487g004xezsz8cte4827t7y847gzr5n6enwv6rrk09l0cjfl62rmnx79": ["http://localhost:8000/submit"]*15,
            }
        )

    async def test_resolve_normal(self):
        expected_agent = "agent1qt0487g004xezsz8cte4827t7y847gzr5n6enwv6rrk09l0cjfl62rmnx79"
        destination, endpoints = await self.resolver.resolve(expected_agent)
        self.assertEqual(len(endpoints), 10)
        self.assertEqual(destination, expected_agent)

    async def test_resolve_not_registered(self):
        not_registered_agent = "agent1q992tl7j9062ussaunq6vp5p4qaqugkzp8pva3xlszmeg0533k952lz8alf"
        destination2, endpoints2 = await self.resolver.resolve(not_registered_agent)
        self.assertEqual(len(endpoints2), 0)
        self.assertEqual(destination2, not_registered_agent)

if __name__ == '__main__':
    unittest.main()
