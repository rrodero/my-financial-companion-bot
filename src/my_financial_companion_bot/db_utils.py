import sqlite3
from typing import Optional

# Define the default database path as a constant for clarity
DEFAULT_DB_PATH = 'finance.db'

def connect_db(db_path: str = DEFAULT_DB_PATH) -> Optional[sqlite3.Connection]:
    """
    Establishes and returns a connection to the local SQLite database file.

    This is a core utility function for accessing the application's
    persistent data store. It handles the connection attempt and provides
    basic error reporting if the connection fails.

    :param db_path: The file path to the SQLite database. Defaults to 'finance.db'.
    :return: A sqlite3.Connection object upon successful connection, or None
        if a sqlite3.Error occurs during the connection process.

    Senior Developer Notes:
    - Returning None on failure is a simple way to indicate connection issues.
      In larger applications, logging the error and potentially re-raising
      a custom exception might be preferred to signal a critical failure.
    - SQLite connections are generally not thread-safe by default. Given
      Streamlit's potential multithreaded nature or future multiprocess
      agent interactions, consider how connections will be managed.
      Using `check_same_thread=False` can relax this, but requires careful
      handling in concurrent scenarios to avoid concurrent writes or reads
      causing issues. For this single-user, local project scale, it's often
      acceptable, but be mindful if concurrency needs increase.
    """

    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print(f"Successfully connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        print(f"ERROR: Database connection failed at {db_path}. Details: {e}")
        return None


def get_db_connection(db_path: str = DEFAULT_DB_PATH) -> Optional[sqlite3.Connection]:
    """
    Helper to get a database connection suitable for use as a context manager.
    Equivalent to connect_db for usage with 'with'.
    """
    return connect_db(db_path)