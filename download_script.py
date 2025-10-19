import os
from kaggle.api.kaggle_api_extended import KaggleApi

# We will ignore environment variables and set the download path directly.
download_path = 'E:/kaggle_data' # <-- We are forcing it to use the E: drive for the data!

# Check if the path exists, if not, create it
if not os.path.exists(download_path):
    os.makedirs(download_path)
    
print(f"Configuration will be read from the default C: drive location.")
print(f"Dataset will be downloaded and unzipped into: {download_path}")

try:
    print("\nInitializing Kaggle API...")
    # This will now find the file in C:\Users\Bhagya\.kaggle\
    api = KaggleApi()
    api.authenticate()
    print("Authentication successful.")

    print("\nStarting dataset download and extraction... Please be patient.")
    api.dataset_download_files(
        'vipoooool/new-plant-diseases-dataset',
        path=download_path,
        unzip=True
    )

    print("\n\u2705\u2705\u2705 Download and Unzip Complete! It is done. \u2705\u2705\u2705")

except Exception as e:
    print(f"\nAn error occurred: {e}")
