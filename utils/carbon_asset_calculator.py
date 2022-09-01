import typing as tp

from logging import getLogger
from datetime import date

from db_interaction import sql_query

logger = getLogger(__name__)


def get_last_burn_date(address: str) -> tp.Optional[date]:

    logger.info(f"SQL query to get LastBurnDate for address '{address}'")
    response: list = sql_query(f"SELECT LastBurnDate from Burns where Address = '{address}'")

    if not response:
        logger.info(f"No burns were made for {address}.")
        return None
    else:
        date_list: list = list(map(int, str(response[0][0]).split("-")))
        date_: date = date(date_list[0], date_list[1], date_list[2])
        logger.info(f"Date fetched: {date_}")
        return date_


def get_kwt_to_burn(address: str, kwt_current: float) -> float:

    logger.info(f"SQL query to get TotalBurnt amount for address '{address}'")
    response: list = sql_query(f"SELECT TotalBurnt from Burns where Address = '{address}'")
    if not response:
        logger.info(f"No burns were made for {address}.")
        return kwt_current
    else:
        logger.info(f"kWt totally burnt: {response[0][0]}")
        return kwt_current - response[0][0]


def get_tokens_to_burn(kwt: float, geo: str) -> float:


    return kwt
