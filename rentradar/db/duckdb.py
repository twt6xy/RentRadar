import logging

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class DuckDBManager:
    """
    Manages a DuckDB database connection, offering utilities to create tables from pandas DataFrames
    or supported file formats (CSV, Parquet), execute SQL queries, list tables, and use the manager
    as a context manager for automatic resource management.

    Attributes:
        db_path (str): The path to the DuckDB database file.
        conn (duckdb.DuckDBPyConnection): The connection object to the DuckDB database.
    """

    def __init__(self, db_path: str):
        """
        Initializes or connects to a DuckDB database at the specified path.
        """
        self.db_path = db_path
        self.conn = duckdb.connect(database=self.db_path, read_only=False)

    def open_connection(self):
        """
        Opens a connection to the DuckDB database.
        """
        try:
            self.conn = duckdb.connect(database=self.db_path, read_only=False)
            logger.info("Connected to DuckDB database at %s", self.db_path)
        except Exception as e:
            logger.error("Failed to connect to DuckDB database: %s", e)
            raise

    def table_from_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Creates a table in the DuckDB database from a pandas DataFrame.
        """
        try:
            df.to_sql(table_name, self.conn, if_exists="replace", index=False)
            logger.info("Table '%s' created from DataFrame", table_name)
        except Exception as e:
            logger.error("Failed to create table: %s", e)
            raise

    def table_from_file(
        self, file_path: str, table_name: str, file_format: str = "csv"
    ):
        """
        Creates a table in the database from a file.
        """
        try:
            if file_format.lower() == "csv":
                df = pd.read_csv(file_path)
            elif file_format.lower() == "parquet":
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

            self.table_from_dataframe(df, table_name)
            logger.info("Table '%s' created from file %s", table_name, file_path)
        except Exception as e:
            logger.error(
                "Failed to create table '%s' from file %s: %s", table_name, file_path, e
            )
            raise

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query on the database and returns the result.
        """
        try:
            result = self.conn.execute(query).fetchdf()
            logger.info("Executed query: %s", query)
            return result
        except Exception as e:
            logger.error("Failed to execute query: %s: %s", query, e)
            raise

    def list_tables(self) -> pd.DataFrame:
        """
        Lists all tables in the database.
        """
        return self.execute_query("SHOW TABLES")

    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """
        Returns the schema of the specified table in the database.
        """
        query = f"PRAGMA table_info({table_name})"
        return self.conn.execute(query).fetchdf()

    def close(self):
        """
        Closes the connection to the database.
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def __enter__(self):
        """
        Allows the class to be used as a context manager.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Allows the class to be used as a context manager.
        """
        self.close()
