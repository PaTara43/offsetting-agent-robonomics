"""
Main script to burn assets.

"""

import logging
import os

from utils import get_tokens_to_burn, burn_carbon_asset

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    seed = os.getenv("OFFSETTING_AGENT_SEED")
    tokens_to_burn: float = get_tokens_to_burn(geo="59.934280, 30.335099", kwh=0.01)
    # These are the kwh consumed from a state power system. Coefficients used to calculate mass of CO2 emitted.
    tr_hash: tuple = burn_carbon_asset(seed=seed, tokens_to_burn=tokens_to_burn)
    print(tr_hash)
