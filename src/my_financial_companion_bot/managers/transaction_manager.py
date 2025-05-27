import sqlite3
from typing import Optional

from ..db_utils import get_db_connection
from ..models.transaction import Transaction

TRANSACTIONS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')), 
    original_source TEXT,
    category_id INTEGER,
    tags TEXT,
    note TEXT,
    installment_series_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
    FOREIGN KEY (installment_series_id) REFERENCES installment_series (series_id)
);
"""

class TransactionManager:

    def __init__(self, db_path: str):
        """
        Initializes the TransactionManager with the path to the database file.
        """
        self.db_path = db_path
        self._create_table()


    def _create_table(self):
        """
        Creates the transactions table if it doesn't exist.
        This function aligns with the roadmap step 1.3 [1].
        """
        conn = get_db_connection(self.db_path)
        try:
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(TRANSACTIONS_TABLE_SCHEMA)
                    conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")  # Basic error handling


    def insert_transaction(self, transaction_data: Transaction) -> Optional[int]:
        """
        Inserts a new transaction record into the transactions table.
        This method aligns with the roadmap step 1.3 [1].
        transaction_data is expected to be a dictionary matching the schema.
        """
        sql = """
        INSERT INTO transactions (date, description, amount, type, original_source, category_id, tags, note, installment_series_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        conn = get_db_connection(self.db_path)
        try:
            if conn:
                with conn:
                    cursor = conn.cursor()
                    values = transaction_data.to_tuple()
                    cursor.execute(sql, values)
                    conn.commit()
                    transaction_id = cursor.lastrowid
                    print(f"Transaction inserted: {transaction_id}")
                    return transaction_id
        except sqlite3.Error as e:
            print(f"Database error during insertion: {e}")
            if conn:
                conn.rollback()
            return None
        return None


