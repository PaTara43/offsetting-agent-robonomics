"""
Constants list.

"""

from os import path

IPCI_TYPE_REGISTRY = {
    "types": {
        "AccountInfo": "AccountInfoWithRefCount",
        "Address": "AccountId",
        "LookupSource": "AccountId",
        "RefCount": "u8",
        "Record": "Vec<u8>",
        "TechnicalParam": "Vec<u8>",
        "TechnicalReport": "Vec<u8>",
        "EconomicalParam": "{}",
        "ProofParam": "MultiSignature",
        "LiabilityIndex": "u64",
    }
}
IPCI_SS58_ADDRESS_TYPE = 32
IPCI_REMOTE_WS = "wss://ipci.frontier.rpc.robonomics.network"
CARBON_ASSET_ID = "0xf7917950a91fcce8ca17b6d24f8607490000000000000067"

AGENT_NODE_REMOTE_WS = "ws://127.0.0.1:9944"
AGENT_LISTEN_MULTIADDR = "/ip4/127.0.0.1/tcp/44440"
NEGOTIATIONS_TOPIC = "negotiations"
LIABILITY_TOPIC = "liability"
DAPP_NODE_REMOTE_WS = "ws://127.0.0.1:9991"
DAPP_PUBLISH_MULTIADDR = "/ip4/127.0.0.1/tcp/44440"

SQLITE_DB_PATH = path.join(path.abspath(path.dirname(__file__)), "..", "db", "burns.db")

CO2_INTENSITY_TABLE_PATH = path.join(
    path.abspath(path.dirname(__file__)), "..", "co2_intensity", "carbon-intensity-electricity-01-09-2022_cropped.csv"
)
WORLD_CO2_INTENSITY = 35.9863166809082

W3GW = "https://crustwebsites.net"
W3PS = "https://pin.crustcode.com"
