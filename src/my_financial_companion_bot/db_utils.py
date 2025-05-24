import sqlite3
from typing import Optional

# Define the default database path as a constant for clarity
DEFAULT_DB_PATH = '../data/finance.db'

def connect_db(db_path: str = DEFAULT_DB_PATH) -> Optional[sqlite3.Connection]:
    """
    Establishes and returns a connection to the local SQLite database file.

    This is a core utility function for accessing the application's
    persistent data store. It handles the connection attempt and provides
    basic error reporting if the connection fails.

    :param db_path: The file path to the SQLite database. Defaults to 'finance.db'.
    :return: A sqlite3.Connection object upon successful connection, or None
        if a sqlite3.Error occurs during the connection process.
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


def create_tables(db_path: str = DEFAULT_DB_PATH):
    """
    Creates necessary tables in the SQLite database if they don't exist.

    Args:
        db_path: The path to the SQLite database file.
                 Defaults to DEFAULT_DB_PATH.
    """
    conn = get_db_connection(db_path)
    try:
        if conn:
            with conn:
                cursor = conn.cursor()

                sql_create_transactions_table = """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('Income' or 'Expense')), 
                    original_Source TEXT,
                    category_id TEXT,
                    tags TEXT,
                    note TEXT,
                    installment_series_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                    FOREIGN KEY (installment_series_id) REFERENCES installment_series (series_id)
                );
                """

                sql_create_categories_table = """
                    CREATE TABLE IF NOT EXISTS categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_name TEXT NOT NULL UNIQUE,
                        parent_category_id INTEGER,
                        FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
                    );
                """

                # Using CHECK(user_profile_id = 1) to enforce a single row
                sql_create_user_profile_table = """
                CREATE TABLE IF NOT EXISTS user_profile (
                    user_profile_id INTEGER PRIMARY KEY CHECK(user_profile_id = 1), 
                    age INTEGER,
                    occupation TEXT,
                    income REAL,
                    household_size INTEGER,
                    assets TEXT,
                    liabilities TEXT,
                    specific_financial_goals TEXT,
                    risk_tolerance TEXT
                );
                """

                sql_create_installment_series_table = """
                    CREATE TABLE IF NOT EXISTS installment_series (
                        series_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        original_amount REAL NOT NULL,
                        total_installments INTEGER NOT NULL,
                        installment_amount REAL,
                        interest_rate REAL,
                        start_date TEXT NOT NULL,
                        end_date TEXT,
                        status TEXT NOT NULL CHECK(status IN ('Active' or 'Completed' or 'Cancelled')) DEFAULT 'Active',
                        current_installment_number INTEGER DEFAULT 0,
                        notes TEXT
                    );
                """

            # Execute table creation statements
            cursor.execute(sql_create_transactions_table)
            cursor.execute(sql_create_categories_table)
            cursor.execute(sql_create_user_profile_table)
            cursor.execute(sql_create_installment_series_table)

            # Add the default 'user_profile' row if it doesn't exist
            # This handles the CHECK (id = 1) constraint for the single row
            cursor.execute("INSERT OR IGNORE INTO user_profile (user_profile_id) VALUES (1);")

            # Commit the changes
            conn.commit()
            print("Database tables created successfully (or already exist).")
    except sqlite3.Error as create_tables_error:
        print(f"Database error during table creation: {create_tables_error}")