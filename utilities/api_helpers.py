import logging
import os
from typing import Optional

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class APIClient:
    """Reusable API client wrapper for requests library."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self._default_headers = {
            "Content-Type": "application/json"
        }
        logger.info(f"APIClient initialized with base_url: {base_url}")

    def set_headers(self, headers: dict) -> None:
        """Set default headers for all requests."""
        self._default_headers.update(headers)
        self.session.headers.update(headers)
        logger.info(f"Headers updated: {headers}")

    def _log_request(self, method: str, endpoint: str) -> None:
        """Log request details."""
        logger.info(f"Request: {method} {endpoint}")

    def _log_response(self, response: requests.Response) -> None:
        """Log response details."""
        logger.info(f"Response: {response.status_code} for {response.request.method} {response.request.url}")
        if response.status_code >= 400:
            logger.error(f"Error response: {response.text}")

    def _check_response(self, response: requests.Response) -> requests.Response:
        """Check response status and raise custom exception for non-2xx responses."""
        if response.status_code >= 200 and response.status_code < 300:
            return response

        error_msg = f"API request failed with status {response.status_code}"
        if response.text:
            error_msg += f": {response.text[:200]}"

        raise APIError(error_msg, status_code=response.status_code)

    def _handle_request_exception(self, exception: requests.RequestException, method: str, url: str) -> None:
        """Handle requests library exceptions and raise custom APIError."""
        error_msg = f"{method} request to {url} failed"

        if isinstance(exception, requests.exceptions.Timeout):
            error_msg += ": Request timed out"
        elif isinstance(exception, requests.exceptions.ConnectionError):
            error_msg += ": Connection error"
        elif isinstance(exception, requests.exceptions.HTTPError):
            error_msg += f": HTTP error {exception.response.status_code}"

        raise APIError(error_msg)

    def get(self, endpoint: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        """Execute GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("GET", endpoint)

        request_headers = self._default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = self.session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            self._log_response(response)
            self._check_response(response)
            return response.json()
        except requests.RequestException as e:
            self._handle_request_exception(e, "GET", url)

    def post(self, endpoint: str, json: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        """Execute POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("POST", endpoint)

        request_headers = self._default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = self.session.post(
                url,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )
            self._log_response(response)
            self._check_response(response)
            return response.json()
        except requests.RequestException as e:
            self._handle_request_exception(e, "POST", url)

    def put(self, endpoint: str, json: Optional[dict] = None, headers: Optional[dict] = None) -> dict:
        """Execute PUT request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("PUT", endpoint)

        request_headers = self._default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = self.session.put(
                url,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )
            self._log_response(response)
            self._check_response(response)
            return response.json()
        except requests.RequestException as e:
            self._handle_request_exception(e, "PUT", url)

    def delete(self, endpoint: str, headers: Optional[dict] = None) -> dict:
        """Execute DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self._log_request("DELETE", endpoint)

        request_headers = self._default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = self.session.delete(
                url,
                headers=request_headers,
                timeout=self.timeout
            )
            self._log_response(response)
            self._check_response(response)
            return response.json()
        except requests.RequestException as e:
            self._handle_request_exception(e, "DELETE", url)


def load_config(config_path: str = "config/settings.json") -> dict:
    """Load configuration from environment variables with optional JSON file fallback.

    Environment variables take precedence over JSON config file.
    """
    # Load from environment variables first (these take precedence)
    config = {
        "base_url": os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com"),
        "timeout": int(os.getenv("TIMEOUT", "30")),
        "retries": int(os.getenv("RETRIES", "3")),
        "headers": {
            "Content-Type": os.getenv("CONTENT_TYPE", "application/json")
        }
    }

    logger.info("Configuration loaded from environment variables")

    # Check if JSON config file exists (optional fallback)
    if os.path.exists(config_path):
        try:
            import json
            with open(config_path, 'r') as f:
                json_config = json.load(f)
            # Merge JSON config as fallback for values not set in env
            for key in ["base_url", "timeout", "retries"]:
                if key in json_config and os.getenv(key.upper()) is None:
                    config[key] = json_config[key]
            logger.info(f"Additional config loaded from {config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
        except ImportError:
            pass

    return config
