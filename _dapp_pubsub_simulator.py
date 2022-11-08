import logging
import os

from robonomicsinterface import Account, PubSub, Liability
from substrateinterface import KeypairType
from threading import Thread
from time import time, sleep

from utils.constants import (
    LAST_BURN_DATE_QUERY_TOPIC,
    LAST_BURN_DATE_RESPONSE_TOPIC,
    LIABILITY_QUERY_TOPIC,
    DAPP_NODE_REMOTE_WS
)
from utils.pubsub import parse_income_message
from utils.ipfs_utils import ipfs_upload_dict

logger = logging.getLogger(__name__)


def callback_negotiations(obj, update_nr, subscription_id):
    print(parse_income_message(obj["params"]["result"]["data"]))


# PubSub subscriber
def subscribe_negotiations():
    account_ = Account(remote_ws=DAPP_NODE_REMOTE_WS)
    pubsub_ = PubSub(account_)

    pubsub_.subscribe(LAST_BURN_DATE_RESPONSE_TOPIC, result_handler=callback_negotiations)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # Create DAPP account
    dapp_user = Account(remote_ws=DAPP_NODE_REMOTE_WS,
                        seed=os.getenv("DAPP_SEED"),
                        crypto_type=KeypairType.ED25519)

    # Negotiations subscriber emulation
    negotiations_subscriber_thread = Thread(target=subscribe_negotiations)
    negotiations_subscriber_thread.start()

    # Negotiations query emulation:
    pubsub = PubSub(dapp_user)

    while True:

        query = input("last burn date (1)/liability (2)")

        if query == "1":
            negotiations_query = dict(address=dapp_user.get_address(), kwh_current=20.0, timestamp=time())
            print(f"publish: {pubsub.publish(LAST_BURN_DATE_QUERY_TOPIC, str(negotiations_query))}")
        elif query == "2":
            technics = ipfs_upload_dict(os.getenv("DAPP_SEED"), dict(geo="59.934280, 30.335099", kwh=5.0))
            economics = 0
            promisee = dapp_user.get_address()
            liability_singer = Liability(dapp_user)
            promisee_signature = liability_singer.sign_liability(technics, economics)

            liability_query = dict(technics=technics,
                                   economics=economics,
                                   promisee=promisee,
                                   promisee_signature=dict(ED25519=promisee_signature),
                                   timestamp=time())
            print(pubsub.connect("/dns/robonomics.rpc.multi-agent.io/tcp/44440"))
            sleep(2)
            print(pubsub.publish(LIABILITY_QUERY_TOPIC, str(liability_query)))
