"""
This module catches income liabilities and burns tokens once Liability created. Then reports.

"""
import ipfshttpclient2
import json
import logging
import os
import traceback
import typing as tp

from datetime import date
from robonomicsinterface import Account, Subscriber, SubEvent, ipfs_32_bytes_to_qm_hash, web_3_auth

from utils import (
    get_tokens_to_burn,
    burn_carbon_asset,
    add_burn_record,
    report_liability,
    AGENT_NODE_REMOTE_WS,
    pubsub_send,
    LIABILITY_REPORT_TOPIC,
    IPFS_W3GW,
)

logger = logging.getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")
worker_account = Account(seed=seed, remote_ws=AGENT_NODE_REMOTE_WS)


def callback_new_liability(data):
    """
    Process new Liability to find if promisor is the agent, burn tokens then.

    :param data: New liability data: index, hash, price, promisee, promisor

    """

    if data[4] == worker_account.get_address():

        try:

            logger.info(f"New liability for the agent: {data}")

            cid: str = ipfs_32_bytes_to_qm_hash(data[1]["hash"])
            auth = web_3_auth(seed=seed)
            client = ipfshttpclient2.connect(addr=IPFS_W3GW, auth=auth)
            technics: tp.Dict[str, tp.Union[float, str]] = client.get_json(cid)
            tokens_to_burn: float = get_tokens_to_burn(technics["kwh"], technics["geo"])

            logger.info(f"Burning tokens {tokens_to_burn}...")

            tr_hash: str = burn_carbon_asset(seed=seed, tokens_to_burn=tokens_to_burn)
            add_burn_record(address=data[3], date_=date.today(), kwh_burnt=technics["kwh"])
            logger.info(f"Reporting burn {tr_hash}")
            report_tr_hash: str = report_liability(
                seed=seed, index=data[0], report_content=dict(burn_transaction_hash=tr_hash)
            )
            logger.info(f"Reported liability {data[0]} at {report_tr_hash}")
            pubsub_send(
                topic=LIABILITY_REPORT_TOPIC,
                data=json.dumps(dict(address=data[3], success=True, report=data[0])),
            )

        except Exception:
            logger.error(f"Failed to process new liability: {traceback.format_exc()}")
            pubsub_send(
                topic=LIABILITY_REPORT_TOPIC,
                data=json.dumps({"address": data[3], "Success": "False", "Report": data[0]}),
            )


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
