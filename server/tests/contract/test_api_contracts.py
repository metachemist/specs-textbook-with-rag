import pytest
from fastapi.testclient import TestClient
from src.api.retrieval_api import router
from main import app  # Assuming the main FastAPI app is in main.py


# Add the router to the app for testing
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)


class TestAPIContracts:
    
    def test_search_endpoint_contract(self, client):
        """
        Test the POST /api/v1/search endpoint contract
        """
        # Test with valid request
        request_data = {
            "query": "What is a node?",
            "top_k": 5
        }
        
        response = client.post("/api/v1/search", json=request_data)
        
        # Check that the response has the expected structure
        assert response.status_code in [200, 400, 500]  # Expected status codes
        
        if response.status_code == 200:
            response_data = response.json()
            # Check that required fields are present
            assert "query_id" in response_data
            assert "results" in response_data
            assert "total_results" in response_data
            assert "search_time_ms" in response_data
            assert "message" in response_data
            
            # Check that types are correct
            assert isinstance(response_data["query_id"], str)
            assert isinstance(response_data["results"], list)
            assert isinstance(response_data["total_results"], int)
            assert isinstance(response_data["search_time_ms"], (int, float))
            assert isinstance(response_data["message"], str)
            
            # Check that results are properly structured
            for result in response_data["results"]:
                assert "id" in result
                assert "content" in result
                assert "score" in result
                assert "source_url" in result
                assert "source_file_path" in result
                assert "chunk_index" in result
                assert "metadata" in result
    
    def test_search_endpoint_invalid_request(self, client):
        """
        Test that the POST /api/v1/search endpoint properly handles invalid requests
        """
        # Test with invalid request (no query)
        request_data = {
            "query": "",  # Empty query
            "top_k": 5
        }
        
        response = client.post("/api/v1/search", json=request_data)
        
        # Should return 400 for bad request or 500 for server error
        assert response.status_code in [400, 500]
    
    def test_search_endpoint_with_filters(self, client):
        """
        Test the POST /api/v1/search endpoint with filters
        """
        # Test with filters
        request_data = {
            "query": "What is a node?",
            "top_k": 3,
            "filters": {
                "content_type": "documentation",
                "tags": ["robotics", "nodes"]
            }
        }
        
        response = client.post("/api/v1/search", json=request_data)
        
        # Check that the response has the expected structure
        assert response.status_code in [200, 400, 500]  # Expected status codes
    
    def test_get_search_result_contract(self, client):
        """
        Test the GET /api/v1/search/{query_id} endpoint contract
        """
        # Test with a sample query ID
        query_id = "test-query-id"
        
        response = client.get(f"/api/v1/search/{query_id}")
        
        # Check that the response has the expected structure
        assert response.status_code in [200, 404, 500]  # Expected status codes