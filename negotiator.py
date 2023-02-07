"""
This module talks with the DAPP via Robonomics PubSub interface providing information about the latest burns.

"""

import json
import logging
import traceback
import typing as tp

from datetime import date
from time import time

from utils import (
    pubsub_subscribe,
    parse_income_message,
    pubsub_send,
    get_last_compensation_date,
    get_kwh_to_compensate,
    LAST_COMPENSATION_DATE_QUERY_TOPIC,
    LAST_COMPENSATION_DATE_RESPONSE_TOPIC,
)

logger = logging.getLogger(__name__)


def callback_negotiations(obj, update_nr, subscription_id):
    """
    Process incoming PubSub negotiations messages. In this function 'return' statement will collapse the subscription,
        so avoided.

    :param obj: Income message.
    :param update_nr: Message index.
    :param subscription_id: Subscription ID.

    """

    try:

        income_data: tp.Dict[str, tp.Union[str, float]] = parse_income_message(raw_data=obj["params"]["result"]["data"])
        logger.info(f"Got request for last compensation date and N kWh to be compensated: {income_data}")
        last_compensation_date: tp.Optional[date] = get_last_compensation_date(income_data["address"])
        kwh_to_compensate: float = get_kwh_to_compensate(income_data["address"], income_data["kwh_current"])

        logger.info("Sending response to the DApp")
        outcome_data: str = json.dumps(
            dict(
                address=income_data["address"], last_compensation_date=last_compensation_date, kwh_to_compensate=kwh_to_compensate, timestamp=time()
            )
        )
        pubsub_send(LAST_COMPENSATION_DATE_RESPONSE_TOPIC, outcome_data)

    except Exception:
        logger.error(f"Failed to process DApp query: {traceback.format_exc()}")


def main():
    """
    Initialize pubsub listener to process incoming messages.

    """

    logger.info("Starting negotiator... Waiting for incoming messages.")
    negotiator = pubsub_subscribe(topic=LAST_COMPENSATION_DATE_QUERY_TOPIC, callback=callback_negotiations)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
