import json
import os
import qrcode
from django.conf import settings
from .models import Product

def run():
    data_path = os.path.join(settings.BASE_DIR, 'verifier', 'data', 'amazon_data.txt')
    qr_output_dir = os.path.join(settings.BASE_DIR, 'verifier', 'static', 'qr_codes')
    os.makedirs(qr_output_dir, exist_ok=True)

    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                product_data = json.loads(line.strip())
                asin = product_data.get('asin')
                title = product_data.get('title', 'No Name')

                if asin and not Product.objects.filter(qr_code=asin).exists():
                    # Save to database
                    product = Product(product_name=title, qr_code=asin, verified=True)
                    product.save()

                    # Generate QR
                    qr = qrcode.make(asin)
                    qr.save(os.path.join(qr_output_dir, f"{asin}.png"))

            except Exception as e:
                print(f"Error: {e}")
