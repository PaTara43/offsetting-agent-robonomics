import time
import typing as tp

from ast import literal_eval
from logging import getLogger
from robonomicsinterface import Account, PubSub

from constants import AGENT_LISTEN_MULTIADDR, AGENT_NODE_REMOTE_WS, DAPP_PUBLISH_MULTIADDR, DAPP_NODE_REMOTE_WS

logger = getLogger(__name__)


def pubsub_subscribe(topic: str, callback: callable):
    """
    Subscribe to a specified topic with a specified callback

    :param topic: Topic to subscribe to.
    :param callback: Callback to execute
    """
    account = Account(remote_ws=AGENT_NODE_REMOTE_WS)
    pubsub = PubSub(account)

    pubsub.listen(AGENT_LISTEN_MULTIADDR)
    time.sleep(2)
    pubsub.subscribe(topic, result_handler=callback)


def parse_income_message(rawdata: tp.List[tp.Any]) -> dict:
    """
    Parse income PubSub Message.

    :param rawdata: Income PubSub Message.

    :return: technics, amount, promisee, promisee_signature.

    """

    for i in range(len(rawdata)):
        rawdata[i] = chr(rawdata[i])
    data: str = "".join(rawdata)
    data_dict: tp.Dict[tp.Union[dict, int, str]] = literal_eval(data)

    return data_dict


def pubsub_send(data: tp.Any, topic: str):
    """
    Send data to a topic via PubSub

    :param data: Data to send.
    :param topic: Topic to send to.
    """

    account = Account(remote_ws=DAPP_NODE_REMOTE_WS)
    pubsub = PubSub(account)

    pubsub.connect(DAPP_PUBLISH_MULTIADDR)
    time.sleep(2)

    pubsub.publish(topic, data)
