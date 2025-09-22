#!/usr/bin/env python3
"""Test all imports for the Fitness RAG Agent"""

print("🔍 Testing Fitness RAG Agent Imports...")
print("=" * 50)

# Test 1: Basic Python modules
print("1. Testing basic Python modules...")
try:
    import json
    import os
    import sys
    from pathlib import Path
    print("   ✅ Basic modules imported successfully")
except Exception as e:
    print(f"   ❌ Basic modules failed: {e}")

# Test 2: Configuration
print("2. Testing configuration...")
try:
    from src.config import Config
    print(f"   ✅ Config imported - Model: {Config.MODEL_NAME}")
except Exception as e:
    print(f"   ❌ Config failed: {e}")

# Test 3: FAISS
print("3. Testing FAISS...")
try:
    import faiss
    print("   ✅ FAISS imported successfully")
except Exception as e:
    print(f"   ❌ FAISS failed: {e}")

# Test 4: Sentence Transformers
print("4. Testing Sentence Transformers...")
try:
    from sentence_transformers import SentenceTransformer
    print("   ✅ Sentence Transformers imported successfully")
except Exception as e:
    print(f"   ❌ Sentence Transformers failed: {e}")

# Test 5: FastAPI
print("5. Testing FastAPI...")
try:
    from fastapi import FastAPI
    import uvicorn
    print("   ✅ FastAPI imported successfully")
except Exception as e:
    print(f"   ❌ FastAPI failed: {e}")

# Test 6: Pydantic
print("6. Testing Pydantic...")
try:
    from pydantic import BaseModel
    print("   ✅ Pydantic imported successfully")
except Exception as e:
    print(f"   ❌ Pydantic failed: {e}")

# Test 7: RAG Agent
print("7. Testing RAG Agent...")
try:
    from src.rag_agent import FitnessRAGAgent
    print("   ✅ RAG Agent imported successfully")
except Exception as e:
    print(f"   ❌ RAG Agent failed: {e}")

# Test 8: API Wrapper
print("8. Testing API Wrapper...")
try:
    from src.api_wrapper import start_cli, start_api_server
    print("   ✅ API Wrapper imported successfully")
except Exception as e:
    print(f"   ❌ API Wrapper failed: {e}")

print("\n" + "=" * 50)
print("🎉 Import test completed!")
print("\nIf all tests passed, you can now run:")
print("  python main.py cli    # For CLI mode")
print("  python main.py api    # For API mode")
