import os
import sqlite3
import pytest

try:
    # Attempt import from a potential package structure (e.g., src/my_package/...)
    from src.my_financial_companion_bot.db_utils import get_db_connection, DEFAULT_DB_PATH
except ImportError:
    try:
        from db_utils import get_db_connection, DEFAULT_DB_PATH
        print("Imported connect_db from 'db_utils'.")
    except ImportError as e:
        pytest.fail(f"Failed to import connect_db function. Ensure its path is correct. Error: {e}")


@pytest.fixture(scope='function')
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


def test_connect_db_success(temp_db_path):
    """
    Test that connect_db successfully establishes a connection to a database file.
    """
    print("Running test_connect_db_success...")

    # Action: Call the connect_db function with the path provided by the fixture
    conn = get_db_connection(temp_db_path)

    # Assertion 1: Verify that the function returned a connection object (not None)
    # A successful connection should return a valid sqlite3.Connection object.
    assert conn is not None, "connect_db should return a connection object on successful connection."

    # Assertion 2: Verify the type of the returned object
    # Ensure the returned object is indeed an instance of sqlite3.Connection.
    assert isinstance(conn, sqlite3.Connection), "The returned object should be an sqlite3.Connection instance."

    # Assertion 3: Verify the connection is usable by executing a simple query
    # This checks if the connection object is functional.
    try:
        if conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                assert result[0] == 1, "A basic SELECT 1 query should return (1,) on a valid connection."
    except sqlite3.Error as error:
        # If a sqlite3.Error occurs during a basic query, the connection is likely invalid
        pytest.fail(f"Database operation failed on seemingly successful connection: {error}")