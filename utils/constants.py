"""
Constants list.
"""

from os import path

IPCI_SS58_ADDRESS_TYPE = 32
IPCI_REMOTE_WS = "wss://kusama.rpc.ipci.io"
CARBON_ASSET_ID = "0xcbf2d1c28581201dc468e312fd44413e0000000000000065"

CO2_INTENSITY_TABLE_PATH = path.join(
    path.abspath(path.dirname(__file__)), "..", "co2_intensity", "carbon-intensity-electricity-01-09-2022_cropped.csv"
)
WORLD_CO2_INTENSITY = 425.23486328125
