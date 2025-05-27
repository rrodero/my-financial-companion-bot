import pytest
import os

@pytest.fixture
def temp_db_path(tmp_path):
    """
    Pytest fixture to create and clean up a temporary database file for each test function.

    'tmp_path' is a built-in pytest fixture that provides a unique temporary
    directory path object for the test session.
    """
    # Construct a path for the temporary database file within the temporary directory
    db_file = tmp_path / "test_finance.db"
    db_path = str(db_file) # Convert Path object to string for sqlite3

    print(f"\nSetting up temporary database: {db_path}")

    yield db_path

    # Teardown: Clean up the temporary database file after the test function finishes
    print(f"Cleaning up temporary database: {db_path}")
    if os.path.exists(db_path):
        os.remove(db_path)