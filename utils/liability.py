"""
Tool for creating and reporting liabilities in Robonomics Network.

"""

import json
import typing as tp

from robonomicsinterface import Account, Liability, ipfs_upload_content, web_3_auth
from .constants import ROBONOMICS_NODE, UPLOAD_W3GW


def create_liability(
    seed: str,
    technics: str,
    economics: int,
    promisee: str,
    promisee_signature: str,
    promisee_signature_crypto_type: int,
) -> tp.Tuple[int, str]:
    """
    Create liability for an agent ot burn a carbon tokens. Created by agent.

    :param seed: Agent seed.
    :param technics: Burning process data: kWt*h, geotag.
    :param economics: XRT reward to agent for burning. Paid by promisee.
    :param promisee: Promisee ss58_address.
    :param promisee_signature: Promisee technics and economics signed message.
    :param promisee_signature_crypto_type: Promisee signature crypto type

    :return: liability index and transaction hash.

    """
    account = Account(seed=seed, remote_ws=ROBONOMICS_NODE)
    liability_manager = Liability(account)

    return liability_manager.create(
        technics_hash=technics,
        economics=economics,
        promisee=promisee,
        promisor=account.get_address(),
        promisee_params_signature=promisee_signature,
        promisor_params_signature=liability_manager.sign_liability(technics_hash=technics, economics=economics),
        promisee_signature_crypto_type=promisee_signature_crypto_type,
    )


def report_liability(seed: str, index: int, report_content: dict) -> str:
    """
    Finalize and report liability when job is done.

    :param seed: Agent seed.
    :param index: Liability index.
    :param report_content: Report content to pass to report as IPFS hash.

    :return: Finalization transaction hash.

    """

    account = Account(seed=seed, remote_ws=ROBONOMICS_NODE)
    liability_manager = Liability(account)

    auth = web_3_auth(seed=seed)
    report_content_cid, _ = ipfs_upload_content(content=json.dumps(report_content), gateway=UPLOAD_W3GW, auth=auth)

    return liability_manager.finalize(index=index, report_hash=report_content_cid)
