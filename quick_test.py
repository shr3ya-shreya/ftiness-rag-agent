#!/usr/bin/env python3
"""Quick test to verify core functionality"""

print("🚀 Quick Fitness RAG Agent Test")
print("=" * 40)

# Test 1: Basic imports
print("🔍 Testing basic imports...")
try:
    from src.config import Config
    print("✅ Config imported successfully")
    print(f"   Model: {Config.MODEL_NAME}")
    print(f"   API Port: {Config.API_PORT}")
except Exception as e:
    print(f"❌ Config import failed: {e}")

# Test 2: FAISS import
print("\n🔍 Testing FAISS import...")
try:
    import faiss
    print("✅ FAISS imported successfully")
except Exception as e:
    print(f"❌ FAISS import failed: {e}")

# Test 3: Sentence Transformers
print("\n🔍 Testing Sentence Transformers...")
try:
    from sentence_transformers import SentenceTransformer
    print("✅ Sentence Transformers imported successfully")
except Exception as e:
    print(f"❌ Sentence Transformers import failed: {e}")

# Test 4: FastAPI
print("\n🔍 Testing FastAPI...")
try:
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
except Exception as e:
    print(f"❌ FastAPI import failed: {e}")

print("\n" + "=" * 40)
print("🎉 Quick test completed!")
