"""Pytest configuration and shared fixtures."""
import os

import pytest

from utilities.api_helpers import APIClient


def pytest_addoption(parser):
    """Add custom command line options for API tests."""
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Base URL for the API under test (overrides BASE_URL env var)"
    )
    parser.addoption(
        "--timeout",
        action="store",
        type=int,
        default=None,
        help="Request timeout in seconds (overrides TIMEOUT env var)"
    )


@pytest.fixture(scope="session")
def api_config(request):
    """Load API configuration from environment variables with command-line overrides."""
    config = {
        "base_url": os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com"),
        "timeout": int(os.getenv("TIMEOUT", "30")),
        "retries": int(os.getenv("RETRIES", "3")),
        "headers": {
            "Content-Type": os.getenv("CONTENT_TYPE", "application/json")
        }
    }

    # Override with command line options if provided
    base_url = request.config.getoption("--base-url")
    if base_url:
        config["base_url"] = base_url

    timeout = request.config.getoption("--timeout")
    if timeout is not None:
        config["timeout"] = timeout

    return config


@pytest.fixture(scope="session")
def api_client(api_config):
    """Create and return an APIClient instance."""
    client = APIClient(
        base_url=api_config["base_url"],
        timeout=api_config.get("timeout", 30)
    )

    # Set default headers from config
    headers = api_config.get("headers", {})
    if headers:
        client.set_headers(headers)

    return client
