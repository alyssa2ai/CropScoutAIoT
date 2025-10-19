from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import datetime # Import the datetime library for timestamps

# --- Firebase Integration ---
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
# Make sure 'firebase_credentials.json' is in the same folder as this script
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client() # This is your connection to the Firestore database

# --- Your Existing Code ---
app = Flask(__name__)

# Load your trained model (ensure the path is correct)
model_path = "New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/trained_model.keras"
model = tf.keras.models.load_model(model_path)
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).resize((128, 128))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['file']
    image_bytes = file.read()
    processed_image = preprocess_image(image_bytes)
    prediction = model.predict(processed_image)
    
    predicted_index = np.argmax(prediction)
    disease = class_names[predicted_index]
    confidence = float(np.max(prediction))

    # --- Save to Firebase ---
    # Create a dictionary with the data you want to save
    data_to_save = {
        'disease': disease,
        'confidence': confidence,
        'timestamp': datetime.datetime.now(datetime.timezone.utc) # Add a timestamp
    }
    # Add the data to a collection named "predictions"
    db.collection('predictions').add(data_to_save)
    print(f"Data saved to Firebase: {data_to_save}")
    
    # Return the JSON response to the client
    return jsonify({'disease': disease, 'confidence': confidence})

# --- MOVED THIS FUNCTION UP ---
# This function was below the app.run() call, which would prevent it from ever being registered.
@app.route('/sensors', methods=['POST'])
def receive_sensor_data():
    sensor_data = request.get_json()
    
    # Add a timestamp to the received data
    sensor_data['timestamp'] = datetime.datetime.now(datetime.timezone.utc)
    
    # Save the data to a new collection named "sensor_readings"
    db.collection('sensor_readings').add(sensor_data)
    
    print(f"Sensor data saved to Firebase: {sensor_data}")
    
    # Send a success response back
    return jsonify({'status': 'success', 'data_received': sensor_data}), 200

# This line MUST be the last thing in the file to start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
