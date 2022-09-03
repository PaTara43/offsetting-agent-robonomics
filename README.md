# offsetting-agent-robonomics
Substrate-based offsetting agent for carbon footprint tokens burn


This service consists of 3 modules:

- negotiator talks with the dapp via Robonomics PubSub channel, get the last burn date for an account
based on its address. It can also calculate the number of carbon assets to burn this time.

- liability_manager is responsible for creating a liabilities for the offsetting agent. 

- worker awaits for new liabilities and burns carbon assets in IPCI Network. After that finalizes the liability and reports it.
hash is uploaded to the datalog in Robonomics Network.

Local DB is used to store burns history. There is a DB creation script.