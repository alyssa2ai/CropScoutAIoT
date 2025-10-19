import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# =================================================================
# Section 1: Knowledge Base and Initializations
# =================================================================

# Recommendations Dictionary
recommendations = {
    "Tomato___Late_blight": {
        "description": "Late blight is a fungal disease that can quickly destroy tomato plants, especially in cool, wet weather.",
        "chemical_treatment": "Apply fungicides containing mancozeb, chlorothalonil, or copper. Follow product instructions carefully.",
        "organic_treatment": "Use a copper-based organic fungicide. Ensure good air circulation by pruning lower leaves. Remove and destroy infected plants immediately.",
        "prevention": "Water plants at the base to avoid wet leaves. Provide ample spacing between plants. Plant disease-resistant varieties if possible."
    },
    "Apple___Apple_scab": {
        "description": "Apple scab is a common fungal disease affecting apple trees, causing dark, scabby spots on leaves and fruit.",
        "chemical_treatment": "Apply fungicides like captan or myclobutanil starting from early spring.",
        "organic_treatment": "Spray with sulfur-based organic fungicides. Rake up and destroy fallen leaves in the autumn to reduce fungal spores.",
        "prevention": "Choose scab-resistant apple varieties. Prune trees to improve air circulation and sunlight penetration."
    },
    "Tomato___healthy": {
        "description": "The plant appears to be healthy.",
        "chemical_treatment": "No treatment necessary.",
        "organic_treatment": "No treatment necessary.",
        "prevention": "Continue good watering practices, ensure proper nutrients, and monitor for any signs of pests or disease."
    }
}

# --- Firebase Initialization (Cached) ---
@st.cache_resource
def init_firebase():
    # If firebase already initialized, return the real client
    if firebase_admin._apps:
        return firestore.client()

    # If firebase credentials file exists, initialize real Firebase
    import os
    # Try multiple ways to load credentials (path env var, raw JSON env var, streamlit secrets)
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    if cred_path and os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            st.warning(f"Error initializing Firebase with {cred_path}: {e}. Trying other credential sources.")

    # If raw JSON for credentials was provided via env var
    raw_json = os.environ.get("FIREBASE_CREDENTIALS", None)
    if raw_json:
        try:
            import json
            cred_dict = json.loads(raw_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            st.warning(f"Error initializing Firebase from FIREBASE_CREDENTIALS env var: {e}. Trying Streamlit secrets or falling back.")

    # Try Streamlit secrets (st.secrets.firebase should be a dict or JSON string)
    try:
        if hasattr(st, 'secrets') and st.secrets and "firebase" in st.secrets:
            firebase_secret = st.secrets["firebase"]
            if isinstance(firebase_secret, str):
                import json
                firebase_secret = json.loads(firebase_secret)
            cred = credentials.Certificate(firebase_secret)
            firebase_admin.initialize_app(cred)
            return firestore.client()
    except Exception as e:
        st.warning(f"Error initializing Firebase from Streamlit secrets: {e}. Falling back to in-memory stub.")

    # Graceful fallback: create a minimal in-memory Firestore-like stub
    st.warning("firebase_credentials.json not found in copy — using an in-memory stub for Firestore. No remote reads/writes will occur.")

    class CollectionStub:
        def __init__(self, name):
            self.name = name
            self._docs = []

        def where(self, *args, **kwargs):
            # Return self to allow chaining .where(...).where(...)
            return self

        def stream(self):
            # Return an iterator of zero documents
            return iter([])

        def add(self, doc):
            # Store added documents in memory (no persistence)
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

db = init_firebase()

# --- Model Loading (Cached) ---
@st.cache_resource
def load_model():
    # Prefer a local models/ directory in the copy. This keeps the original project untouched.
    model_path_candidates = [
        "models/trained_model.keras",
        "models/my_model.keras",
        "models/my_model.h5",
        "New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/trained_model.keras",
    ]
    model_path = None
    import os
    for p in model_path_candidates:
        if os.path.exists(p):
            model_path = p
            break
    # If the trained model file is missing in this copy, return a small stub model
    try:
        if model_path is None:
            raise FileNotFoundError("No model found in candidates: " + str(model_path_candidates))
        model = tf.keras.models.load_model(model_path)
        return model
    except (IOError, OSError, ValueError, tf.errors.NotFoundError, FileNotFoundError) as e:
        st.warning("Trained model not found in copy — using a dummy model that always predicts class 0. Uploading images will return the first class.")

        class ModelStub:
            def predict(self, _image_array):
                # Return a single-sample prediction where class 0 has probability 1.0
                return np.array([[1.0]])

        return ModelStub()

model = load_model()

# --- Data Fetching, Preprocessing, and Prediction Functions ---
@st.cache_data(ttl=60)
def fetch_data_by_date(collection_name, start_date, end_date):
    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
    docs = db.collection(collection_name).where('timestamp', '>=', start_datetime).where('timestamp', '<=', end_datetime).stream()
    data = [doc.to_dict() for doc in docs]
    if not data: return pd.DataFrame()
    df = pd.DataFrame(data)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    return df

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).resize((128, 128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    return input_arr

def model_prediction(image_array):
    predictions = model.predict(image_array)
    return np.argmax(predictions)

# --- Sidebar ---
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition", "Live Monitoring"])

# --- Page Rendering Logic ---

if app_mode == "Home":
    st.header("PLANT DISEASE RECOGNITION SYSTEM")
    import os
    if os.path.exists("home_page.jpeg"):
        st.image("home_page.jpeg", use_container_width=True)
    else:
        st.info("home_page.jpeg not found in this copy. Upload or place it next to main.py to display the homepage image.")
    st.markdown("Welcome to my Plant Disease Recognition System!")

elif app_mode == "About":
    st.header("About The Project")
    st.markdown("""#### About Dataset...""")

elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image:")
    
    if test_image is not None:
        if st.button("Show Image"):
            st.image(test_image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Predict"):
            st.snow()
            st.write("My Prediction")
            
            image_bytes = test_image.getvalue()
            processed_image = preprocess_image(image_bytes)
            result_index = model_prediction(processed_image)
            
            class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                          'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew',
                          'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                          'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
                          'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                          'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                          'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
                          'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                          'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
                          'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
                          'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold',
                          'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
                          'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                          'Tomato___healthy']
                          
            st.success(f"The model is predicting it's a {class_name[result_index]}")
            
            # --- THIS IS THE CORRECT PLACEMENT FOR THE RECOMMENDATION CODE ---
            predicted_disease = class_name[result_index]

            if predicted_disease in recommendations:
                st.markdown("---")
                st.subheader("Recommendations")
                info = recommendations[predicted_disease]
                
                st.info(f"**Description:** {info['description']}")
                st.warning(f"**Chemical Treatment:** {info['chemical_treatment']}")
                st.success(f"**Organic Treatment:** {info['organic_treatment']}")
                st.info(f"**Prevention:** {info['prevention']}")

elif app_mode == "Live Monitoring":
    st.header("Historical Data Dashboard")
    st.markdown("Select a date range to view historical sensor and prediction data.")
    
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
    end_date = col2.date_input("End Date", datetime.date.today())

    if st.button("Show History"):
        predictions_df = fetch_data_by_date("predictions", start_date, end_date)
        sensors_df = fetch_data_by_date("sensor_readings", start_date, end_date)
        
        st.subheader(f"Data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
        
        if not sensors_df.empty:
            st.subheader("Last Recorded Sensor Readings in Range")
            # ... (rest of dashboard code)
        else:
            st.warning("No sensor data available for the selected date range.")

        if not predictions_df.empty:
            st.subheader("Disease Predictions in Range")
            # ... (rest of dashboard code)
        else:
            st.warning("No prediction data available for the selected date range.")
