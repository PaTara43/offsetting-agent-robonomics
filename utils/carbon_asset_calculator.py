"""
Perform various carbon asset burning process calculations.

"""

import csv
import typing as tp
from datetime import date
from logging import getLogger

from geopy.geocoders import Nominatim

from .constants import CO2_INTENSITY_TABLE_PATH, WORLD_CO2_INTENSITY
from .db_utils import sql_query

logger = getLogger(__name__)


def get_last_compensation_date(address: str) -> tp.Union[date, str]:
    """
    Get the date of a last token burn for an account.

    :param address: Account to check.

    :return: Date of last compensation. None if no compensations.

    """

    logger.info(f"SQL query to get LastCompensationDate for address '{address}'")
    response: list = sql_query(f"SELECT LastCompensationDate from Compensations where Address = '{address}'")

    if not response:
        logger.info(f"No compensations were made for {address}.")
        return "None"
    else:
        date_list: list = list(map(int, str(response[0][0]).split("-")))
        date_: date = date(date_list[0], date_list[1], date_list[2])
        logger.info(f"Date fetched: {date_}")
        return str(date_)


def get_kwh_to_compensate(address: str, kwh_current: float) -> float:
    """
    Get a number of kWt*h to compensate given the record of compensations.

    :param address: Account to check.
    :param kwh_current: Current account kWt*h

    :return: Number of kWt*h to compensate this time.

    """

    logger.info(f"SQL query to get TotalCompensated amount for address '{address}'")
    response: list = sql_query(f"SELECT TotalCompensated from Compensations where Address = '{address}'")
    if not response:
        logger.info(f"No compensations were made for {address}.")
        return kwh_current
    else:
        logger.info(f"kWt*h totally compensated: {response[0][0]}")
        return kwh_current - response[0][0]


def get_assets_to_burn(kwh: float, geo: str) -> float:
    """
    Get an amount of carbon assets to burn based on a number of kWt*h burnt and country of residence.
        Source:
        CO2 emission intensity by countries: https://ourworldindata.org/electricity-mix#carbon-intensity-of-electricity

        DISCLAIMER: THIS IS NOT INTENDED TO BE A COMPLETELY ACCURATE CALCULATION. THE FINAL RESULT HEAVILY DEPENDS ON
        THE TYPE OF COAL USED. ALSO, THE STATISTICS DATA MAY BE INCORRECT/OUTDATED. THEREFORE, DO NOT TREAT THIS AS
        A SCIENTIFIC RESEARCH.

    :param kwh: Number of kWt*h to compensate.
    :param geo: Coordinates of the household.

    :return: Number of carbon assets to burn.

    """
    co2_intensity: float = WORLD_CO2_INTENSITY

    logger.info(f"Getting country by geo: {geo}.")
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(geo, language="en")
    if location:
        country: str = location.raw["address"]["country"]
        logger.info(f"Country based on geo: {country}.")

        logger.info(f"Getting CO2 intensity in g/kWh for {country}.")
        with open(CO2_INTENSITY_TABLE_PATH, "r") as intensity:
            intensity_csv = csv.reader(intensity)
            for row in intensity_csv:
                if row[0] == country:
                    co2_intensity = float(row[1])
                    break
        logger.info(f"CO2 intensity for {country}: {co2_intensity} g/kWh.")

    else:
        logger.info(f"No country was determined. Using global coefficient: {WORLD_CO2_INTENSITY} g/kWh.")

    tons_co2 = kwh * co2_intensity / 10**6  # Table show how many grams of CO2 produced per kWh generated in country.

    logger.info(f"Number of metric tons of CO2 / Carbon assets to burn for {kwh} kWh: {tons_co2}.")

    return tons_co2  # 1 Carbon asset per metric tonn of co2
