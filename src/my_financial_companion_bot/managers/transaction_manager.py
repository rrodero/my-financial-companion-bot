import sqlite3
from typing import Optional, List, Dict

from ..db_utils import get_db_connection, DEFAULT_DB_PATH
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

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """
        Initializes the TransactionManager with the path to the database file.
        """
        self.db_path = db_path
        self._create_table()


    def _create_table(self):
        """
        Creates the transactions table if it doesn't exist.
        """
        conn = get_db_connection(self.db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(TRANSACTIONS_TABLE_SCHEMA)
        except sqlite3.Error as e:
            print(f"Database error during table creation: {e}")  # Basic error handling


    def insert_transaction(self, transaction_data: Transaction) -> Optional[int]:
        """
        Inserts a new transaction record into the transactions table.
        """
        sql = """
        INSERT INTO transactions (date, description, amount, type, original_source, category_id, tags, note, installment_series_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        conn = get_db_connection(self.db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, transaction_data.to_tuple())
                conn.commit()
                transaction_id = cursor.lastrowid
                print(f"Transaction inserted: {transaction_id}")
                return transaction_id
        except sqlite3.Error as e:
            print(f"Database error during insertion: {e}")
            return None

    def get_all_transactions(self) -> List[Transaction]:
        """
        Retrieves all transactions from the table.
        Returns a list of transactions.
        """
        sql = """
        SELECT transaction_id, date, description, 
        amount, type, original_source, category_id, tags, note, installment_series_id 
        FROM transactions;
        """
        conn = get_db_connection(self.db_path)
        transactions = []
        try:
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    transactions = [Transaction.from_dict(**row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error during retrieval: {e}")
        return transactions


    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        """
        Retrieves a single transaction by its ID.
        """
        sql = """
        SELECT transaction_id, date, description, 
        amount, type, original_source, category_id, tags, note, installment_series_id 
        FROM transactions WHERE transaction_id = ?;
        """
        conn = get_db_connection(self.db_path)
        transaction = None
        try:
            if conn:
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, (transaction_id,))
                    row = cursor.fetchone()
                    if row:
                        transaction = Transaction.from_dict(**row)
        except sqlite3.Error as e:
            print(f"Database error during retrieval by ID: {e}")
        return transaction


    def update_transaction(self, transaction_id: int, update_data: Dict) -> bool:
        """
        Updates an existing transaction by ID with new data.
        update_data is a dictionary of columns to update.
        """
        # Build SQL query dynamically based on update_data keys
        set_clauses = [f"{key} = ?" for key in update_data.keys() if key != 'transaction_id']
        if not set_clauses:
            print("No data provided for update.")
            return False

        sql = f"UPDATE transactions SET {', '.join(set_clauses)} WHERE transaction_id = ?"
        values = list(update_data.values()) + [transaction_id]

        try:
            conn = get_db_connection(self.db_path)
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, values)
                # conn.commit()
                print(f"Transaction ID {transaction_id} updated.")
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
            return False


    def delete_transaction(self, transaction_id) -> bool:
        """
        Delete a transaction by its ID
        :param transaction_id:
        :return:
        """
        sql = "DELETE FROM transactions WHERE transaction_id = ?"
        try:
            conn = get_db_connection(self.db_path)
            with conn:
                cursor = conn.cursor()
                cursor.execute(sql, (transaction_id,))
                print(f"Transaction ID {transaction_id} deleted.")
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error during deletion: {e}")
            return False


