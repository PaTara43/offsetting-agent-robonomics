import typing as tp

from scalecodec.types import GenericCall, GenericExtrinsic
from substrateinterface import SubstrateInterface, ExtrinsicReceipt

from .constants import CARBON_ASSET_ID, IPCI_REMOTE_WS
from .substrate import create_instance, create_keypair


def burn_carbon_asset(amount: int, seed: str, endpoint: str = IPCI_REMOTE_WS) -> tp.Tuple[str, str]:
    """
    Burn carbon assets in IPCS Substrate network.

    :param amount: Amount of tokens to be burnt, decimals (pMITO).
    :param seed: Offsetting agent account seed in any form.
    :param endpoint: Parachain endpoint.

    :return: transaction hash, block_num-event_idx.

    """

    keypair = create_keypair(seed)
    interface: SubstrateInterface = create_instance(endpoint)

    call: GenericCall = interface.compose_call(
        call_module="CarbonAsset",
        call_function="burn",
        call_params=dict(id=CARBON_ASSET_ID,
                         who={"Id": keypair.ss58_address},
                         amount=amount)
    )

    signed_extrinsic: GenericExtrinsic = interface.create_signed_extrinsic(call=call, keypair=keypair)
    receipt: ExtrinsicReceipt = interface.submit_extrinsic(signed_extrinsic, wait_for_finalization=True)
    block_num: int = interface.get_block_number(receipt.block_hash)

    return receipt.extrinsic_hash, f"{block_num}-{receipt.extrinsic_idx}"
