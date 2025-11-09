"""
Dataset Download Script
This script downloads the brain tumor classification dataset from Kaggle.
The dataset will be extracted to the data/ directory for organized storage.
"""
import requests
import zipfile
import io
import os

# Get project root directory (parent of scripts directory)
scripts_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(scripts_dir)
data_dir = os.path.join(base_dir, "data")

# Create data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

url = "https://www.kaggle.com/api/v1/datasets/download/sartajbhuvaji/brain-tumor-classification-mri"
headers = {"User-Agent": "Mozilla/5.0"}

print("Downloading dataset...")
print(f"Dataset will be extracted to: {data_dir}")
response = requests.get(url, headers=headers, stream=True)

if response.status_code == 200:
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(data_dir)
    print(f"✅ Dataset downloaded and extracted into '{data_dir}' folder")
    print("Note: You may need to organize the extracted files into Training/ and Testing/ subdirectories.")
else:
    print(f"❌ Failed to download dataset. Status code: {response.status_code}")
    print("Please check your internet connection and try again.")
