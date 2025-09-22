#!/usr/bin/env python3
"""Simple demonstration of the Fitness RAG Agent functionality"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def load_sample_data():
    """Load sample fitness data"""
    try:
        with open("data/sample_fitness_data.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def simple_search(query, data, k=3):
    """Simple keyword-based search (fallback when vector search isn't available)"""
    query_lower = query.lower()
    query_words = query_lower.split()
    results = []
    
    for item in data:
        score = 0
        text_to_search = f"{item['exercise']} {item['condition']} {item['advice']} {item['context']}".lower()
        
        # Check for exact phrase matches
        if query_lower in text_to_search:
            score += 5
        
        # Check for individual word matches
        for word in query_words:
            if word in item['exercise'].lower():
                score += 3
            if word in item['condition'].lower():
                score += 2
            if word in item['advice'].lower():
                score += 1
            if word in item['context'].lower():
                score += 1
        
        # Check for partial matches
        for word in query_words:
            if any(word in field.lower() for field in [item['exercise'], item['condition'], item['advice'], item['context']]):
                score += 0.5
            
        if score > 0:
            item_copy = item.copy()
            item_copy['similarity_score'] = min(score / 10.0, 1.0)  # Normalize to 0-1
            results.append(item_copy)
    
    # Sort by score and return top k
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return results[:k]

def format_response(query, results):
    """Format the response nicely"""
    if not results:
        return f"I couldn't find any relevant fitness advice for '{query}'."
    
    response = f"Based on your query: '{query}'\n\nHere's what I found:\n\n"
    
    for i, result in enumerate(results, 1):
        response += f"{i}. **{result['exercise'].title()} for {result['condition'].replace('_', ' ').title()}**\n"
        response += f"   Context: {result['context'].title()}\n"
        response += f"   Advice: {result['advice']}\n"
        response += f"   Relevance: {result['similarity_score']:.3f}\n\n"
    
    return response

def main():
    """Main demonstration function"""
    print("🚀 Fitness RAG Agent - Simple Demo")
    print("=" * 50)
    print("Note: This is a simplified version using keyword search.")
    print("The full version uses AI-powered vector similarity search.")
    print("=" * 50)
    
    # Load sample data
    print("📚 Loading fitness data...")
    data = load_sample_data()
    if not data:
        print("❌ No data found. Please check data/sample_fitness_data.json")
        return
    
    print(f"✅ Loaded {len(data)} fitness advice documents")
    
    # Demo queries
    demo_queries = [
        "beginner squat advice",
        "knee pain exercises", 
        "shoulder pain prevention",
        "older adult fitness"
    ]
    
    print("\n🎯 Running demo queries...")
    print("=" * 50)
    
    for query in demo_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 30)
        
        results = simple_search(query, data, k=2)
        response = format_response(query, results)
        print(response)
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nTo use the full AI-powered version:")
    print("1. Install all dependencies: pip install -r requirements.txt")
    print("2. Run: python main.py cli")
    print("3. Or use Cursor IDE: Press F5 and select 'Run CLI'")

if __name__ == "__main__":
    main()
