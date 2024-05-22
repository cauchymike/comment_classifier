import pandas as pd
from sqlalchemy import create_engine
import time

class PostgresDB:
    def __init__(self, conn_string: str) -> None:
        """
        Initialize the PostgresDB class.

        Args:
            conn_string (str): PostgreSQL connection string.
        """
        self.conn_string = conn_string
        self.engine = None
        self.connection = None  # Store the connection object

    def connect(self) -> None:
        """
        Connect to the PostgreSQL database using SQLAlchemy.
        """
        try:
            self.engine = create_engine(self.conn_string)
            self.connection = self.engine.connect()  # Store the connection
            print("Connected to PostgreSQL database.")
        except Exception as e:
            print("Error connecting to PostgreSQL:", e)

    def fetch_records(self, table_name: str) -> pd.DataFrame:
        """
        Fetch records from a specified table using pandas.

        Args:
            table_name (str): Name of the table to fetch records from.

        Returns:
            pd.DataFrame: DataFrame containing the fetched records.
        """
        if self.engine is None or self.connection is None:
            print("Please connect to the database first.")
            return pd.DataFrame()

        start_time = time.time()  # Record start time
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, self.engine)
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time
        print(f"Time taken to fetch records from {table_name}: {elapsed_time:.2f} seconds")

        return df

    def close_connection(self) -> None:
        """
        Close the connection to the PostgreSQL database.
        """
        if self.connection is not None:
            self.connection.close()
            print("Connection to PostgreSQL database closed.")
        else:
            print("No active connection to close.")


# # modified db connection strings to contain necessary parameters
# conn_string = "postgresql://niphemi.oyewole:W7bHIgaN1ejh@ep-delicate-river-a5cq94ee-pooler.us-east-2.aws.neon.tech:5432/Vetassist"

