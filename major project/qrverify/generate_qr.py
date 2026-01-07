import qrcode
import os

# Directory to save QR codes
output_dir = "verifier/static/qr_codes"
os.makedirs(output_dir, exist_ok=True)

# List of sample products with QR content and verification status
products = [
    {"code": "ABC123", "filename": "abc123.png", "verified": True},
    {"code": "XYZ789", "filename": "xyz789.png", "verified": True},
    {"code": "LMN456", "filename": "lmn456.png", "verified": True},
    {"code": "FAKE000", "filename": "fake000.png", "verified": False},
    {"code": "COUNTER123", "filename": "counter123.png", "verified": False},
    {"code": "DUPLICATE999", "filename": "duplicate999.png", "verified": False},
]

# Generate QR codes and save them
for product in products:
    qr = qrcode.make(product["code"])
    qr_path = os.path.join(output_dir, product["filename"])
    qr.save(qr_path)
    print(f"Saved QR for {'VALID' if product['verified'] else 'COUNTERFEIT'} product: {product['code']} -> {qr_path}")
