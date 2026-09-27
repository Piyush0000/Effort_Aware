"""
Database Seeding Script for Research Demonstrations.
"""

import sys
import os

# Add root project dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager

def main():
    print("Initializing Database Manager...")
    db = DatabaseManager()
    print("Seeding synthetic research experiment dataset (60 sample participant records)...")
    db.seed_synthetic_experiment_data(count=60)
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    main()
