"""
Main script to burn assets.

"""

import logging
import os

from utils import get_tokens_to_burn, burn_carbon_asset

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    seed = os.getenv("OFFSETTING_AGENT_SEED")
    tokens_to_burn: float = get_tokens_to_burn(geo="59.934280, 30.335099", kwh=5.0)
    # These are kwh produced by the country power stations, coefficients used to calculate coal share and tons of CO2
    # emitted
    tr_hash: str = burn_carbon_asset(seed=seed, tokens_to_burn=tokens_to_burn)
