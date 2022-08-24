import typing as tp

from scalecodec.types import GenericCall, GenericExtrinsic
from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt

from .constants import CARBON_ASSET_ID, IPCI_REMOTE_WS, IPCI_TYPE_REGISTRY, IPCI_SS58_ADDRESS_TYPE


def create_instance(endpoint: str) -> SubstrateInterface:
    """
    Create on IPCI Substrate instance.

    :param endpoint: Parachain endpoint.

    :return: IPCI Substrate instance.

    """

    interface: SubstrateInterface = SubstrateInterface(
        url=endpoint,
        ss58_format=IPCI_SS58_ADDRESS_TYPE,
        type_registry_preset="substrate-node-template",
        type_registry=IPCI_TYPE_REGISTRY,
    )

    return interface


def create_keypair(seed: str) -> Keypair:
    """
    Create a keypair using an `os.getenv()`-provided seed.

    :param seed: Offsetting agent seed in any form.

    :return: substrateinterface Keypair.

    """

    if seed.startswith("0x"):
        return Keypair.create_from_seed(seed_hex=hex(int(seed, 16)), ss58_format=IPCI_SS58_ADDRESS_TYPE)
    else:
        return Keypair.create_from_mnemonic(seed, ss58_format=IPCI_SS58_ADDRESS_TYPE)


def burn_carbon_asset(seed: str, technics: str) -> str:
    """
    Burn carbon assets in IPCS Substrate network.

    :param seed: Offsetting agent account seed in any form.
    :param technics: Technics from liability to be parsed and executed.

    :return: transaction hash, block_num-event_idx.

    """

    keypair = create_keypair(seed)
    interface: SubstrateInterface = create_instance(endpoint)

    call: GenericCall = interface.compose_call(
        call_module="CarbonAsset",
        call_function="burn",
        call_params=dict(id=CARBON_ASSET_ID, who={"Id": keypair.ss58_address}, amount=amount),
    )

    signed_extrinsic: GenericExtrinsic = interface.create_signed_extrinsic(call=call, keypair=keypair)
    receipt: ExtrinsicReceipt = interface.submit_extrinsic(signed_extrinsic, wait_for_finalization=True)

    return receipt.extrinsic_hash
