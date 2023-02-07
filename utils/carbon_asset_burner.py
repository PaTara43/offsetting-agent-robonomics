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


def burn_carbon_asset(seed: str, assets_to_burn: float) -> str:
    """
    Burn carbon assets in Statemine Substrate network.

    :param seed: Offsetting agent account seed in any form.
    :param assets_to_burn: Number of assets to burn.

    :return: Transaction hash.

    """

    keypair: Keypair = create_keypair(seed)
    interface: SubstrateInterface = create_instance()

    call: GenericCall = interface.compose_call(
        call_module="Assets",
        call_function="burn",
        call_params=dict(
            id=CARBON_ASSET_ID, who={"Id": keypair.ss58_address}, amount=assets_to_burn * 10 ** CARBON_ASSET_DECIMAL
        ),
    )

    signed_extrinsic: GenericExtrinsic = interface.create_signed_extrinsic(call=call, keypair=keypair)
    receipt: ExtrinsicReceipt = interface.submit_extrinsic(signed_extrinsic, wait_for_finalization=True)

    return receipt.extrinsic_hash


def add_compensate_record(address: str, date_: date, kwh_compensated: float) -> float:
    """
    Update DB record of committed compensation.

    :param address: Liability promisee address.
    :param date_: Date when the tokens were burnt.
    :param kwh_compensated: How much kWt*h were compensated.

    :return: Total amount of kWh compensated.
    """

    logger.info(f"Adding new compensation record to the table.")

    response: list = sql_query(f"SELECT TotalCompensated from Compensations where Address = '{address}'")
    if not response:
        logger.info("Adding new address to compensations history.")
        sql_query(f"INSERT INTO Compensations VALUES ('{address}', '{date_}', {kwh_compensated})")
        return kwh_compensated
    else:
        logger.info(f"Adding new data to the existing address {address}.")
        sql_query(f"DELETE FROM Compensations WHERE Address='{address}'")
        sql_query(
            f"INSERT INTO Compensations (Address, LastCompensationDate, TotalCompensated) VALUES ('{address}', '{date_}', "
            f"'{response[0][0] + kwh_compensated}')"
        )
        return response[0][0] + kwh_compensated
