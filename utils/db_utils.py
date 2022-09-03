"""
SQL DB interaction via SQLite.

"""

import sqlite3
import typing as tp

from logging import getLogger

from constants import SQLITE_DB_PATH

logger = getLogger(__name__)


def sql_query(query: str) -> tp.Any:
    """
    Perform a provided SQL query to the local DB.

    :param query: SQL command to perform.

    :return: Query result.

    """

    try:
        sqlite_connection = sqlite3.connect(SQLITE_DB_PATH)
        cursor = sqlite_connection.cursor()
        logger.info("Connected to the DB.")
        logger.info(f"Query to execute: {query}")

        cursor.execute(query)
        if "INSERT" or "DELETE" in query:
            sqlite_connection.commit()
        result: tp.Any = cursor.fetchall()
        logger.info(f"Query result: {result}")
        cursor.close()

        return result
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logger.info("Closed SQL DB connection")
