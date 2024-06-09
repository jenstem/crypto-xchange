import os
from dotenv import load_dotenv
from mysql import connector

load_dotenv()

# Establish connection to DB
class Database:
    def __init__(self):
        self.db = connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME')
        )

# Create cursor from DB connection
# Execute SQL query
        # Fetch and store results
        # Query price and symbols
        # Sub-query to get all rows from price table
        # Check length of container (results from sub-query)
        # Calculate the profit
        # Add to list of profits
        # Create spreadsheet with profits
        # Close connection
        # Allow for exceptions

        self.cursor = self.connection.cursor()

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

        self.db.close()