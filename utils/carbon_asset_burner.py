"""
This file contains functions to burn carbon assets in IPCI network and update burns history in local DB.

"""

from datetime import date
from logging import getLogger
from scalecodec.types import GenericCall, GenericExtrinsic
from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt

from .db_utils import sql_query
from .constants import CARBON_ASSET_ID, CARBON_ASSET_DECIMAL
from .substrate_utils import create_keypair, create_instance

logger = getLogger(__name__)


def burn_carbon_asset(seed: str, tokens_to_burn: float) -> str:
    """
    Burn carbon assets in IPCS Substrate network.

    :param seed: Offsetting agent account seed in any form.
    :param tokens_to_burn: Number of tokens to burn.

    :return: transaction hash.

    """

    keypair: Keypair = create_keypair(seed)
    interface: SubstrateInterface = create_instance()

    call: GenericCall = interface.compose_call(
        call_module="Assets",
        call_function="burn",
        call_params=dict(id=CARBON_ASSET_ID, who={"Id": keypair.ss58_address}, amount=tokens_to_burn*10**CARBON_ASSET_DECIMAL),
    )

    signed_extrinsic: GenericExtrinsic = interface.create_signed_extrinsic(call=call, keypair=keypair)
    receipt: ExtrinsicReceipt = interface.submit_extrinsic(signed_extrinsic, wait_for_finalization=True)

    return receipt.extrinsic_hash


def add_burn_record(address: str, date_: date, kwh_burnt: float):
    """
    Update DB record of committed burns.

    :param address: Liability promisee address.
    :param date_: Date when the tokens were burnt.
    :param kwh_burnt: How much kWt*h were burnt.

    """

    logger.info(f"Adding new burn record to the table.")

    response: list = sql_query(f"SELECT TotalBurnt from Burns where Address = '{address}'")
    if not response:
        logger.info("Adding new address to burns history.")
        sql_query(f"INSERT INTO Burns VALUES ('{address}', '{date_}', {kwh_burnt})")
    else:
        logger.info(f"Adding new data to the existing address {address}.")
        sql_query(f"DELETE FROM Burns WHERE Address='{address}'")
        sql_query(
            f"INSERT INTO Burns (Address, LastBurnDate, TotalBurnt) VALUES ('{address}', '{date_}', "
            f"'{response[0][0] + kwh_burnt}')"
        )
