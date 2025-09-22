import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Using default values.")

class Config:
    """Configuration settings for the Fitness RAG Agent"""
    
    # Model settings
    MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
    
    # File paths
    INDEX_FILE = os.getenv("INDEX_FILE", "storage/fitness_index.faiss")
    METADATA_FILE = os.getenv("METADATA_FILE", "storage/fitness_metadata.pkl")
    DATA_FILE = os.getenv("DATA_FILE", "data/sample_fitness_data.json")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Debug
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Ensure storage directory exists
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
