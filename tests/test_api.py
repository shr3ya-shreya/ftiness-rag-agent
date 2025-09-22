import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from src.api_wrapper import app

class TestAPI:
    """Test cases for FastAPI endpoints"""
    
    def setup_method(self):
        """Setup test client"""
        self.client = TestClient(app)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_load_data(self):
        """Test data loading endpoint"""
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats."
            }
        ]
        response = self.client.post("/load_data", json=sample_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Successfully loaded" in data["message"]
    
    def test_query_endpoint(self):
        """Test query endpoint"""
        # First load some data
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats."
            }
        ]
        self.client.post("/load_data", json=sample_data)
        
        # Then test query
        query_data = {"query": "beginner squat", "k": 1}
        response = self.client.post("/query", json=query_data)
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert "response" in data
        assert data["query"] == "beginner squat"
    
    def test_add_document(self):
        """Test add document endpoint"""
        # First load some data
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats."
            }
        ]
        self.client.post("/load_data", json=sample_data)
        
        # Then add new document
        new_doc = {
            "exercise": "deadlift",
            "context": "personalization",
            "condition": "beginner",
            "advice": "Start with light weight."
        }
        response = self.client.post("/add_document", json=new_doc)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"]
    
    def test_stats_endpoint(self):
        """Test stats endpoint"""
        # First load some data
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats."
            }
        ]
        self.client.post("/load_data", json=sample_data)
        
        # Then test stats
        response = self.client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "stats" in data
        assert "total_documents" in data["stats"]
