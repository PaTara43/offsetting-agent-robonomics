import os
import time

from logging import getLogger
from robonomicsinterface import Account, Subscriber

from utils import parse_income_message, create_liability, PUBSUB_LISTEN_MULTIADDR

logger = getLogger(__name__)

seed = os.getenv("OFFSETTING_AGENT_SEED")


def callback_new_liability():


    # liability tracker
