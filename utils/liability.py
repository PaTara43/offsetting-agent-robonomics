import typing as tp

from robonomicsinterface import Account, Liability
from substrateinterface import KeypairType


def create_liability(
    seed: str, technics: str, economics: int, promisee: str, promisee_signature: str
) -> tp.Tuple[int, str]:
    """
    Create liability for an agent ot burn a carbon tokens. Created by agent.

    :param seed: Agent seed.
    :param technics: Burning process data: kWt*h, geotag.
    :param economics: XRT reward to agent for burning. Paid by promisee.
    :param promisee: Promisee ss58_address.
    :param promisee_signature: Promisee technics and economics signed message.

    :return: liability index and transaction hash.

    """
    account = Account(seed=seed)
    liability_manager = Liability(account)

    return liability_manager.create(
        technics_hash=technics,
        economics=economics,
        promisee=promisee,
        promisor=account.get_address(),
        promisee_params_signature=promisee_signature,
        promisor_params_signature=liability_manager.sign_liability(technics_hash=technics, economics=economics),
        promisee_signature_crypto_type=KeypairType.ED25519,
    )

def report_liability(report_content: dict) -> str:

    return "abc"
