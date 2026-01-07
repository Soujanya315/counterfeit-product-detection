import os
import django
import json

# Set the DJANGO_SETTINGS_MODULE to your project's settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrverify.settings')
django.setup()

# Now, you can import your Django models
from verifier.models import Product

# Correct file path to dataset (relative to the current script location)
dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'dummy_products.json')

# Check if the file exists and load it
if os.path.exists(dataset_path):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Dataset loaded successfully!")

    # Insert products into the Product model
    for product_data in data:
        # Create a new product entry
        product = Product(
            product_name=product_data["product_name"],
            product_code=product_data["product_code"],
            price=product_data["price"],
            verified=product_data["verified"]
        )
        # Save the product into the database
        product.save()
    print("Products have been successfully added to the database.")
else:
    print(f"Error: The file {dataset_path} does not exist. Please check the path.")
