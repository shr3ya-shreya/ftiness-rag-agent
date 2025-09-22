import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.rag_agent import FitnessRAGAgent

class TestFitnessRAGAgent:
    """Test cases for FitnessRAGAgent"""
    
    def setup_method(self):
        """Setup test data"""
        self.sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats or bodyweight squats."
            },
            {
                "exercise": "push_up",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with wall push-ups or incline push-ups."
            }
        ]
        self.agent = FitnessRAGAgent()
    
    def test_create_document_text(self):
        """Test document text creation"""
        item = self.sample_data[0]
        text = self.agent.create_document_text(item)
        assert "squat" in text
        assert "personalization" in text
        assert "beginner" in text
        assert "box squats" in text
    
    def test_load_data(self):
        """Test data loading and indexing"""
        self.agent.load_data(self.sample_data)
        assert self.agent.index is not None
        assert len(self.agent.documents) == 2
        assert self.agent.index.ntotal == 2
    
    def test_search(self):
        """Test search functionality"""
        self.agent.load_data(self.sample_data)
        results = self.agent.search("beginner squat", k=1)
        assert len(results) == 1
        assert results[0]['exercise'] == 'squat'
        assert 'similarity_score' in results[0]
    
    def test_query(self):
        """Test query functionality"""
        self.agent.load_data(self.sample_data)
        response = self.agent.query("beginner squat")
        assert "squat" in response.lower()
        assert "beginner" in response.lower()
    
    def test_get_stats(self):
        """Test statistics generation"""
        self.agent.load_data(self.sample_data)
        stats = self.agent.get_stats()
        assert stats['total_documents'] == 2
        assert stats['unique_exercises'] == 2
        assert 'squat' in stats['exercises']
        assert 'push_up' in stats['exercises']
    
    def test_add_document(self):
        """Test adding new document"""
        self.agent.load_data(self.sample_data)
        new_doc = {
            "exercise": "deadlift",
            "context": "personalization",
            "condition": "beginner",
            "advice": "Start with light weight and focus on form."
        }
        self.agent.add_document(new_doc)
        assert len(self.agent.documents) == 3
        assert self.agent.index.ntotal == 3
