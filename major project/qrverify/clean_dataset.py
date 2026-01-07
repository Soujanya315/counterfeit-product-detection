import os
import shutil

# Current dataset path
BASE_DIR = "verifier/dataset"

# Keep only these two final folders
TARGET_CLASSES = ["genuine", "counterfeit"]

def clean_dataset():
    for root, dirs, files in os.walk(BASE_DIR):
        for d in dirs:
            if d not in TARGET_CLASSES:
                folder_path = os.path.join(root, d)
                for file in os.listdir(folder_path):
                    src = os.path.join(folder_path, file)
                    dst_class = "genuine" if "genuine" in d.lower() or "original" in d.lower() else "counterfeit"
                    dst = os.path.join(BASE_DIR, dst_class, file)
                    shutil.move(src, dst)
                shutil.rmtree(folder_path)  # delete the extra folder

if __name__ == "__main__":
    clean_dataset()
    print("✅ Dataset cleaned! Now you only have 'genuine' and 'counterfeit'.")
