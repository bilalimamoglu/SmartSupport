import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.database_manager import DatabaseManager


def initialize_db_from_file(file_path):
    """
    Initialize the database with leads from the given JSON file.

    :param file_path: Path to the JSON file containing lead data.
    """
    db_manager = DatabaseManager()
    db_manager.initialize_db_from_file(file_path)
    print("Database initialized with leads from", file_path)


if __name__ == "__main__":
    # Define the path to the example leads JSON file
    file_path = os.path.join(os.path.dirname(__file__), '../../data/leads/example_leads.json')

    # Initialize the database
    initialize_db_from_file(file_path)
