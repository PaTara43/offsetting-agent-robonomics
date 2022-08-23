import json
import os
import traceback

from datetime import date
from logging import getLogger

from utils import (
    subscribe,
    parse_income_message,
    send,
    get_last_burn_date,
    get_kwt_to_burn,
    NEGOTIATOR_TOPIC,
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

        income_data = parse_income_message(obj['params']['result']['data'])
        logger.info(f"Got request for last burn date and N assets to be burnt: {income_data}")
        last_burn_date: date = get_last_burn_date(income_data["address"])
        kwt_to_burn: float = get_kwt_to_burn(income_data["address"], income_data["n_current"])

        logger.info("Sending response to the DApp")
        outcome_data: str = json.dumps(dict(last_burn_date=last_burn_date, kwt_to_burn=kwt_to_burn))
        send(outcome_data, NEGOTIATOR_TOPIC)

    except Exception:
        logger.error(f"Failed to process DApp query: {traceback.format_exc()}")


def main():
    """
    Initialize pubsub listener to process incoming messages.

    """

    negotiator = subscribe(topic=NEGOTIATOR_TOPIC, callback=callback_negotiations)

if __name__ == '__main__':
    main()
