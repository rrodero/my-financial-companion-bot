from typing import Optional
import chardet
import streamlit as st
import pandas as pd
from src.my_financial_companion_bot.managers.transaction_manager import TransactionManager
from src.my_financial_companion_bot.models.transaction import Transaction
from src.my_financial_companion_bot.models.transaction_type import TransactionType

st.set_page_config(page_title="Transactions", page_icon="💲")

st.title("Transactions")
st.header("Add Transactions")

def detect_separator_and_encoding(file, possible_separators=None, possible_encodings=None) -> tuple[str, str]:
    if possible_separators is None:
        possible_separators = [';', ':', '\t']
    if possible_encodings is None:
        possible_encodings = ['latin1', 'utf-8']

    file_content = file.getvalue()

    # Detect encoding using chardet
    encoding_detector = chardet.detect(file_content)
    detected_encoding = encoding_detector['encoding']

    first_line = ''

    try:
        # Try to read the first line with the detected encoding
        first_line = file_content.decode(detected_encoding).splitlines()[0]
    except UnicodeDecodeError:
        # If detected encoding fails, try possible encodings
        for encoding in possible_encodings:
            try:
                first_line = file_content.decode(encoding).splitlines()[0]
                detected_encoding = encoding
                break
            except UnicodeDecodeError:
                continue

    detected_separator = None
    for sep in possible_separators:
        if sep in first_line:
            detected_separator = sep
            break

    # If no separator is detected, default to comma
    if detected_separator is None:
        detected_separator = ','

    return detected_encoding, detected_separator

def load_and_inspect_csv(file) -> Optional[pd.DataFrame]:
    encoding, sep = detect_separator_and_encoding(file)

    try:
        return pd.read_csv(file, encoding=encoding, sep=sep)
    except pd.errors.EmptyDataError:
        st.error(f"The file {file.name} is empty.")
    except pd.errors.ParserError:
        st.error(f"Problem parsing file {file.name}. Check the file format.")
    except UnicodeDecodeError:
        st.error(f"Error decoding file {file.name}")
    except FileNotFoundError:
        st.error(f"The file {file.name} is not found.")
    except Exception as e:
        st.error(f"Unexpected error reading file {file.name}: {e}")

    return None


def normalize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    column_mapping = {
        'date': ['data', 'data lançamento', 'data de compra'],
        'description': ['descrição', 'histórico', 'historico'],
        'income': ['entrada'],
        'expense': ['saída', 'saida'],
        'amount': ['valor', 'valor (em r$)']
    }

    # Normalize dataframe columns
    lower_col = lambda col: col.lower().strip()
    normalized_dataframe_columns = [lower_col(col) for col in dataframe.columns]
    reverse_column_mapping = {}
    for standard_name, possible_names in column_mapping.items():
        for name in possible_names:
            normalized_name = lower_col(name)
            if normalized_name in normalized_dataframe_columns:
                original_column_name = dataframe.columns[normalized_dataframe_columns.index(normalized_name)]
                reverse_column_mapping[original_column_name] = standard_name

    dataframe.rename(columns=reverse_column_mapping, inplace=True)

    if 'income' in dataframe.columns and 'expense' in dataframe.columns:
        dataframe['amount'] = dataframe['income'] - dataframe['expense']
    elif 'income' in dataframe.columns:
        dataframe['amount'] = dataframe['income']
    elif 'expense' in dataframe.columns:
        dataframe['amount'] = -dataframe['expense']

    dataframe = dataframe.loc[:, ~dataframe.columns.duplicated()]
    columns_of_interest = ['date', 'description', 'amount']
    return dataframe[columns_of_interest]

# Section for CSV Upload
st.subheader("Upload Transactions File (CSV)")

status_text = st.sidebar.empty()

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    status_text.text("Processing CSV upload...")
    df = load_and_inspect_csv(uploaded_file)
    df = normalize_column_names(df)

    st.write(f"Preview of uploaded file **{uploaded_file.name}**:")
    st.dataframe(df.head())
    progress_bar = st.sidebar.progress(0, 'Inserting transactions...')
    size = len(df.index)
    if "transaction_manager" not in st.session_state:
        st.session_state.transaction_manager = TransactionManager(
            '/Users/rrodero/python_projects/my-financial-companion-bot/data/teste.db')
    for index, row in df.iterrows():
        new_transaction = Transaction(date=row['date'],
                                      description=row['description'],
                                      amount=row['amount'],
                                      type=TransactionType.INCOME.value if row['amount'] > 0 else TransactionType.EXPENSE.value,
                                      original_source='CSV FILE', category_id=None, tags=None, note=None,
                                      installment_series_id=None)
        st.session_state.transaction_manager.insert_transaction(new_transaction)
        progress_bar.progress(((index + 1)/size), 'Inserting transactions...')
    progress_bar.empty()
    status_text.empty()