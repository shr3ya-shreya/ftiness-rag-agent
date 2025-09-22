import json
import faiss
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import pickle
import os
from .config import Config

class FitnessRAGAgent:
    """Fitness RAG Agent using FAISS vector database for semantic search"""
    
    def __init__(self, model_name: str = None, index_file: str = None, 
                 metadata_file: str = None):
        """
        Initialize the RAG agent with FAISS vector database
        
        Args:
            model_name: Sentence transformer model name
            index_file: Path to FAISS index file
            metadata_file: Path to metadata pickle file
        """
        self.model_name = model_name or Config.MODEL_NAME
        self.index_file = index_file or Config.INDEX_FILE
        self.metadata_file = metadata_file or Config.METADATA_FILE
        
        print(f"Initializing agent with model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.index = None
        self.documents = []
        self.dimension = None
        
    def create_document_text(self, item: Dict[str, Any]) -> str:
        """Create searchable text from JSON item"""
        return f"Exercise: {item['exercise']} | Context: {item['context']} | Condition: {item['condition']} | Advice: {item['advice']}"
    
    def load_data(self, json_data: List[Dict[str, Any]]) -> None:
        """Load JSON data and create embeddings"""
        print(f"Loading {len(json_data)} documents...")
        
        # Store original documents
        self.documents = json_data
        
        # Create text representations for embedding
        texts = [self.create_document_text(item) for item in json_data]
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Get embedding dimension
        self.dimension = embeddings.shape[1]
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"Created FAISS index with {self.index.ntotal} documents")
        
    def save_index(self) -> None:
        """Save FAISS index and metadata to disk"""
        if self.index is not None:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
            os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
            
            faiss.write_index(self.index, self.index_file)
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.documents, f)
            print(f"Saved index to {self.index_file} and metadata to {self.metadata_file}")
        
    def load_index(self) -> bool:
        """Load FAISS index and metadata from disk"""
        try:
            if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, 'rb') as f:
                    self.documents = pickle.load(f)
                print(f"Loaded index with {self.index.ntotal} documents")
                return True
            return False
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant documents using vector similarity"""
        if self.index is None:
            raise ValueError("No index loaded. Please load data first.")
        
        # Generate query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1:  # Valid result
                result = self.documents[idx].copy()
                result['similarity_score'] = float(score)
                result['rank'] = i + 1
                results.append(result)
        
        return results
    
    def query(self, query: str, k: int = 3) -> str:
        """Query the agent and get a formatted response"""
        results = self.search(query, k)
        
        if not results:
            return "I couldn't find any relevant fitness advice for your query."
        
        response = f"Based on your query: '{query}'\n\nHere's what I found:\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"{i}. **{result['exercise'].title()} for {result['condition'].replace('_', ' ').title()}**\n"
            response += f"   Context: {result['context'].title()}\n"
            response += f"   Advice: {result['advice']}\n"
            response += f"   Relevance: {result['similarity_score']:.3f}\n\n"
        
        return response
    
    def add_document(self, document: Dict[str, Any]) -> None:
        """Add a new document to the index"""
        # Add to documents list
        self.documents.append(document)
        
        # Create embedding
        text = self.create_document_text(document)
        embedding = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(embedding)
        
        # Add to index
        self.index.add(embedding.astype('float32'))
        
        print(f"Added new document. Index now has {self.index.ntotal} documents")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.documents:
            return {"total_documents": 0}
        
        exercises = set(doc['exercise'] for doc in self.documents)
        contexts = set(doc['context'] for doc in self.documents)
        conditions = set(doc['condition'] for doc in self.documents)
        
        return {
            "total_documents": len(self.documents),
            "unique_exercises": len(exercises),
            "unique_contexts": len(contexts),
            "unique_conditions": len(conditions),
            "exercises": list(exercises),
            "contexts": list(contexts),
            "conditions": list(conditions)
        }

# Test function
if __name__ == "__main__":
    # Test with sample data
    import json
    from pathlib import Path
    
    # Load sample data
    data_file = Path(__file__).parent.parent / "data" / "sample_fitness_data.json"
    try:
        with open(data_file, 'r') as f:
            sample_data = json.load(f)
    except FileNotFoundError:
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats or bodyweight squats. Focus on consistent depth and control before adding load."
            }
        ]
    
    # Initialize and test agent
    agent = FitnessRAGAgent()
    
    if not agent.load_index():
        print("Creating new index...")
        agent.load_data(sample_data)
        agent.save_index()
    
    # Test query
    print("\n" + "="*50)
    print("Testing query...")
    response = agent.query("I'm a beginner, how should I start with squats?")
    print(response)
