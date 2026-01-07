import os
import shutil
import random
from PIL import Image, ImageEnhance, ImageFilter

# CHANGE THIS to your folder path
base_dir = r"C:\Users\sohs2\OneDrive\Desktop\Logo_CNN_Training"

logos_root = os.path.join(base_dir, "genLogoOutput")
dataset_root = os.path.join(base_dir, "dataset")
genuine_root = os.path.join(dataset_root, "genuine")
counterfeit_root = os.path.join(dataset_root, "counterfeit")

os.makedirs(genuine_root, exist_ok=True)
os.makedirs(counterfeit_root, exist_ok=True)

def make_fake_variant(img: Image.Image):
    img = img.convert("RGB")
    w, h = img.size

    img = ImageEnhance.Brightness(img).enhance(random.uniform(0.5, 1.5))
    img = ImageEnhance.Contrast(img).enhance(random.uniform(0.5, 1.5))

    if random.random() < 0.6:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.7, 1.8)))

    angle = random.uniform(-18, 18)
    img = img.rotate(angle, expand=True, fillcolor=(255, 255, 255))

    w2, h2 = img.size
    left = random.randint(0, int(w2 * 0.1))
    top = random.randint(0, int(h2 * 0.1))
    right = random.randint(int(w2 * 0.9), w2)
    bottom = random.randint(int(h2 * 0.9), h2)
    img = img.crop((left, top, right, bottom))
    img = img.resize((w, h))

    return img

for brand_name in os.listdir(logos_root):
    brand_src_dir = os.path.join(logos_root, brand_name)
    if not os.path.isdir(brand_src_dir):
        continue

    print(f"Processing brand: {brand_name}")

    brand_genuine_dir = os.path.join(genuine_root, brand_name)
    brand_counterfeit_dir = os.path.join(counterfeit_root, brand_name)

    os.makedirs(brand_genuine_dir, exist_ok=True)
    os.makedirs(brand_counterfeit_dir, exist_ok=True)

    for fname in os.listdir(brand_src_dir):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        src_path = os.path.join(brand_src_dir, fname)
        shutil.copy2(src_path, os.path.join(brand_genuine_dir, fname))

        try:
            img = Image.open(src_path)
        except Exception as e:
            print("Error opening", src_path, e)
            continue

        for i in range(2):
            fake_img = make_fake_variant(img)
            fake_name = f"fake_{i}_{fname}"
            fake_path = os.path.join(brand_counterfeit_dir, fake_name)
            fake_img.save(fake_path, format="JPEG")

print("✅ Dataset built successfully!")
print("Check the new 'dataset' folder now.")
