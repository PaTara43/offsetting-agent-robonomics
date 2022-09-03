"""
IPFS posting and downloading mechanism using Web3 Gateway.

"""

import json
import requests

from ast import literal_eval
from substrateinterface import Keypair

from constants import W3GW, W3PS
from exceptions import FailedToUploadFile, FailedToPinFile
from substrate_utils import create_keypair


def ipfs_get_data(cid: str) -> dict:
    """
    Get content of a JSON-like file in IPFS network

    :param cid: IPFS cid.

    :return: Content of a file stored.

    """

    response = requests.get(W3GW + "/ipfs/" + cid)
    return literal_eval(response.content.decode("utf-8"))


def ipfs_upload_dict(seed: str, content: dict) -> str:
    """
    Upload and pin a file to IPFS via IPFS Web3 Gateway with private key-signed message. The signed message is user's
        pubkey. https://wiki.crust.network/docs/en/buildIPFSWeb3AuthGW#usage.

    :param seed: Account seed in raw/mnemonic form.
    :param content: Content to upload to IPFS.

    :return: IPFS cid.

    """

    keypair: Keypair = create_keypair(seed)
    content_bytes = json.dumps(content).encode("utf-8")

    response = requests.post(
        W3GW + "/api/v0/add",
        auth=(f"sub-{keypair.ss58_address}", f"0x{keypair.sign(keypair.ss58_address).hex()}"),
        files={"file@": (None, content_bytes)},
    )

    if response.status_code == 200:
        resp = literal_eval(response.content.decode("utf-8"))
        cid = resp["Hash"]
    else:
        raise FailedToUploadFile(response.status_code)

    _pin_file(keypair, cid)

    return cid


def _pin_file(keypair: Keypair, ipfs_cid: str) -> bool:
    """
    Pin file for some time via Web3 IPFS pinning service. This may help to spread the file wider across IPFS.

    :param keypair: Account keypair.
    :param ipfs_cid: Uploaded file cid.

    :return: Server response flag.
    """

    body = {"cid": ipfs_cid}

    response = requests.post(
        W3PS + "/psa/pins",
        auth=(f"sub-{keypair.ss58_address}", f"0x{keypair.sign(keypair.ss58_address).hex()}"),
        json=body,
    )

    if response.status_code == 200:
        return True
    else:
        raise FailedToPinFile(response.status_code)
