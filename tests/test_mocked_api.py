"""Test suite with mocked API responses using responses library.

These tests validate that the APIClient handles various error scenarios
gracefully by raising appropriate custom exceptions.
"""
import pytest
import requests
import responses
from responses import matchers

from utilities.api_helpers import APIClient, APIError


class TestMockedErrorHandling:
    """Tests for API error handling with mocked responses."""

    @responses.activate
    def test_handle_500_internal_server_error(self):
        """Test that APIClient raises APIError for 500 response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.GET,
            f"{base_url}/posts",
            json={"error": "Internal Server Error"},
            status=500
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/posts")

        assert excinfo.value.status_code == 500
        assert "500" in str(excinfo.value)
        assert "Internal Server Error" in str(excinfo.value)

    @responses.activate
    def test_handle_404_not_found(self):
        """Test that APIClient raises APIError for 404 response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.GET,
            f"{base_url}/posts/99999",
            json={"error": "Post not found"},
            status=404
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/posts/99999")

        assert excinfo.value.status_code == 404
        assert "404" in str(excinfo.value)
        assert "Post not found" in str(excinfo.value)

    @responses.activate
    def test_handle_404_not_found_with_text_response(self):
        """Test 404 handling when response is plain text."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.GET,
            f"{base_url}/invalid/endpoint",
            body="Not Found",
            status=404
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/invalid/endpoint")

        assert excinfo.value.status_code == 404

    @responses.activate
    def test_handle_401_unauthorized(self):
        """Test that APIClient raises APIError for 401 response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.GET,
            f"{base_url}/protected",
            json={"error": "Unauthorized"},
            status=401
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/protected")

        assert excinfo.value.status_code == 401
        assert "401" in str(excinfo.value)

    @responses.activate
    def test_handle_403_forbidden(self):
        """Test that APIClient raises APIError for 403 response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.GET,
            f"{base_url}/admin",
            json={"error": "Forbidden"},
            status=403
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/admin")

        assert excinfo.value.status_code == 403
        assert "403" in str(excinfo.value)


class TestMockedTimeoutHandling:
    """Tests for timeout handling."""

    @responses.activate
    def test_handle_timeout_on_get_request(self):
        """Test that APIClient handles timeout gracefully."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=2)

        # Use a custom exception that will be raised by responses
        responses.add(
            responses.GET,
            f"{base_url}/slow-endpoint",
            body=requests.exceptions.Timeout("Request timed out")
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/slow-endpoint")

        assert "timeout" in str(excinfo.value).lower() or "timed out" in str(excinfo.value).lower()

    @responses.activate
    def test_handle_timeout_on_post_request(self):
        """Test that APIClient handles timeout gracefully on POST."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=2)

        responses.add(
            responses.POST,
            f"{base_url}/posts",
            body=requests.exceptions.Timeout("Request timed out")
        )

        with pytest.raises(APIError) as excinfo:
            client.post("/posts", json={"title": "Test", "body": "Body", "userId": 1})

        assert "timeout" in str(excinfo.value).lower() or "timed out" in str(excinfo.value).lower()


class TestMockedConnectionErrors:
    """Tests for connection error handling."""

    @responses.activate
    def test_handle_connection_error(self):
        """Test that APIClient handles connection errors gracefully."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        # Use a custom exception that will be raised by responses
        responses.add(
            responses.GET,
            f"{base_url}/posts",
            body=requests.exceptions.ConnectionError("Connection refused")
        )

        with pytest.raises(APIError) as excinfo:
            client.get("/posts")

        assert "connection" in str(excinfo.value).lower() or "refused" in str(excinfo.value).lower()


class TestMockedSuccessScenarios:
    """Tests for successful API responses with mocking."""

    @responses.activate
    def test_mocked_get_success(self):
        """Test successful GET request with mocked response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        mock_response = [
            {"id": 1, "title": "Mocked Post 1", "body": "Content 1", "userId": 1},
            {"id": 2, "title": "Mocked Post 2", "body": "Content 2", "userId": 1}
        ]

        responses.add(
            responses.GET,
            f"{base_url}/posts",
            json=mock_response,
            status=200
        )

        result = client.get("/posts")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "Mocked Post 1"

    @responses.activate
    def test_mocked_post_success(self):
        """Test successful POST request with mocked response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        mock_response = {
            "id": 101,
            "title": "Created Post",
            "body": "Test content",
            "userId": 1
        }

        responses.add(
            responses.POST,
            f"{base_url}/posts",
            json=mock_response,
            status=201
        )

        payload = {
            "title": "Created Post",
            "body": "Test content",
            "userId": 1
        }

        result = client.post("/posts", json=payload)
        assert result["id"] == 101
        assert result["title"] == "Created Post"

    @responses.activate
    def test_mocked_put_success(self):
        """Test successful PUT request with mocked response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        mock_response = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body",
            "userId": 1
        }

        responses.add(
            responses.PUT,
            f"{base_url}/posts/1",
            json=mock_response,
            status=200
        )

        result = client.put("/posts/1", json={"title": "Updated Title", "body": "Updated body", "userId": 1})
        assert result["title"] == "Updated Title"

    @responses.activate
    def test_mocked_delete_success(self):
        """Test successful DELETE request with mocked response."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        responses.add(
            responses.DELETE,
            f"{base_url}/posts/1",
            json={},
            status=200
        )

        result = client.delete("/posts/1")
        assert result == {}


class TestMockedQueryParameters:
    """Tests for query parameter handling with mocking."""

    @responses.activate
    def test_get_with_query_parameters(self):
        """Test GET request with query parameters."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        mock_response = [
            {"id": 1, "title": "Post 1", "body": "Content", "userId": 1}
        ]

        responses.add(
            responses.GET,
            f"{base_url}/posts",
            json=mock_response,
            status=200,
            match=[matchers.query_param_matcher({"userId": "1"})]
        )

        result = client.get("/posts", params={"userId": 1})
        assert isinstance(result, list)
        assert len(result) == 1


class TestMockedMultipleEndpoints:
    """Tests for multiple endpoint mocking in single test."""

    @responses.activate
    def test_mock_multiple_endpoints(self):
        """Test mocking multiple API endpoints."""
        base_url = "https://api.example.com"
        client = APIClient(base_url=base_url, timeout=10)

        # Mock posts endpoint
        responses.add(
            responses.GET,
            f"{base_url}/posts",
            json=[{"id": 1, "title": "Post", "body": "Content", "userId": 1}],
            status=200
        )

        # Mock users endpoint
        responses.add(
            responses.GET,
            f"{base_url}/users/1",
            json={"id": 1, "name": "Test User", "username": "test", "email": "test@example.com"},
            status=200
        )

        # Mock albums endpoint
        responses.add(
            responses.GET,
            f"{base_url}/albums",
            json=[{"id": 1, "title": "Album 1", "userId": 1}],
            status=200
        )

        posts = client.get("/posts")
        users = client.get("/users/1")
        albums = client.get("/albums")

        assert len(posts) == 1
        assert users["name"] == "Test User"
        assert len(albums) == 1
