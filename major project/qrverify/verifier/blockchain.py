import os
import json
from web3 import Web3
from django.conf import settings
from dotenv import load_dotenv
import qrcode

# -------------------- Load Environment --------------------
load_dotenv()
RPC = os.getenv("ETH_RPC", "http://127.0.0.1:7545")
CONTRACT_ADDR = os.getenv("CONTRACT_ADDR")

# -------------------- Connect to Ethereum --------------------
w3 = Web3(Web3.HTTPProvider(RPC))

if not w3.is_connected():
    raise Exception("❌ Failed to connect to Ethereum RPC. Check Ganache and RPC URL.")

# -------------------- Load Contract --------------------
ARTIFACT_PATH = os.path.join(settings.BASE_DIR, "build", "contracts", "ProductVerification.json")
with open(ARTIFACT_PATH) as f:
    artifact = json.load(f)
abi = artifact["abi"]

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDR), abi=abi)

# Make sure default account exists
if not w3.eth.accounts:
    raise Exception("❌ No accounts found in Ganache. Check Ganache setup.")

w3.eth.default_account = w3.eth.accounts[0]

# -------------------- Blockchain Functions --------------------
def register_product(product_id: str, cid: str, issuer: str):
    """Register a product on blockchain."""
    try:
        normalized_id = product_id.strip().upper()
        print(f"Registering product: {normalized_id} | CID: {cid} | Issuer: {issuer}")
        tx_hash = contract.functions.registerProduct(normalized_id, cid.strip(), issuer.strip()).transact()
        print("Transaction sent. TxHash:", tx_hash.hex())

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("✅ Transaction mined in block:", receipt.blockNumber)
        return {
            "status": "success",
            "txHash": tx_hash.hex(),
            "blockNumber": receipt.blockNumber
        }
    except Exception as e:
        print("❌ Registration error:", str(e))
        return {"status": "error", "error": str(e)}

def verify_product(product_id: str):
    """Verify a product by ID from blockchain."""
    try:
        normalized_id = product_id.strip().upper()
        cid, issuer, timestamp, exists = contract.functions.getProduct(normalized_id).call()
        return {"exists": exists, "cid": cid, "issuer": issuer, "timestamp": timestamp}
    except Exception as e:
        return {"exists": False, "error": str(e)}

# -------------------- QR Code Generator --------------------
def generate_qr(product_id: str):
    """Generate a QR code for the product ID."""
    qr_img = qrcode.make(product_id.strip().upper())
    qr_folder = os.path.join(settings.BASE_DIR, "verifier", "static", "qr_codes")
    os.makedirs(qr_folder, exist_ok=True)
    qr_path = os.path.join(qr_folder, f"{product_id.strip().upper()}.png")
    qr_img.save(qr_path)
    return qr_path
