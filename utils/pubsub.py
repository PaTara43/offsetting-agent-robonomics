import time
import typing as tp
from ast import literal_eval
from logging import getLogger

from robonomicsinterface import Account, PubSub

from .constants import AGENT_NODE_REMOTE_WS, DAPP_NODE_MULTIADDR

logger = getLogger(__name__)


def pubsub_subscribe(topic: str, callback: callable):
    """
    Subscribe to a specified topic with a specified callback

    :param topic: Topic to subscribe to.
    :param callback: Callback to execute
    """
    account = Account(remote_ws=AGENT_NODE_REMOTE_WS)
    pubsub = PubSub(account)
    logger.info(f"Subscribing to a {topic} topic in Robonomics PubSub...")
    pubsub.subscribe(topic, result_handler=callback)


def parse_income_message(raw_data: tp.List[tp.Any]) -> dict:
    """
    Parse income PubSub Message.

    :param raw_data: Income PubSub Message.

    :return: technics, amount, promisee, promisee_signature.

    """

    for i in range(len(raw_data)):
        raw_data[i] = chr(raw_data[i])
    data: str = "".join(raw_data)
    data_dict: tp.Dict[tp.Union[dict, int, str]] = literal_eval(data)

    return data_dict


def pubsub_send(topic: str, data: tp.Any):
    """
    Send data to a topic via PubSub

    :param topic: Topic to send to.
    :param data: Data to send.

    """

    logger.info(f"Sending data {data} to topic {topic}.")
    account = Account(remote_ws=AGENT_NODE_REMOTE_WS)
    pubsub = PubSub(account)
    logger.info(f"PubSub connect result: {pubsub.connect(DAPP_NODE_MULTIADDR)}")
    time.sleep(1)
    logger.info(f"PubSub send result: {pubsub.publish(topic, str(data))}")
