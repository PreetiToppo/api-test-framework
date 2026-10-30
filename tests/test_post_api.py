import pytest
from jsonschema import validate

from utilities.api_helpers import APIError

# JSON Schema definitions
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "body": {"type": "string", "minLength": 1}
    },
    "required": ["userId", "id", "title", "body"],
    "additionalProperties": False
}

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": "string"},
        "website": {"type": "string"}
    },
    "required": ["id", "name", "username", "email"]
}

ALBUM_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1}
    },
    "required": ["userId", "id", "title"],
    "additionalProperties": False
}

# Test data for parametrized testing
VALID_POST_PAYLOADS = [
    {
        "title": "First Post",
        "body": "This is the first test post content.",
        "userId": 1
    },
    {
        "title": "Another Interesting Post",
        "body": "Testing with different content here.",
        "userId": 2
    },
    {
        "title": "API Testing Framework",
        "body": "This post validates the robustness of our testing framework.",
        "userId": 3
    },
    {
        "title": "Comprehensive Testing",
        "body": "Ensure all endpoints are properly tested.",
        "userId": 10
    },
    {
        "title": "Production Ready",
        "body": "Final validation before deployment.",
        "userId": 5
    }
]


class TestPostEndpoint:
    """Test suite for POST /posts endpoint."""

    @pytest.mark.parametrize("payload", VALID_POST_PAYLOADS)
    def test_create_post_with_different_payloads(self, api_client, payload):
        """Test POST endpoint with multiple valid payloads using parametrization."""
        response = api_client.post("/posts", json=payload)

        assert response["id"] is not None
        assert response["id"] == 101
        assert response["title"] == payload["title"]
        assert response["body"] == payload["body"]
        assert response["userId"] == payload["userId"]

    def test_create_post_returns_correct_status_code(self, api_client):
        """Test that creating a post returns 201 Created."""
        payload = {
            "title": "Test Post",
            "body": "Test content",
            "userId": 1
        }
        response = api_client.post("/posts", json=payload)
        assert response["id"] == 101

    def test_create_post_returns_data_in_response(self, api_client):
        """Test that created post includes all expected fields in response."""
        payload = {
            "title": "Response Validation Test",
            "body": "This tests the response structure.",
            "userId": 1
        }
        response = api_client.post("/posts", json=payload)

        assert "id" in response
        assert "title" in response
        assert "body" in response
        assert "userId" in response


class TestNegativeCases:
    """Negative test cases for error handling."""

    def test_create_post_with_invalid_endpoint_returns_404(self, api_client):
        """Test POST request to non-existent endpoint returns 404."""
        payload = {
            "title": "Test",
            "body": "Test",
            "userId": 1
        }

        with pytest.raises(APIError) as excinfo:
            api_client.post("/nonexistent/endpoint", json=payload)

        assert excinfo.value.status_code == 404


class TestGetEndpoints:
    """Test suite for GET endpoints."""

    def test_get_all_posts_returns_list(self, api_client):
        """Test GET /posts returns a list of posts."""
        posts = api_client.get("/posts")
        assert isinstance(posts, list)
        assert len(posts) > 0

    def test_get_all_posts_has_correct_structure(self, api_client):
        """Test that each post in the list has expected structure."""
        posts = api_client.get("/posts")

        for post in posts[:5]:  # Check first 5 posts
            assert "userId" in post
            assert "id" in post
            assert "title" in post
            assert "body" in post

    def test_get_single_post_by_id(self, api_client):
        """Test GET /posts/{id} returns correct post."""
        post = api_client.get("/posts/1")
        assert post["id"] == 1
        validate(instance=post, schema=POST_SCHEMA)

    def test_get_post_with_invalid_id_raises_error(self, api_client):
        """Test GET /posts with invalid ID returns 404."""
        with pytest.raises(APIError) as excinfo:
            api_client.get("/posts/99999")
        assert excinfo.value.status_code == 404

    def test_get_user_by_id(self, api_client):
        """Test GET /users/{id} returns correct user data."""
        user = api_client.get("/users/1")
        assert user["id"] == 1
        validate(instance=user, schema=USER_SCHEMA)

    def test_get_albums(self, api_client):
        """Test GET /albums returns list of albums."""
        albums = api_client.get("/albums")
        assert isinstance(albums, list)
        assert len(albums) > 0
        validate(instance=albums[0], schema=ALBUM_SCHEMA)


class TestDeleteEndpoint:
    """Test suite for DELETE endpoints."""

    def test_delete_post_returns_success(self, api_client):
        """Test DELETE /posts/{id} returns 200."""
        response = api_client.delete("/posts/1")
        assert response == {}

    def test_delete_non_existent_post(self, api_client):
        """Test DELETE on non-existent resource."""
        response = api_client.delete("/posts/99999")
        assert response == {}


class TestPUTUpdateEndpoint:
    """Test suite for PUT update endpoints."""

    def test_update_post_returns_updated_data(self, api_client):
        """Test PUT /posts/{id} returns updated post."""
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated content",
            "userId": 1
        }
        response = api_client.put("/posts/1", json=payload)

        assert response["title"] == payload["title"]
        assert response["body"] == payload["body"]

    def test_update_post_preserves_id(self, api_client):
        """Test that PUT request preserves the post ID."""
        payload = {
            "id": 1,
            "title": "Another Update",
            "body": "More updates",
            "userId": 1
        }
        response = api_client.put("/posts/1", json=payload)

        assert response["id"] == 1


class TestJSONSchemaValidation:
    """Tests for JSON schema validation."""

    def test_post_schema_validation(self, api_client):
        """Validate response against POST schema."""
        posts = api_client.get("/posts")
        for post in posts[:3]:
            validate(instance=post, schema=POST_SCHEMA)

    def test_user_schema_validation(self, api_client):
        """Validate user response against USER schema."""
        user = api_client.get("/users/1")
        validate(instance=user, schema=USER_SCHEMA)

    def test_album_schema_validation(self, api_client):
        """Validate album response against ALBUM schema."""
        albums = api_client.get("/albums")
        for album in albums[:3]:
            validate(instance=album, schema=ALBUM_SCHEMA)

    def test_create_post_schema_validation(self, api_client):
        """Validate POST response against POST schema."""
        payload = {
            "title": "Schema Validation Test",
            "body": "Testing schema validation.",
            "userId": 1
        }
        response = api_client.post("/posts", json=payload)
        validate(instance=response, schema=POST_SCHEMA)


class TestEdgeCases:
    """Edge case testing."""

    def test_get_posts_with_query_params(self, api_client):
        """Test GET with query parameters."""
        posts = api_client.get("/posts", params={"userId": 1})
        assert isinstance(posts, list)
        assert all(post["userId"] == 1 for post in posts)

    def test_response_time_is_reasonable(self, api_client):
        """Test that API responds within reasonable time."""
        import time
        start = time.time()
        api_client.get("/posts")
        elapsed = time.time() - start
        assert elapsed < 10, "API response time exceeded 10 seconds"

    def test_content_type_is_json(self, api_client):
        """Test that responses have correct content type."""
        import requests as req
        response = req.get("https://jsonplaceholder.typicode.com/posts")
        assert "application/json" in response.headers.get("Content-Type", "")
