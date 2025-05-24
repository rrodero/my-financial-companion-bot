import sqlite3

def connect_db(db_path: str = 'finance.db') -> sqlite3.Connection | None:
    """
    Establishes a connection to the local SQLite database file.

    :param db_path: The path to the SQLite database file (default is 'finance.db').
    :return: A sqlite3.Connection object representing the database connection.
    """

    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Database connectio error: {e}")
        return None