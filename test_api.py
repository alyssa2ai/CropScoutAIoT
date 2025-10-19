import requests

# The URL where your Flask app is running
url = 'http://127.0.0.1:5000/predict'

# --- IMPORTANT ---
# This path MUST point to a real image file on your computer.
# Please double-check that this file exists.
image_path = r"E:\kaggle_data\test\test\TomatoEarlyBlight1.JPG"

print(f"--> Attempting to send image from: {image_path}")

try:
    with open(image_path, 'rb') as f:
        # 'file' is the key that your app.py expects
        files = {'file': f}
        
        # Send the request to your running app.py server
        response = requests.post(url, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("\n--> \u2705 SUCCESS! Prediction from server:")
            print(response.json())
        else:
            print(f"\n--> \u274c ERROR: Server responded with status code {response.status_code}")
            print(f"    Response: {response.text}")

except FileNotFoundError:
    print(f"\n--> \u274c FATAL ERROR: The file was not found at the path: {image_path}")
    print("    Please make sure the path is correct and the file exists.")

except requests.exceptions.ConnectionError:
    print(f"\n--> \u274c FATAL ERROR: Could not connect to the server at {url}.")
    print("    Please make sure your 'app.py' script is running in another terminal.")
