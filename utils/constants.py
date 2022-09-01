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
PUBSUB_LISTEN_MULTIADDR = "/ip4/127.0.0.1/tcp/44440"
NEGOTIATOR_TOPIC = "negotiations"
LIABILITY_TOPIC = "liability"
SQLITE_DB_PATH = path.join(path.abspath(path.dirname(__file__)), "..", "db", "burns.db")
