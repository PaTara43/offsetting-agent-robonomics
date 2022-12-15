"""
This file contains functions to burn carbon assets in IPCI network and update burns history in local DB.

"""

from logging import getLogger
from substrateinterface import SubstrateInterface, Keypair

from .constants import STATEMINE_REMOTE_WS, STATEMINE_SS58_ADDRESS_TYPE

logger = getLogger(__name__)


def create_instance() -> SubstrateInterface:
    """
    Create on Statemine Substrate instance.

    :return: Statemine Substrate instance.

    """

    interface: SubstrateInterface = SubstrateInterface(url=STATEMINE_REMOTE_WS, ss58_format=STATEMINE_SS58_ADDRESS_TYPE)

    return interface


def create_keypair(seed: str) -> Keypair:
    """
    Create a keypair using an `os.getenv()`-provided seed.

    :param seed: Offsetting agent seed in any form.

    :return: substrateinterface Keypair.

    """

    if seed.startswith("0x"):
        return Keypair.create_from_seed(seed_hex=hex(int(seed, 16)), ss58_format=STATEMINE_SS58_ADDRESS_TYPE)
    else:
        return Keypair.create_from_mnemonic(seed, ss58_format=STATEMINE_SS58_ADDRESS_TYPE)
