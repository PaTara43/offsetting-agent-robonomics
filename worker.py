import os
import traceback

from logging import getLogger
from robonomicsinterface import Account, Subscriber, SubEvent

from utils import burn_carbon_asset, report_liability

logger = getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")
worker_account = Account(seed=seed)


def callback_new_liability(data):
    """
    Process new Liability to find if promisor is the agent, burn tokens then.

    :param data: New liability data: index, hash, price, promisee, promisor

    """

    if data[4] == worker_account.get_address():

        try:

            logger.info(f"New liability for the agent: {data}")
            logger.info(f"Burning tokens...")
            tr_hash: str = burn_carbon_asset(seed=seed, technics=data[1]["hash"])
            logger.info(f"Reporting burn {tr_hash}")
            report_tr_hash: str = report_liability(dict(burn_transaction_hash=tr_hash))
            logger.info(f"Reported liability {data[0]} at {report_tr_hash}")

        except Exception:
            logger.error(f"Failed to process new liability: {traceback.format_exc()}")


def main():
    """
    Initialize liability subscriber to process incoming messages.

    """

    liability_subscription = Subscriber(
        account=worker_account, subscribed_event=SubEvent.NewLiability, subscription_handler=callback_new_liability
    )


if __name__ == "__main__":
    main()
