from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set default account (use first Ganache account)
w3.eth.default_account = w3.eth.accounts[0]

# Read compiled contract
with open("verifier/contracts/ProductVerification.json") as f:
    contract_data = json.load(f)

abi = contract_data["abi"]
bytecode = contract_data["bytecode"]

# Deploy contract
ProductVerification = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = ProductVerification.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Contract deployed at:", tx_receipt.contractAddress)

# Save contract address for later use
with open("verifier/contract_address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)
