"""
Create a small DB to host burns history.

"""

import sqlite3

from logging import getLogger

logger = getLogger(__name__)


try:
    sqlite_connection = sqlite3.connect("burns.db")
    sqlite_create_table_query = """
                                CREATE TABLE Burns (
                                Address TEXT PRIMARY KEY UNIQUE,
                                LastBurnDate DATE,
                                TotalBurnt FLOAT);
                                """

    cursor = sqlite_connection.cursor()
    logger.info("Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    logger.info("Table created")
    cursor.close()

except sqlite3.Error as error:
    logger.error(f"Error creating the table: {error}")
finally:
    if sqlite_connection:
        sqlite_connection.close()
        logger.info("Closed SQLite connection")
