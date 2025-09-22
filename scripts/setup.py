#!/usr/bin/env python3
"""Setup script for Fitness RAG Agent - Cursor IDE Version"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command):
    """Run shell command and return success status"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ["src", "data", "storage", "tests", "scripts", ".cursor"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✓ Created directory structure")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    if run_command("pip install -r requirements.txt"):
        print("✓ Dependencies installed")
    else:
        print("✗ Failed to install dependencies")
        return False
    return True

def create_sample_data():
    """Create sample data file if it doesn't exist"""
    data_file = Path("data/sample_fitness_data.json")
    if not data_file.exists():
        sample_data = [
            {
                "exercise": "squat",
                "context": "personalization",
                "condition": "beginner",
                "advice": "Start with box squats or bodyweight squats. Focus on consistent depth and control before adding load."
            }
        ]
        with open(data_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        print("✓ Created sample data file")

def setup_cursor():
    """Create Cursor IDE configuration files"""
    settings = {
        "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
        "python.terminal.activateEnvironment": True,
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "storage/": True
        }
    }
    
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run CLI",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "args": ["cli"],
                "console": "integratedTerminal"
            },
            {
                "name": "Run API",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "args": ["api"],
                "console": "integratedTerminal"
            }
        ]
    }
    
    os.makedirs(".cursor", exist_ok=True)
    
    with open(".cursor/settings.json", 'w') as f:
        json.dump(settings, f, indent=2)
       
    with open(".cursor/launch.json", 'w') as f:
        json.dump(launch, f, indent=2)
       
    print("✓ Created Cursor IDE configuration")

def main():
    print("Setting up Fitness RAG Agent for Cursor IDE...")
    
    create_directories()
    create_sample_data()
    setup_cursor()
    
    if install_dependencies():
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. python main.py cli    # Run CLI mode")
        print("2. python main.py api    # Run API server")
        print("3. Press F5 in Cursor    # Debug mode")
        print("4. Use Ctrl+Shift+P → 'Tasks: Run Task' for available tasks")
    else:
        print("\n❌ Setup failed. Please check error messages above.")

if __name__ == "__main__":
    main()
