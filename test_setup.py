#!/usr/bin/env python3
"""Test script to verify Fitness RAG Agent setup"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from src.config import Config
        print("✅ Config module imported successfully")
        print(f"   Model: {Config.MODEL_NAME}")
        print(f"   API Port: {Config.API_PORT}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from src.rag_agent import FitnessRAGAgent
        print("✅ RAG Agent module imported successfully")
    except Exception as e:
        print(f"❌ RAG Agent import failed: {e}")
        return False
    
    try:
        from src.api_wrapper import start_cli, start_api_server
        print("✅ API Wrapper module imported successfully")
    except Exception as e:
        print(f"❌ API Wrapper import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test if sample data can be loaded"""
    print("\n🔍 Testing data loading...")
    
    try:
        import json
        data_file = Path("data/sample_fitness_data.json")
        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
            print(f"✅ Sample data loaded successfully ({len(data)} documents)")
            return True
        else:
            print("❌ Sample data file not found")
            return False
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_agent_creation():
    """Test if RAG agent can be created"""
    print("\n🔍 Testing agent creation...")
    
    try:
        from src.rag_agent import FitnessRAGAgent
        agent = FitnessRAGAgent()
        print("✅ RAG Agent created successfully")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Fitness RAG Agent Setup Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test data loading
    if not test_data_loading():
        all_passed = False
    
    # Test agent creation
    if not test_agent_creation():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! The Fitness RAG Agent is ready to use.")
        print("\nNext steps:")
        print("1. Run CLI mode: python main.py cli")
        print("2. Run API mode: python main.py api")
        print("3. Use Cursor IDE: Press F5 to debug")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("Try installing missing dependencies with: pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    main()
