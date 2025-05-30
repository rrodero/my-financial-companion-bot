import streamlit as st
from ..managers.transaction_manager import TransactionManager

st.set_page_config(page_title="Transactions", page_icon="💲")

st.title("Transactions")
st.header("Add Transactions")

# Section for CSV Upload
st.subheader("Upload Transactions File (CSV)")

if "transaction_manager" not in st.session_state:
    st.session_state.transaction_manager = TransactionManager(":memory:")

status_text = st.sidebar.empty()

uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
if uploaded_file is not None:
    progress_bar = st.sidebar.progress(0)
    status_text.text("Processing CSV upload...")