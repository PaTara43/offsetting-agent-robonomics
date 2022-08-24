import os
import traceback

from logging import getLogger

from utils import subscribe, parse_income_message, create_liability, LIABILITY_TOPIC

logger = getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")


def callback_liability(obj, update_nr, subscription_id):
    """
    Process incoming PubSub liability request messages. In this function 'return' statement will collapse the
        subscription, so avoided.

    :param obj: Income message.
    :param update_nr: Message index.
    :param subscription_id: Subscription ID.

    """

    try:

        income_data = parse_income_message(obj["params"]["result"]["data"])
        logger.info(f"Got request for burning carbon assets: {income_data}")
        logger.info(f"Creating liability...")
        index, tr_hash = create_liability(
            seed=seed,
            technics=income_data["technics"],
            economics=income_data["economics"],
            promisee=income_data["promisee"],
            promisee_signature=income_data["promisee_signature"],
        )
        logger.info(f"Liability {index} created at {tr_hash}.")

    except Exception:
        logger.error(f"Failed process DApp query: {traceback.format_exc()}")


def main():
    """
    Initialize pubsub listener to process incoming messages.

    """

    liability_manager = subscribe(topic=LIABILITY_TOPIC, callback=callback_liability)


if __name__ == "__main__":
    main()
