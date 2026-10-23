"""
Database initialization script.

This script:
1. Creates all database tables
2. Generates synthetic data for demonstration
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data.synthetic_data import generate_synthetic_data


if __name__ == "__main__":
    print("Revenue Intelligence Inbox - Database Initialization")
    print("="*80)
    
    try:
        generate_synthetic_data()
        print("\n✓ Database initialization complete!")
        print("\nYou can now run the application with:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        sys.exit(1)
