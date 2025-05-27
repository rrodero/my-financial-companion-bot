import pytest

try:
    import my_financial_companion_bot.managers.transaction_manager as tm
    from my_financial_companion_bot.models.transaction import Transaction
    from my_financial_companion_bot.models.transaction_type import TransactionType
except ImportError as e:
    pytest.fail(f"Failed to import. Ensure its path is correct. Error: {e}")




def test_insert_retrieve_transaction_success(temp_db_path):
    manager = tm.TransactionManager(temp_db_path)
    new_transaction = Transaction(
        '2025-05-10', 'Test Transaction', 25.5,
        TransactionType.EXPENSE.value, 'CSV File', 1, '', '', None
    )
    transaction_id = manager.insert_transaction(new_transaction)

    assert transaction_id == 1

    transaction = manager.get_transaction_by_id(transaction_id)

    assert transaction.transaction_id == 1 and transaction.type == TransactionType.EXPENSE.value



