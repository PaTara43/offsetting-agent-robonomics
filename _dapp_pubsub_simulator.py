import time

from threading import Thread
from logging import getLogger
from robonomicsinterface import Account, PubSub

from utils.constants import LAST_BURN_DATE_QUERY_TOPIC, LAST_BURN_DATE_RESPONSE_TOPIC, \
    DAPP_NODE_REMOTE_WS, DAPP_LISTEN_MULTIADDR, DAPP_PUBLISH_MULTIADDR
from utils.pubsub import parse_income_message

logger = getLogger(__name__)


def callback(obj, update_nr, subscription_id):

    print(parse_income_message(obj["params"]["result"]["data"]))


# PubSub subscriber
def subscriber():

    account_ = Account(remote_ws=DAPP_NODE_REMOTE_WS)
    pubsub_ = PubSub(account_)

    pubsub_.listen(DAPP_LISTEN_MULTIADDR)
    time.sleep(2)
    pubsub_.subscribe(LAST_BURN_DATE_RESPONSE_TOPIC, result_handler=callback)


# Negotiations subscriber emulation
negotiations_subscriber = Thread(target=subscriber)
negotiations_subscriber.start()


# Negotiations query emulation:
remote_ws = DAPP_NODE_REMOTE_WS
account = Account(remote_ws=remote_ws)
pubsub = PubSub(account)

print(pubsub.connect(DAPP_PUBLISH_MULTIADDR))
time.sleep(2)

negotiations_query = dict(address="address", kwh_current=12.0)
print(pubsub.publish(LAST_BURN_DATE_QUERY_TOPIC, str(negotiations_query)))

