"""
This module listens to liability queries in Robonomics Pubsub and creates a liability once requested.

"""

import logging
import os
import traceback
import typing as tp

from utils import LIABILITY_QUERY_TOPIC, create_liability, parse_income_message, pubsub_subscribe

logger = logging.getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")
keypair_type: dict = {"ED25519": 0, "SR25519": 1, "ECDSA": 2}


def callback_liability(obj, update_nr, subscription_id):
    """
    Process incoming PubSub liability request messages. In this function 'return' statement will collapse the
        subscription, so avoided.

    :param obj: Income message.
    :param update_nr: Message index.
    :param subscription_id: Subscription ID.

    """

    try:

        income_data: tp.Dict[str, tp.Union[str, int, dict]] = parse_income_message(obj["params"]["result"]["data"])
        logger.info(f"Got request for kWh offsetting: {income_data}")
        logger.info(f"Creating liability...")
        promisee_signature_crypto_type: str = list(income_data["promisee_signature"].keys())[0]
        index, tr_hash = create_liability(
            seed=seed,
            technics=income_data["technics"],
            economics=income_data["economics"],
            promisee=income_data["promisee"],
            promisee_signature=income_data["promisee_signature"][promisee_signature_crypto_type],
            promisee_signature_crypto_type=keypair_type[promisee_signature_crypto_type],
        )
        logger.info(f"Liability {index} created at {tr_hash}.")

    except Exception:
        logger.error(f"Failed process DApp query: {traceback.format_exc()}")


def main():
    """
    Initialize pubsub listener to process incoming messages.

    """

    logger.info("Starting liability_manager... Waiting for incoming messages.")
    liability_manager = pubsub_subscribe(topic=LIABILITY_QUERY_TOPIC, callback=callback_liability)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
