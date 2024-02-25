import duckdb
import pandas as pd


class DuckDBManager:
    """
    Manages a DuckDB database connection.

    The class provides methods to:
    - Create or connect to a DuckDB database at a specified path.
    - Create tables within the database directly from pandas DataFrames or supported file formats (CSV, Parquet).
    - Execute arbitrary SQL queries and return results as pandas DataFrames.
    - List existing tables in the database.
    - Close the database connection properly.

    Attributes:
        db_path (str): The path to the DuckDB database file.
        conn (duckdb.DuckDBPyConnection): The connection object to the DuckDB database.

    Methods:
        table_from_dataframe(df, table_name): Creates a table from a pandas DataFrame.
        table_from_file(file_path, table_name, file_format): Creates a table from a file.
        execute_query(query): Executes a given SQL query and returns the results as a DataFrame.
        list_tables(): Returns a list of all tables in the database.
        close(): Closes the database connection.
    """

    def __init__(self, db_path: str):
        """
        Initializes or connects to a DuckDB database at the specified path.

        Args:
            db_path (str): The file path to the DuckDB database.
        """
        self.db_path = db_path
        self.conn = duckdb.connect(database=self.db_path, read_only=False)

    def table_from_dataframe(self, df: pd.DataFrame, table_name: str):
        """
        Creates a table in the DuckDB database from a pandas DataFrame and ensures it is saved to disk.

        Args:
            df (pd.DataFrame): The DataFrame to store as a table.
            table_name (str): The name of the table in the database.
        """
        df.to_sql(table_name, self.conn, if_exists="replace", index=False)

    def table_from_file(
        self, file_path: str, table_name: str, file_format: str = "csv"
    ):
        """
        Creates a table in the database from a file.

        Args:
            file_path (str): The file path of the data file.
            table_name (str): The name of the table to be created in the database.
            file_format (str): The format of the file ('csv', 'parquet', etc.). Default is 'csv'.
        """
        if file_format.lower() == "csv":
            df = pd.read_csv(file_path)
        elif file_format.lower() == "parquet":
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

        self.table_from_dataframe(df, table_name)

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query on the database and returns the result as a DataFrame.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame: The result of the query.
        """
        return self.conn.execute(query).fetchdf()

    def list_tables(self) -> pd.DataFrame:
        """
        Lists all tables in the database.

        Returns:
            pd.DataFrame: A DataFrame containing the names of the tables.
        """
        return self.execute_query("SHOW TABLES")

    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()
