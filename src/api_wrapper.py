from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import uvicorn
import sys
from pathlib import Path

# Import our modules
from .rag_agent import FitnessRAGAgent
from .config import Config

# Pydantic models for API
class QueryRequest(BaseModel):
    query: str
    k: int = 3

class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    response: str

class AddDocumentRequest(BaseModel):
    exercise: str
    context: str
    condition: str
    advice: str

class StatsResponse(BaseModel):
    stats: Dict[str, Any]

# Initialize FastAPI app
app = FastAPI(title="Fitness RAG Agent API", version="1.0.0")

# Global agent instance
agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent on startup"""
    global agent
    agent = FitnessRAGAgent()
    
    # Try to load existing index
    if not agent.load_index():
        print("No existing index found. Loading sample data...")
        try:
            with open(Config.DATA_FILE, 'r') as f:
                sample_data = json.load(f)
            agent.load_data(sample_data)
            agent.save_index()
        except FileNotFoundError:
            print(f"Warning: {Config.DATA_FILE} not found.")

@app.post("/load_data", response_model=Dict[str, str])
async def load_data(data: List[Dict[str, Any]]):
    """Load fitness data and create vector index"""
    try:
        agent.load_data(data)
        agent.save_index()
        return {"message": f"Successfully loaded {len(data)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """Query the fitness agent"""
    try:
        if agent.index is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please load data first.")
        
        results = agent.search(request.query, request.k)
        response = agent.query(request.query, request.k)
        
        return QueryResponse(
            query=request.query,
            results=results,
            response=response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_document", response_model=Dict[str, str])
async def add_document(request: AddDocumentRequest):
    """Add a new document to the index"""
    try:
        if agent.index is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please load data first.")
        
        document = {
            "exercise": request.exercise,
            "context": request.context,
            "condition": request.condition,
            "advice": request.advice
        }
        
        agent.add_document(document)
        agent.save_index()
        
        return {"message": "Document added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics"""
    try:
        if agent.index is None:
            raise HTTPException(status_code=400, detail="No data loaded. Please load data first.")
        
        stats = agent.get_stats()
        return StatsResponse(stats=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent_loaded": agent is not None and agent.index is not None}

def start_api_server(host: str = None, port: int = None):
    """Start the FastAPI server"""
    host = host or Config.API_HOST
    port = port or Config.API_PORT
    
    print(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

def start_cli():
    """Start the CLI interface"""
    global agent
    
    if agent is None:
        agent = FitnessRAGAgent()
        
        # Try to load existing index
        if not agent.load_index():
            print("No existing index found. Loading sample data...")
            try:
                with open(Config.DATA_FILE, 'r') as f:
                    sample_data = json.load(f)
                agent.load_data(sample_data)
                agent.save_index()
            except FileNotFoundError:
                print(f"Warning: {Config.DATA_FILE} not found.")
                return
    
    print("\n" + "="*50)
    print("Fitness RAG Agent CLI")
    print("="*50)
    print("Commands:")
    print("  query <your question>  - Ask a fitness question")
    print("  stats                  - Show database statistics")
    print("  quit                   - Exit the program")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'stats':
                stats = agent.get_stats()
                print(f"\nDatabase Statistics:")
                print(f"  Total documents: {stats['total_documents']}")
                print(f"  Unique exercises: {stats['unique_exercises']}")
                print(f"  Unique contexts: {stats['unique_contexts']}")
                print(f"  Unique conditions: {stats['unique_conditions']}")
            elif user_input.startswith('query '):
                query = user_input[6:].strip()
                if query:
                    response = agent.query(query)
                    print(f"\n{response}")
                else:
                    print("Please provide a query after 'query'")
            else:
                print("Unknown command. Try 'query <question>', 'stats', or 'quit'")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_cli()
