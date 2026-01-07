from bing_image_downloader import downloader
import os

# Paths for dataset
base_dir = "verifier/dataset"
categories = {
    "genuine": "original branded product",
    "counterfeit": "fake product packaging"
}

# Create dataset folders
for category, query in categories.items():
    path = os.path.join(base_dir, category)
    os.makedirs(path, exist_ok=True)
    print(f"Downloading images for {category}...")

    # Download 30 images for each category
    downloader.download(query, limit=30, output_dir=base_dir, adult_filter_off=True, force_replace=False, timeout=60)

print("✅ Image dataset ready in verifier/dataset/")
