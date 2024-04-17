import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

from rentradar.db.duckdb import DuckDBManager

DB_PATH = "rentradar/db/rentradar.db"
DEFAULT_TABLE = "properties"


@st.cache_resource
def get_pyg_renderer(df: pd.DataFrame) -> "StreamlitRenderer":
    return StreamlitRenderer(df, spec_io_mode="rw")


def render_table_explorer(db_manager: DuckDBManager, default_table: str):
    tables = db_manager.list_tables()["name"].tolist()
    selected_table = st.sidebar.selectbox(
        "Select a table:", tables, index=tables.index(default_table)
    )

    if selected_table:
        query = f"SELECT * FROM {selected_table}"
        df = db_manager.execute_query(query)
        renderer = get_pyg_renderer(df)
        renderer.explorer()


def render_sql_query_explorer(db_manager: DuckDBManager):
    query = st.sidebar.text_area("Enter your SQL query:")

    if query:
        df = db_manager.execute_query(query)
        renderer = get_pyg_renderer(df)
        renderer.explorer()


def main():
    st.set_page_config(page_title="RentRadar - Charts", layout="wide")
    st.sidebar.markdown("# Explore 📈")
    st.title("📊 RentRadar Chart Builder 📈")

    input_option = st.sidebar.radio("Select an option:", ("Table", "SQL Query"))

    with DuckDBManager(DB_PATH) as db_manager:
        if input_option == "Table":
            render_table_explorer(db_manager, DEFAULT_TABLE)
        elif input_option == "SQL Query":
            render_sql_query_explorer(db_manager)


if __name__ == "__main__":
    main()
