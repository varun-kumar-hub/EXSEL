"""
Smart Water Distribution & Sequential Water-Gate Control System
Development Entry Point
"""
import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import run

if __name__ == "__main__":
    run()
