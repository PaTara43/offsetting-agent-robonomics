"""
Constants list.

Robonomics node launch for dev tests:
    1st node: target/debug/robonomics --dev --tmp -l rpc=trace
    2nd node: target/debug/robonomics --dev --tmp --ws-port 9991 -l rpc=trace

"""

from os import path


STATEMINE_SS58_ADDRESS_TYPE = 2
STATEMINE_REMOTE_WS = "wss://statemine-rpc.polkadot.io"
CARBON_ASSET_ID = "0xf7917950a91fcce8ca17b6d24f8607490000000000000067"

ROBONOMICS_NODE = None  # None for Kusama Parachain Node. "ws://127.0.0.1:9944" for testing.
AGENT_NODE_REMOTE_WS = "wss://robonomics.rpc.multi-agent.io/"  # 91.122.35.172
DAPP_NODE_REMOTE_WS = "wss://kusama.rpc.robonomics.network/"  # This if for _dapp_pubsub_simulator 23.88.52.147

LAST_BURN_DATE_QUERY_TOPIC = "last_burn_date_query"
LAST_BURN_DATE_RESPONSE_TOPIC = "last_burn_date_response"
LIABILITY_QUERY_TOPIC = "liability_query"

SQLITE_DB_PATH = path.join(path.abspath(path.dirname(__file__)), "..", "db", "burns.db")

CO2_INTENSITY_TABLE_PATH = path.join(
    path.abspath(path.dirname(__file__)), "..", "co2_intensity", "carbon-intensity-electricity-01-09-2022_cropped.csv"
)
WORLD_CO2_INTENSITY = 425.23486328125

W3GW = "https://crustwebsites.net"
W3PS = "https://pin.crustcode.com"
