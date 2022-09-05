import json
import os
import traceback
import typing as tp

from datetime import date
from logging import getLogger

from utils import (
    pubsub_subscribe,
    parse_income_message,
    pubsub_send,
    get_last_burn_date,
    get_kwh_to_burn,
    NEGOTIATIONS_TOPIC,
)

logger = getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")


def callback_negotiations(obj, update_nr, subscription_id):
    """
    Process incoming PubSub negotiations messages. In this function 'return' statement will collapse the subscription,
        so avoided.

    :param obj: Income message.
    :param update_nr: Message index.
    :param subscription_id: Subscription ID.

    """

    try:

        income_data: tp.Dict[str, tp.Union[str, float]] = parse_income_message(obj["params"]["result"]["data"])
        logger.info(f"Got request for last burn date and N assets to be burnt: {income_data}")
        last_burn_date: tp.Optional[date] = get_last_burn_date(income_data["address"])
        kwh_to_burn: float = get_kwh_to_burn(income_data["address"], income_data["kwh_current"])

        logger.info("Sending response to the DApp")
        outcome_data: str = json.dumps(dict(last_burn_date=last_burn_date, kwh_to_burn=kwh_to_burn))
        pubsub_send(outcome_data, NEGOTIATIONS_TOPIC)

    except Exception:
        logger.error(f"Failed to process DApp query: {traceback.format_exc()}")


def main():
    """
    Initialize pubsub listener to process incoming messages.

    """

    logger.info("Starting negotiator... Waiting for incoming messages.")
    negotiator = pubsub_subscribe(topic=NEGOTIATIONS_TOPIC, callback=callback_negotiations)


if __name__ == "__main__":
    main()
