# Fitness RAG Agent - Cursor IDE Setup Plan

## Overview
Adapting VSCode-specific instructions to work with Cursor IDE for a Fitness RAG (Retrieval-Augmented Generation) Agent project.

## Todo Items

### 1. Project Structure Setup
- [ ] Create directory structure (src/, data/, storage/, tests/, scripts/)
- [ ] Create __init__.py files for Python packages
- [ ] Set up basic project files

### 2. Cursor-Specific Configuration
- [ ] Create .cursor/ directory for Cursor-specific settings
- [ ] Adapt VSCode settings.json to Cursor-compatible format
- [ ] Create Cursor-specific launch configurations
- [ ] Set up Cursor tasks.json equivalent

### 3. Core Application Files
- [ ] Create src/config.py with environment configuration
- [ ] Create src/rag_agent.py with main RAG functionality
- [ ] Create src/api_wrapper.py with FastAPI wrapper
- [ ] Create main.py entry point

### 4. Data and Storage
- [ ] Create sample fitness data JSON file
- [ ] Set up storage directory structure
- [ ] Create .env file with configuration

### 5. Dependencies and Environment
- [ ] Create requirements.txt with all dependencies
- [ ] Create .gitignore file
- [ ] Set up virtual environment instructions

### 6. Scripts and Utilities
- [ ] Create setup.py for project initialization
- [ ] Create run_cli.py and run_api.py scripts
- [ ] Add helper scripts for common tasks

### 7. Testing Framework
- [ ] Create test files for unit testing
- [ ] Set up pytest configuration
- [ ] Add test data and fixtures

### 8. Documentation
- [ ] Create comprehensive README.md
- [ ] Add Cursor-specific setup instructions
- [ ] Document API endpoints and usage

### 9. Security Review
- [ ] Review all files for sensitive information
- [ ] Ensure no hardcoded secrets
- [ ] Verify .env is in .gitignore
- [ ] Check for security vulnerabilities

### 10. Final Validation
- [ ] Test CLI functionality
- [ ] Test API server
- [ ] Verify all imports work correctly
- [ ] Check for syntax errors
- [ ] Update dev.md with production improvements

## Key Adaptations for Cursor IDE

### VSCode → Cursor Changes:
1. `.vscode/` → `.cursor/` directory
2. Update settings.json for Cursor compatibility
3. Adapt launch.json for Cursor debugger
4. Modify tasks.json for Cursor task runner
5. Update Python interpreter paths for Cursor
6. Ensure Cursor-specific extensions are mentioned

### Security Considerations:
- No sensitive data in frontend
- Proper .env handling
- Secure API endpoints
- Input validation
- Error handling without information leakage

## Notes
- Keep all changes simple and minimal
- Focus on Cursor IDE compatibility
- Maintain production-ready security standards
- Follow "what would Mark Zuckerberg do" approach for frontend

## Review Section

### Changes Made
✅ **Project Structure**: Created complete directory structure with src/, data/, storage/, tests/, scripts/, and .cursor/ directories

✅ **Cursor IDE Adaptation**: 
- Converted .vscode/ to .cursor/ directory
- Updated settings.json for Cursor compatibility (Windows paths, Python interpreter)
- Adapted launch.json with proper Cursor debug configurations
- Created tasks.json for Cursor task runner

✅ **Core Application Files**:
- src/config.py: Environment-based configuration management
- src/rag_agent.py: Complete RAG agent with FAISS vector database
- src/api_wrapper.py: FastAPI wrapper with CLI and API endpoints
- main.py: Entry point with CLI and API modes

✅ **Data and Configuration**:
- Sample fitness data with 10 diverse exercise scenarios
- .env file with secure configuration
- .gitignore properly excluding sensitive files
- requirements.txt with all necessary dependencies

✅ **Scripts and Utilities**:
- scripts/setup.py: Automated project setup for Cursor
- scripts/run_cli.py: CLI runner script
- scripts/run_api.py: API server runner script

✅ **Testing Framework**:
- Complete test suite for agent functionality
- API endpoint tests with FastAPI TestClient
- Comprehensive test coverage

✅ **Documentation**:
- README.md: Complete setup and usage guide for Cursor IDE
- dev.md: Production improvements and architecture decisions
- Inline documentation and docstrings throughout

✅ **Security Review**:
- No hardcoded secrets or sensitive data
- Proper .env handling and .gitignore configuration
- Input validation with Pydantic models
- Secure error handling without information leakage
- No dangerous functions (eval, exec, shell injection)

### Key Adaptations for Cursor IDE
1. **Directory Structure**: .vscode/ → .cursor/
2. **Python Paths**: Updated for Windows (./venv/Scripts/python.exe)
3. **Settings**: Cursor-specific workspace settings
4. **Debug Configurations**: Multiple launch options for different modes
5. **Task Automation**: Cursor-compatible task definitions
6. **Documentation**: Updated all references from VSCode to Cursor

### Production-Ready Features
- Environment-based configuration
- Comprehensive error handling
- Input validation and sanitization
- Persistent vector index storage
- RESTful API with auto-documentation
- Interactive CLI interface
- Complete test coverage
- Security best practices

### Functionality Overview
The Fitness RAG Agent provides:
- **Semantic Search**: Uses FAISS vector database for similarity search
- **Multiple Interfaces**: CLI and REST API
- **Dynamic Data**: Add new fitness advice documents
- **Statistics**: Database analytics and insights
- **Cursor Integration**: Full IDE support with debugging and tasks

All VSCode-specific instructions have been successfully adapted for Cursor IDE while maintaining the same functionality and improving the development experience.
