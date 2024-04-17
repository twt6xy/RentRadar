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

    def __init__(self, db_path: str) -> None:
        """
        Initializes or connects to a DuckDB database at the specified path.
        """
        self.db_path = db_path
        self.conn = duckdb.connect(database=self.db_path, read_only=False)

    def open_connection(self) -> None:
        """
        Opens a connection to the DuckDB database.
        """
        try:
            self.conn = duckdb.connect(database=self.db_path, read_only=False)
            logger.info("Connected to DuckDB database at %s", self.db_path)
        except Exception as e:
            logger.error("Failed to connect to DuckDB database: %s", e)
            raise

    def table_from_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
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
    ) -> None:
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

    def execute_query(self, query: str, params=None) -> pd.DataFrame:
        try:
            if params:
                result = self.conn.execute(query, params).fetchdf()
            else:
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

    def get_database_schema(self) -> pd.DataFrame:
        """
        Returns the schema of all tables in the database as a DataFrame, grouped by table names,
        showing only the column names and their types.
        """
        try:
            tables = self.list_tables()["name"].tolist()
            schema_data = []
            for table_name in tables:
                table_schema = self.get_table_schema(table_name)
                table_schema["table_name"] = table_name
                schema_data.append(table_schema)

            schema_df = pd.concat(schema_data, ignore_index=True)
            schema_df = schema_df[["table_name", "name", "type"]]

            schema_df = schema_df.groupby("table_name").apply(
                lambda x: x.reset_index(drop=True)
            )
            schema_df.index.names = ["table_name", "column_index"]
            schema_df = schema_df.drop("table_name", axis=1)

            logger.info("Retrieved database schema as DataFrame")
            return schema_df
        except Exception as e:
            logger.error("Failed to retrieve database schema as DataFrame: %s", e)
            raise

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")

    def __enter__(self) -> "DuckDBManager":
        """
        Allows the class to be used as a context manager.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Allows the class to be used as a context manager.
        """
        self.close()


class RentRadarQueryAgent(DuckDBManager):
    """
    Specialized DuckDBManager for the RentRadar application, facilitating specific queries on rentradar tables.
    Simplifies data access by encapsulating SQL operations tailored to RentRadar's data model.
    """

    def get_all_properties(self) -> pd.DataFrame:
        query = "SELECT * FROM properties"
        return self.execute_query(query)

    def get_property_by_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM properties WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_property_features_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM property_features WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_county_by_id(self, county_id: str) -> pd.DataFrame:
        query = "SELECT * FROM counties WHERE id = ?"
        return self.execute_query(query, params=(county_id,))

    def get_all_counties(self) -> pd.DataFrame:
        query = "SELECT * FROM counties"
        return self.execute_query(query)

    def get_market_stats_by_zip(self, zipcode: int) -> pd.DataFrame:
        query = "SELECT * FROM current_market_stats WHERE zipCode = ?"
        return self.execute_query(query, params=(zipcode,))

    def get_market_stats_by_bedrooms(self, bedrooms: int) -> pd.DataFrame:
        query = "SELECT * FROM current_market_stats WHERE bedrooms = ?"
        return self.execute_query(query, params=(bedrooms,))

    def get_historic_market_stats_by_zip(self, zip_code: int) -> pd.DataFrame:
        query = "SELECT * FROM historic_market_stats WHERE zipCode = ?"
        return self.execute_query(query, params=(zip_code,))

    def get_historic_market_stats_by_bedrooms(
        self, bedrooms: int, zip_code: int
    ) -> pd.DataFrame:
        query = "SELECT * FROM historic_market_stats WHERE bedrooms = ? AND zipCode = ?"
        return self.execute_query(query, params=(bedrooms, zip_code))

    def get_long_term_rentals_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM long_term_rentals WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_all_long_term_rentals(self) -> pd.DataFrame:
        query = "SELECT * FROM long_term_rentals"
        return self.execute_query(query)

    def get_owners_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM property_owners WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_properties_by_owner_id(self, owner_id: str) -> pd.DataFrame:
        query = "SELECT * FROM property_owners WHERE owner_id = ?"
        return self.execute_query(query, params=(owner_id,))

    def get_property_taxes_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM property_taxes WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_property_taxes_by_year(self, year: str) -> pd.DataFrame:
        query = "SELECT * FROM property_taxes WHERE year = ?"
        return self.execute_query(query, params=(year,))

    def get_property_taxes_by_property_id_and_year(
        self, property_id: str, year: str
    ) -> pd.DataFrame:
        query = "SELECT * FROM property_taxes WHERE property_id = ? AND year = ?"
        return self.execute_query(query, params=(property_id, year))

    def get_property_type_by_id(self, type_id: str) -> pd.DataFrame:
        query = "SELECT * FROM property_types WHERE id = ?"
        return self.execute_query(query, params=(type_id,))

    def get_all_property_types(self) -> pd.DataFrame:
        query = "SELECT * FROM property_types"
        return self.execute_query(query)

    def get_description_by_property_type(self, property_type: str) -> pd.DataFrame:
        query = "SELECT description FROM property_types WHERE propertyType = ?"
        return self.execute_query(query, params=(property_type,))

    def get_sale_listings_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM sale_listings WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_all_sale_listings(self) -> pd.DataFrame:
        query = "SELECT * FROM sale_listings"
        return self.execute_query(query)

    def get_tax_assessments_by_property_id(self, property_id: str) -> pd.DataFrame:
        query = "SELECT * FROM tax_assessments WHERE property_id = ?"
        return self.execute_query(query, params=(property_id,))

    def get_tax_assessment_by_id(self, assessment_id: str) -> pd.DataFrame:
        query = "SELECT * FROM tax_assessments WHERE assessment_id = ?"
        return self.execute_query(query, params=(assessment_id,))

    def get_tax_assessment_by_property_id_and_year(
        self, property_id: str, year: str
    ) -> pd.DataFrame:
        query = "SELECT * FROM tax_assessments WHERE property_id = ? AND year = ?"
        return self.execute_query(query, params=(property_id, year))
