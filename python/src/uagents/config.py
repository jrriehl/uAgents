import logging
import sys
from typing import Any, Dict, List, Optional, Union

from uvicorn.logging import DefaultFormatter

logging.basicConfig(level=logging.INFO)


# Prefix used for agents.
AGENT_PREFIX = "agent"
# Prefix used for ledger.
LEDGER_PREFIX = "fetch"
# Prefix used for users.
USER_PREFIX = "user"
# Prefix used for testing net.
TESTNET_PREFIX = "test-agent"
# Prefix used for main network.
MAINNET_PREFIX = "agent"
# Length of the agent address.
AGENT_ADDRESS_LENGTH = 65

# Almanac contract for the main network.
MAINNET_CONTRACT_ALMANAC = (
    "fetch1mezzhfj7qgveewzwzdk6lz5sae4dunpmmsjr9u7z0tpmdsae8zmquq3y0y"
)
# Almanac contract for the test network.
TESTNET_CONTRACT_ALMANAC = (
    "fetch1tjagw8g8nn4cwuw00cf0m5tl4l6wfw9c0ue507fhx9e3yrsck8zs0l3q4w"
)
# Name service contract for the main network.
MAINNET_CONTRACT_NAME_SERVICE = (
    "fetch1479lwv5vy8skute5cycuz727e55spkhxut0valrcm38x9caa2x8q99ef0q"
)
# Name service contract for the test network.
TESTNET_CONTRACT_NAME_SERVICE = (
    "fetch1mxz8kn3l5ksaftx8a9pj9a6prpzk2uhxnqdkwuqvuh37tw80xu6qges77l"
)
# Fee to be paid for registration.
REGISTRATION_FEE = 500000000000000000
# The denomination of the fee to be paid for registration.
REGISTRATION_DENOM = "atestfet"
# Time in seconds between registration updates.
REGISTRATION_UPDATE_INTERVAL_SECONDS = 3600
# Time in seconds between registration retry attempts.
REGISTRATION_RETRY_INTERVAL_SECONDS = 60
# Average time interval between blocks.
AVERAGE_BLOCK_INTERVAL = 6

# The base URL for the agentverse.
AGENTVERSE_URL = "https://agentverse.ai"
# The API URL for the almanac.
ALMANAC_API_URL = AGENTVERSE_URL + "/v1/almanac/"
# Time interval between mailbox polling in seconds.
MAILBOX_POLL_INTERVAL_SECONDS = 1.0

# Time interval between wallet messaging polls in seconds.
WALLET_MESSAGING_POLL_INTERVAL_SECONDS = 2.0

# Suggested response time in seconds.
RESPONSE_TIME_HINT_SECONDS = 5
# Default timeout for envelope in seconds.
DEFAULT_ENVELOPE_TIMEOUT_SECONDS = 30
# Maximum number of end points by default.
DEFAULT_MAX_ENDPOINTS = 10
# Default search limit.
DEFAULT_SEARCH_LIMIT = 100


def parse_endpoint_config(
    endpoint: Optional[Union[str, List[str], Dict[str, dict]]],
) -> List[Dict[str, Any]]:
    """
    Parse the user-provided endpoint configuration.

    Args:
        endpoint: A string, list or dictionary representing the endpoint configuration.

    Returns:
        List[Dict[str, Any]]: The parsed endpoint configuration.
    """
    if isinstance(endpoint, dict):
        endpoints = [
            {"url": val[0], "weight": val[1].get("weight") or 1}
            for val in endpoint.items()
        ]
    elif isinstance(endpoint, list):
        endpoints = [{"url": val, "weight": 1} for val in endpoint]
    elif isinstance(endpoint, str):
        endpoints = [{"url": endpoint, "weight": 1}]
    else:
        endpoints = None
    return endpoints


def parse_agentverse_config(
    config: Optional[Union[str, Dict[str, str]]] = None,
) -> Dict[str, str]:
    """
    Parse the user-provided agentverse configuration.

    Args:
        config: A string or dictionary representing the AgentVerse configuration.

    Returns:
        Dict[str, str]: The parsed agentverse configuration.
    """
    agent_mailbox_key = None
    base_url = AGENTVERSE_URL
    protocol = None
    protocol_override = None
    if isinstance(config, str):
        if config.count("@") == 1:
            agent_mailbox_key, base_url = config.split("@")
        elif "://" in config:
            base_url = config
        else:
            agent_mailbox_key = config
    elif isinstance(config, dict):
        agent_mailbox_key = config.get("agent_mailbox_key")
        base_url = config.get("base_url") or base_url
        protocol_override = config.get("protocol")
    if "://" in base_url:
        protocol, base_url = base_url.split("://")
    protocol = protocol_override or protocol or "https"
    http_prefix = "https" if protocol in {"wss", "https"} else "http"
    return {
        "agent_mailbox_key": agent_mailbox_key,
        "base_url": base_url,
        "protocol": protocol,
        "http_prefix": http_prefix,
        "use_mailbox": agent_mailbox_key is not None,
    }


def get_logger(logger_name, level=logging.INFO):
    """Get a logger with the given name using uvicorn's default formatter."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(
        DefaultFormatter(fmt="%(levelprefix)s [%(name)5s]: %(message)s")
    )
    logger.addHandler(log_handler)
    logger.propagate = False
    return logger
