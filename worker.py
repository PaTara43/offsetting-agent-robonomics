import logging
import os
import traceback
import typing as tp

from robonomicsinterface import Account, Subscriber, SubEvent, ipfs_32_bytes_to_qm_hash

from utils import burn_carbon_asset, ipfs_get_data, get_tokens_to_burn, report_liability

logger = logging.getLogger(__name__)

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

            cid: str = ipfs_32_bytes_to_qm_hash(data[1]["hash"])
            technics: tp.Dict[str, tp.Union[float, str]] = ipfs_get_data(cid)
            tokens_to_burn: float = get_tokens_to_burn(technics["kwh"], technics["geo"])

            logger.info(f"Burning tokens {tokens_to_burn}...")

            tr_hash: str = burn_carbon_asset(seed=seed, tokens_to_burn=tokens_to_burn)
            logger.info(f"Reporting burn {tr_hash}")
            report_tr_hash: str = report_liability(
                seed=seed, index=data[0], report_content=dict(burn_transaction_hash=tr_hash)
            )
            logger.info(f"Reported liability {data[0]} at {report_tr_hash}")

        except Exception:
            logger.error(f"Failed to process new liability: {traceback.format_exc()}")


def main():
    """
    Initialize liability subscriber to process incoming messages.

    """

    logger.info("Starting liability subscriber... Waiting for incoming liabilities.")
    liability_subscription = Subscriber(
        account=worker_account, subscribed_event=SubEvent.NewLiability, subscription_handler=callback_new_liability
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
