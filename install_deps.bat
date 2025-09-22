@echo off
echo Installing Fitness RAG Agent Dependencies...
echo.

echo Installing faiss-cpu...
pip install faiss-cpu==1.12.0

echo Installing sentence-transformers...
pip install sentence-transformers

echo Installing FastAPI and related packages...
pip install fastapi uvicorn pydantic

echo Installing additional packages...
pip install numpy scikit-learn torch transformers pytest

echo.
echo Installation complete!
echo.
echo Testing the application...
python test_setup.py
pause
