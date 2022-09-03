"""
Perform various carbon asset burning process calculations.

"""

import csv
import typing as tp

from datetime import date
from geopy.geocoders import Nominatim
from logging import getLogger

from constants import COAL_SHARE_TABLE_PATH, WORLD_COAL_SHARE_COEFFICIENT
from db_utils import sql_query

logger = getLogger(__name__)


def get_last_burn_date(address: str) -> tp.Optional[date]:
    """
    Get the date of a last token burn for an account.

    :param address: Account to check.

    :return: Date of last burn. None if no burns.

    """

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
    """
    Get a number of kWt*h to burn given the record of burns.

    :param address: Account to check.
    :param kwt_current: Current account kWt*h amount.

    :return: Number of kWt*h to burn this time.

    """

    logger.info(f"SQL query to get TotalBurnt amount for address '{address}'")
    response: list = sql_query(f"SELECT TotalBurnt from Burns where Address = '{address}'")
    if not response:
        logger.info(f"No burns were made for {address}.")
        return kwt_current
    else:
        logger.info(f"kWt totally burnt: {response[0][0]}")
        return kwt_current - response[0][0]


def get_tokens_to_burn(kwt: float, geo: str) -> float:
    """
    Get an amount of carbon assets to burn based on a number of kWt*h burnt and country of residence.
        Source:
        - Coal Share by countries: https://ourworldindata.org/grapher/share-electricity-coal.

    :param kwt: Number of kWt*h to compensate.
    :param geo: Coordinates of the household.

    :return: Number of carbon assets to burn.

    """
    coal_share_coefficient: float = WORLD_COAL_SHARE_COEFFICIENT

    logger.info(f"Getting country by geo: {geo}.")
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(geo, language="en")
    if location:
        country: str = location.raw["address"]["country"]
        logger.info(f"Country based on geo: {country}.")

        logger.info(f"Getting coal share coefficient for {country}.")
        with open(COAL_SHARE_TABLE_PATH, "r") as coal_share:
            coal_share_csv = csv.reader(coal_share)
            for row in coal_share_csv:
                if row[0] == country:
                    coal_share_coefficient = float(row[1])
                    break
        logger.info(f"Coal share coefficient for {country}: {coal_share_coefficient}.")

    else:
        logger.info(f"No country was determined. Using global coefficient: {WORLD_COAL_SHARE_COEFFICIENT}.")

    kwt_coal: float = kwt * coal_share_coefficient / 100
    logger.info(f"Number of coal-powered kWt*h burnt: {kwt_coal}")

    return kwt_coal
