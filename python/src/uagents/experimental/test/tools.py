import unittest
from typing import Union
from unittest.mock import patch

import pytest
from uagents import Agent, Context, Model, Protocol


class TestAgentProtocol(unittest.IsolatedAsyncioTestCase):
    sample_requests = []
    agentproto: Union[Agent, Protocol] = None
    context = Agent()._ctx

    def setUp(self) -> None:
        if isinstance(self.agentproto, Agent):
            self.agentproto.include(self.agentproto._protocol)
            self.context = self.agentproto._ctx
        super().setUp()

    async def message_handlers_test(self):
        if self.agentproto is None:
            raise unittest.SkipTest("Protocol instance not provided.")

        # Create a sample sender for testing
        sender = self.context.address

        # Call each message handler for each sample request and capture the messages sent
        for sample_request in self.sample_requests:
            schema_digest = Model.build_schema_digest(sample_request)
            handler = self.agentproto._signed_message_handlers.get(schema_digest)
            if handler is None:
                handler = self.agentproto._unsigned_message_handlers.get(schema_digest)
            if handler is None:
                self.fail(
                    f"No message handler found for incoming message type {type(sample_request)}"
                )
            with (
                self.subTest(sample_request=sample_request),
                patch.object(Context, "send") as mock_send,
            ):
                try:
                    # Verify that the messages sent are of the correct type according to
                    # protocol replies
                    await handler(self.context, sender, sample_request)
                    for call_args in mock_send.call_args_list:
                        _address, message = call_args[0]
                        if schema_digest in self.agentproto._replies:
                            self.assertIn(
                                type(message),
                                self.agentproto._replies[schema_digest].values(),
                                (
                                    f"Message type {type(message)} is not in the set of valid "
                                    f"replies for incoming message type {type(sample_request)}: "
                                    f"{self.agentproto._replies[schema_digest].values()}"
                                ),
                            )
                except Exception as ex:
                    self.fail(
                        f"Message handler for '{sample_request}' failed with error: {ex}"
                    )

    async def intervals_test(self):
        if self.agentproto is None:
            pytest.skip("Protocol instance not provided.")

        # Call each interval handler and verify that it is called
        for interval_handler in self.agentproto._interval_handlers:
            with (
                self.subTest(interval_handler=interval_handler),
                patch.object(Context, "send") as mock_send,
            ):
                try:
                    await interval_handler[0](self.context)
                    for call_args in mock_send.call_args_list:
                        _address, message = call_args[0]
                        if self.agentproto.interval_messages:
                            self.assertIn(
                                type(message),
                                self.agentproto.interval_messages,
                                (
                                    f"Message type {type(message)} is not in the set of valid "
                                    f"interval messages: {self.agentproto.interval_messages}"
                                ),
                            )
                except Exception as ex:
                    self.fail(
                        f"Interval handler for '{interval_handler}' failed with error: {ex}"
                    )
