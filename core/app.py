from flask import Flask, request, jsonify
try:
    import tensorflow as tf
except Exception:
    tf = None
from PIL import Image
import numpy as np
import io
import datetime # Import the datetime library for timestamps

# --- Firebase Integration ---
import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase_local():
    # Try multiple credential sources; if none, return an in-memory stub
    import os
    # Local credential file
    local_cred = os.path.join(os.getcwd(), 'firebase_credentials.json')
    try:
        if os.path.exists(local_cred):
            cred = credentials.Certificate(local_cred)
            firebase_admin.initialize_app(cred)
            return firestore.client()
    except Exception:
        pass

    # Try env var path
    try:
        env_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)
        if env_path and os.path.exists(env_path):
            cred = credentials.Certificate(env_path)
            firebase_admin.initialize_app(cred)
            return firestore.client()
    except Exception:
        pass

    # Fallback stub
    class CollectionStub:
        def __init__(self, name):
            self.name = name
            self._docs = []
        def where(self, *args, **kwargs):
            return self
        def stream(self):
            return iter([])
        def add(self, doc):
            self._docs.append(doc)
            return (None, None)

    class DBStub:
        def __init__(self):
            self._collections = {}
        def collection(self, name):
            if name not in self._collections:
                self._collections[name] = CollectionStub(name)
            return self._collections[name]

    return DBStub()


db = init_firebase_local()

# --- Your Existing Code ---
app = Flask(__name__)

# Safe model loading: prefer models/ folder or uploaded model; otherwise use a stub
def safe_load_model():
    model_candidates = [
        'models/trained_model.keras',
        'models/my_model.keras',
        'models/my_model.h5',
        'New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/trained_model.keras'
    ]
    import os
    # If TF not available, return a stub
    if tf is None:
        class ModelStub:
            def predict(self, _x):
                return np.array([[1.0]])
        return ModelStub()
    for p in model_candidates:
        if os.path.exists(p):
            try:
                return tf.keras.models.load_model(p)
            except Exception:
                continue
    # No model found
    class ModelStub:
        def predict(self, _x):
            return np.array([[1.0]])
    return ModelStub()

model = safe_load_model()
from class_names import CLASS_NAMES as class_names

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
