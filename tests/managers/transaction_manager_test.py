import pytest

try:
    import my_financial_companion_bot.managers.transaction_manager as tm
    from my_financial_companion_bot.models.transaction import Transaction
    from my_financial_companion_bot.models.transaction_type import TransactionType
except ImportError as e:
    pytest.fail(f"Failed to import. Ensure its path is correct. Error: {e}")




def test_insert_transaction_success(temp_db_path):
    manager = tm.TransactionManager(temp_db_path)
    transaction = Transaction(
        '2025-05-10', 'Test Transaction', 25.5,
        TransactionType.EXPENSE, 'CSV File', 1, '', '', None
    )
    assert manager.insert_transaction(transaction) == 1

