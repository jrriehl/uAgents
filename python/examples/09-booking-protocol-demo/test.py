from protocols.book import BookTableRequest, TableStatus, book_proto
from restaurant import restaurant
from uagents.experimental.test.tools import TestAgentProtocol

TABLES = {
    1: TableStatus(seats=2, time_start=16, time_end=22),
    2: TableStatus(seats=4, time_start=19, time_end=21),
    3: TableStatus(seats=4, time_start=17, time_end=19),
}


class TestBookProtocol(TestAgentProtocol):
    def setUp(self) -> None:
        for number, status in TABLES.items():
            self.context.storage.set(number, status.dict())
        return super().setUp()

    agentproto = book_proto
    sample_requests = [
        BookTableRequest(table_number=1, time_start=0, duration=30),
        BookTableRequest(table_number=2, time_start=0, duration=30),
        BookTableRequest(table_number=3, time_start=0, duration=30),
    ]

    async def test_message_handlers(self):
        await self.message_handlers_test()

    async def test_intervals(self):
        await self.intervals_test()


class TestRestaurant(TestAgentProtocol):
    def setUp(self) -> None:
        for number, status in TABLES.items():
            self.context.storage.set(number, status.dict())
        return super().setUp()

    agentproto = restaurant

    sample_requests = [
        BookTableRequest(table_number=1, time_start=0, duration=30),
        BookTableRequest(table_number=2, time_start=0, duration=30),
        BookTableRequest(table_number=3, time_start=0, duration=30),
    ]

    async def test_message_handlers(self):
        await self.message_handlers_test()

    async def test_intervals(self):
        await self.intervals_test()
