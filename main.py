import sys
import argparse
import json
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.rag_agent import FitnessRAGAgent
from src.api_wrapper import start_api_server, start_cli
from src.config import Config

def load_sample_data():
    """Load sample data from JSON file"""
    try:
        with open(Config.DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {Config.DATA_FILE} not found. Using minimal sample data.")
        return [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats or bodyweight squats. Focus on consistent depth and control before adding load."
            }
        ]

def setup_agent():
    """Initialize and setup the RAG agent"""
    agent = FitnessRAGAgent(
        model_name=Config.MODEL_NAME,
        index_file=Config.INDEX_FILE,
        metadata_file=Config.METADATA_FILE
    )
    
    # Try to load existing index
    if not agent.load_index():
        print("No existing index found. Creating new one with sample data...")
        sample_data = load_sample_data()
        agent.load_data(sample_data)
        agent.save_index()
        print(f"Created index with {len(sample_data)} documents")
    
    return agent

def main():
    parser = argparse.ArgumentParser(description="Fitness RAG Agent")
    parser.add_argument("mode", choices=["cli", "api"], default="cli", nargs="?",
                       help="Run mode: cli (interactive) or api (server)")
    parser.add_argument("--host", default=Config.API_HOST, help="API host")
    parser.add_argument("--port", type=int, default=Config.API_PORT, help="API port")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        print(f"Starting API server on {args.host}:{args.port}")
        start_api_server(host=args.host, port=args.port)
    else:
        print("Starting CLI mode...")
        start_cli()

if __name__ == "__main__":
    main()
