import streamlit as st
try:
    import tensorflow as tf
except Exception as e:
    # Do not crash the app if tensorflow isn't installed in this environment.
    tf = None
    _tf_import_error = e
import numpy as np
from PIL import Image
import io
import datetime
import os
import json
import sys
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit.components.v1 as components
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="KrishiMitra - Plant Disease Recognition",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global UI Theme with Background and Smooth Styling ---
components.html("""
<style>
body, .stApp {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(232, 255, 247, 0.98) 100%),
        url('https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=1200&h=800&fit=crop');
    background-attachment: fixed;
    background-size: cover;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #2c3e50;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1abc9c 0%, #16a085 100%);
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}
.stButton > button {
    background: linear-gradient(90deg, #27ae60 0%, #229954 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}
h1, h2, h3, h4 {
    color: #1abc9c !important;
    font-weight: 700 !important;
}
</style>
""", height=0)

# =================================================================
# Section 1: Knowledge Base and Initializations
# =================================================================

# Recommendations Dictionary
recommendations = {
    "Tomato___Late_blight": {
        "description": {
            'en': "Late blight is a fungal disease that can quickly destroy tomato plants, especially in cool, wet weather.",
            'hi': "लेट ब्लाइट एक फफ़ुंदी रोग है जो ठंडे, गीले मौसम में टमाटर के पौधों को तेजी से नष्ट कर सकता है।",
            'kn': "ಲೇಟ್ ಬ್ಲೈಟ್ ಒಂದು ಫಂಗಲ್ ರೋಗವಾಗಿದೆ, ವಿಶೇಷವಾಗಿ ತಂಪು, ನೆನೆಸುವ ಹವಾಮಾನದಲ್ಲಿ ಟೊಮೆಟೊ ಸಸ್ಯಗಳನ್ನು ವೇಗವಾಗಿ ನಾಶಮಾಡಬಹುದು."
        },
        "chemical_treatment": {
            'en': "Apply fungicides containing mancozeb, chlorothalonil, or copper. Follow product instructions carefully.",
            'hi': "मैनकोजेब, क्लोरोथेलोनिल या तांबे वाले कवकनाशकों का प्रयोग करें। उत्पाद के निर्देशों का सावधानीपूर्वक पालन करें।",
            'kn': "ಮ್ಯಾಂಕೋಜೆಬ್, ಕ್ಲೋರೋಥಾಲೊನಿಲ್ ಅಥವಾ ತಾಮ್ರವನ್ನು ಒಳಗೊಂಡಿರುವ ಫಂಗಿಸೈಡ್ಗಳನ್ನು ಬಳಸಿ. ಉತ್ಪನ್ನದ ಸೂಚನೆಗಳನ್ನು ಗಮನವಿಟ್ಟು ಅನುಸರಿಸಿ."
        },
        "organic_treatment": {
            'en': "Use a copper-based organic fungicide. Ensure good air circulation by pruning lower leaves. Remove and destroy infected plants immediately.",
            'hi': "तांबे-आधारित जैविक फंगीसाइड का उपयोग करें। निचले पत्तों को छाँटकर अच्छी हवा का संचार बनाएँ। संक्रमित पौधों को तुरंत हटा दें और नष्ट करें।",
            'kn': "Use copper-based organic fungicide. Prune leaves for good air circulation. Remove infected plants immediately."
        },
        "prevention": {
            'en': "Water plants at the base to avoid wet leaves. Provide ample spacing between plants. Plant disease-resistant varieties if possible.",
            'hi': "पत्तियों को गीला होने से बचाने के लिए पौधों की जड़ों के पास पानी दें। पौधों के बीच पर्याप्त दूरी रखें। यदि संभव हो तो रोग-प्रतिरोधी किस्में लगाएँ।",
            'kn': "Water at plant base to keep leaves dry. Space plants adequately. Use disease-resistant varieties if available."
        }
    },
    "Apple___Apple_scab": {
        "description": {
            'en': "Apple scab is a common fungal disease affecting apple trees, causing dark, scabby spots on leaves and fruit.",
            'hi': "एप्पल स्कैब एक सामान्य फफुंदी रोग है जो सेब के पेड़ों को प्रभावित करता है और पत्तियों और फलों पर काले धब्बे बनाता है।",
            'kn': "ആപ്പിൾ സ്ക್ಯಾಬ್ ഒരു പൊതു ഫംഗസ് രോഗമാണ്, എപ്പിൾ മരങ്ങളെ ബാധಿಸುತ್ತದೆ, ഇലകളിലും ഫലങ്ങളിലും ഇരുണ്ട ഞാർശಗಳನ್ನು ಉಂಟುಮಾಡುತ್ತದೆ."
        },
        "chemical_treatment": {
            'en': "Apply fungicides like captan or myclobutanil starting from early spring.",
            'hi': "प्रारंभिक वसंत से कैप्टन या माइलोब्यूटानिल जैसे फंगीसाइड का प्रयोग करें।",
            'kn': "ಆರಂಭಿಕ ವಸಂತದಿಂದ ಕ್ಯಾಪ್ಟನ್ ಅಥವಾ ಮೈಕ್ಲೋಬ್ಯುಟನಿಲ್ ಹೀಗೆ ಫಂಗಿಸೈಡ್ ಗಳನ್ನು ಅನ್ವಯಿಸಿ."
        },
        "organic_treatment": {
            'en': "Spray with sulfur-based organic fungicides. Rake up and destroy fallen leaves in the autumn to reduce fungal spores.",
            'hi': "सल्फर-आधारित जैविक फंगीसाइड स्प्रे करें। ज्वराणु कम करने के लिए पतझड़ में गिरे हुए पत्तों को इकट्ठा करके नष्ट करें।",
            'kn': "ಗುಣಮಟ್ಟದ ಸಲ್ಫರ್ ಆಧಾರಿತ ಆಯುರ್ವೇದ್ಯ ಫಂಗಿಸೈಡನ್ನು ಸೊಂಪಾಗಿ ಸಿಂಪಡಿಸಿ. ಪತನಿಸಿದ ಎಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ ನಾಶಮಾಡಿ."
        },
        "prevention": {
            'en': "Choose scab-resistant apple varieties. Prune trees to improve air circulation and sunlight penetration.",
            'hi': "स्कैब-प्रतिरोधी सेब किस्मों का चयन करें। हवा और धूप के लिए पेड़ों को छाँटे।",
            'kn': "ಸ್ಕ್ಯಾಬ್ ಪ್ರತಿರೋಧಕ ಅಪ್ಪಲ್ ತರಗತಿಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ. ಗಾಳಿಯ ಸಂಚಲನ ಮತ್ತು ಬೆಳಕಿನ ಪ್ರವೇಶಕ್ಕಾಗಿ ಮರಗಳನ್ನು ಕತ್ತರಿಸಿ."
        }
    },
    "Tomato___healthy": {
        "description": {
            'en': "The plant appears to be healthy.",
            'hi': "पौधा स्वस्थ प्रतीत होता है।",
            'kn': "ಸಸ್ಯವು ಆರೋಗ್ಯವಾಗಿರುವಂತೆ ಕಾಣುತ್ತದೆ."
        },
        "chemical_treatment": {
            'en': "No treatment necessary.",
            'hi': "कोई रसायनात्मक उपचार आवश्यक नहीं है।",
            'kn': "ಯಾವುದೇ ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ ಅಗತ್ಯವಿಲ್ಲ."
        },
        "organic_treatment": {
            'en': "No treatment necessary.",
            'hi': "कोई जैविक उपचार आवश्यक नहीं है।",
            'kn': "ಯಾವುದೇ ಜೀವಸಾಕ್ಷರ ಚಿಕಿತ್ಸೆಯ ಅಗತ್ಯವಿಲ್ಲ."
        },
        "prevention": {
            'en': "Continue good watering practices, ensure proper nutrients, and monitor for any signs of pests or disease.",
            'hi': "अच्छे पानी और पोषण का पालन करें और कीड़ों या रोग के संकेतों के लिए निगरानी रखें।",
            'kn': "ಚೆನ್ನಾಗಿ ನೀರಾವರಿ, ಸರಿಯಾದ ಪೋಷಕಾಂಶ ಮತ್ತು ಕೀಟ ಅಥವಾ ರೋಗದ ಲಕ್ಷಣಗಳನ್ನು ಗಮನದಲ್ಲಿಡಿ."
        }
    }
}

def get_recommendation_text(disease_key: str, lang_code: str):
    entry = recommendations.get(disease_key, None)
    if not entry:
        return None
    def pick(field):
        val = entry.get(field, None)
        if isinstance(val, dict):
            return val.get(lang_code, val.get('en', ''))
        return val
    return {
        'description': pick('description'),
        'chemical_treatment': pick('chemical_treatment'),
        'organic_treatment': pick('organic_treatment'),
        'prevention': pick('prevention')
    }

# --- Firebase Initialization (Cached) ---
@st.cache_resource
def init_firebase():
    # If firebase already initialized, return the real client
    if firebase_admin._apps:
        return firestore.client()

    # Prefer an explicit local credentials file if present
    local_cred_file = os.path.join(os.getcwd(), "firebase_credentials.json")
    if os.path.exists(local_cred_file):
        try:
            cred = credentials.Certificate(local_cred_file)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            st.info(f"Found local firebase_credentials.json but failed to initialize Firebase: {e}. Trying other credential sources.")

    # Try GOOGLE_APPLICATION_CREDENTIALS env var (path to a service account file)
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None)
    if cred_path and os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            st.info(f"Error initializing Firebase with {cred_path}: {e}. Trying other credential sources.")

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
            st.info(f"Error initializing Firebase from FIREBASE_CREDENTIALS env var: {e}. Trying Streamlit secrets or falling back.")

    # Try Streamlit secrets without directly accessing st.secrets in a way that triggers Streamlit's 'No secrets found' message
    try:
        secrets_obj = getattr(st, "secrets", None) or {}
        if secrets_obj and "firebase" in secrets_obj:
            firebase_secret = secrets_obj["firebase"]
            if isinstance(firebase_secret, str):
                import json
                firebase_secret = json.loads(firebase_secret)
            cred = credentials.Certificate(firebase_secret)
            firebase_admin.initialize_app(cred)
            return firestore.client()
    except Exception as e:
        st.info(f"Error initializing Firebase from Streamlit secrets: {e}. Falling back to in-memory stub.")

    # Graceful fallback: create a minimal in-memory Firestore-like stub
    st.info("Firebase credentials not found — using an in-memory stub for Firestore. No remote reads/writes will occur.")

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
    """Load or create plant disease classification model"""
    try:
        # Use YOUR TRAINED MODEL - not the untrained one!
        import tensorflow as tf
        trained_model_path = "models/trained_model.h5"
        
        if os.path.exists(trained_model_path):
            st.info("🔄 Loading YOUR trained model...")
            model = tf.keras.models.load_model(trained_model_path)
            st.success("✅ Model loaded successfully!")
            return model
        else:
            # Fallback to disease_cnn.keras if trained model not found
            from core.model_handler import get_or_create_model
            model = get_or_create_model("models/disease_cnn.keras")
            st.success("✅ Model loaded successfully!")
            return model
    
    except Exception as e:
        st.warning(f"⚠️ Error loading model: {e}")
        
        # Fallback: Create a simple predictor
        from core.model_handler import get_or_create_model
        return get_or_create_model("models/disease_cnn.keras")

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
    """
    Preprocess image EXACTLY as in training (reference repo)
    Model expects 0-255 range (NOT normalized!)
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB').resize((128, 128))
    # DO NOT NORMALIZE - model was trained on 0-255 range!
    if tf is not None:
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # Just add batch dimension
        return input_arr
    else:
        # Minimal preprocessing using PIL + numpy
        arr = np.asarray(image).astype(np.float32)
        arr = np.expand_dims(arr, axis=0)
        return arr

def model_prediction(image_array):
    """Get disease prediction from image array"""
    predictions = model.predict(image_array)
    # predictions is already a 2D array from model output
    # Get the class with highest probability
    if len(predictions.shape) > 1:
        result_index = np.argmax(predictions[0]) if predictions.shape[0] == 1 else np.argmax(predictions, axis=1)[0]
    else:
        result_index = np.argmax(predictions)
    return result_index

# --- Sidebar ---
# --- Multilingual UI strings (English / Hindi / Kannada) ---
_translations = {
    'en': {
        'dashboard': 'Dashboard',
        'select_page': 'Select Page',
        'home': 'Home',
        'about': 'About',
        'disease_recognition': 'Disease Recognition',
        'live_monitoring': 'Live Monitoring',
        'choose_image': 'Choose an Image:',
        'show_image': 'Show Image',
        'predict': 'Predict',
        'recommendations': 'Recommendations',
        'description': 'Description',
        'chemical_treatment': 'Chemical Treatment',
        'organic_treatment': 'Organic Treatment',
        'prevention': 'Prevention',
        'read_aloud': 'Read Aloud',
        'welcome': 'Welcome to my Plant Disease Recognition System!'
    },
    'hi': {
        'dashboard': 'डैशबोर्ड',
        'select_page': 'पृष्ठ चुनें',
        'home': 'मुख पृष्ठ',
        'about': 'परियोजना के बारे में',
        'disease_recognition': 'रोग पहचान',
        'live_monitoring': 'लाइव मॉनिटरिंग',
        'choose_image': 'छवि चुनें:',
        'show_image': 'छवि दिखाएँ',
        'predict': 'भविष्यवाणी करें',
        'recommendations': 'सिफारिशें',
        'description': 'विवरण',
        'chemical_treatment': 'रासायनिक उपचार',
        'organic_treatment': 'जैविक उपचार',
        'prevention': 'रोकथाम',
        'read_aloud': 'पठन सुनाएँ',
        'welcome': 'मेरे प्लांट रोग पहचान प्रणाली में आपका स्वागत है!'
    },
    'kn': {
        'dashboard': 'ಡ್ಯಾಸ್ಬೋರ್ಡ್',
        'select_page': 'ಪುಟ ಆಯ್ಕೆ ಮಾಡಿ',
        'home': 'ಮುಖಪುಟ',
        'about': 'ಪ್ರಯೋಜನೆಯ ಬಗ್ಗೆ',
        'disease_recognition': 'ರೋಗ ಗುರುತುಮಾಡುವುದು',
        'live_monitoring': 'ಲೈವ್ ಮಾನಿಟರಿಂಗ್',
        'choose_image': 'ಚಿತ್ರ ಆಯ್ಕೆಮಾಡಿ:',
        'show_image': 'ಚಿತ್ರ ತೋರಿಸಿ',
        'predict': 'ಭವಿಷ್ಯವಾಣಿ',
        'recommendations': 'ಶಿಫಾರಸುಗಳು',
        'description': 'ವಿವರಣೆ',
        'chemical_treatment': 'ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ',
        'organic_treatment': 'ಸಸ್ಯಾವಳಿ उपचार',
        'prevention': 'ತಡೆಯುವಿಕೆ',
        'read_aloud': 'ಓದಲಿಸು',
        'welcome': 'ನನ್ನ ಸಸ್ಯ ರೋಗ ಪರಿಚಯ ವ್ಯವಸ್ಥೆಗೆ ಸ್ವಾಗತ!'
    }
}

# Language selector (code used for translations and for speech synthesis locale)
language_names = {'English': 'en', 'Hindi': 'hi', 'Kannada': 'kn'}
selected_language_name = st.sidebar.selectbox('Language', list(language_names.keys()), index=0)
lang = language_names[selected_language_name]

def t(key: str) -> str:
    return _translations.get(lang, _translations['en']).get(key, _translations['en'].get(key, key))

st.sidebar.title(t('dashboard'))
app_mode = st.sidebar.selectbox(t('select_page'), [t('home'), t('about'), t('disease_recognition'), t('live_monitoring'), 'Market Prices', 'Marketplace'])

# --- Enhanced Gamification & Animation Theme ---
components.html("""
<style>
/* Base animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes shine {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

body, .stApp {
    background: linear-gradient(135deg, #ecf0f1 0%, #e8fff7 50%, #d5f4e6 100%);
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1abc9c 0%, #16a085 100%);
    box-shadow: 4px 0 16px rgba(26, 188, 156, 0.2);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: white !important;
    animation: slideInLeft 0.6s ease-out;
}

.stButton > button {
    background: linear-gradient(90deg, #27ae60 0%, #229954 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(39, 174, 96, 0.3);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease-out;
}

.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(39, 174, 96, 0.5);
    animation: bounce 0.6s ease-in-out;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shine 3s infinite;
}

h1, h2, h3, h4 {
    color: #1abc9c !important;
    font-weight: 800 !important;
    animation: slideInLeft 0.6s ease-out;
}

.stMetric {
    background: rgba(26, 188, 156, 0.1);
    border-left: 5px solid #1abc9c;
    border-radius: 8px;
    padding: 16px;
    animation: fadeIn 0.7s ease-out;
}

.stInfo {
    background: rgba(26, 188, 156, 0.15) !important;
    border-left: 5px solid #1abc9c !important;
    border-radius: 8px !important;
    animation: slideInRight 0.6s ease-out;
}

.stSuccess {
    background: rgba(39, 174, 96, 0.15) !important;
    border-left: 5px solid #27ae60 !important;
    border-radius: 8px !important;
    animation: slideInRight 0.6s ease-out;
}

.stWarning {
    background: rgba(241, 196, 15, 0.15) !important;
    border-left: 5px solid #f39c12 !important;
    border-radius: 8px !important;
    animation: slideInRight 0.6s ease-out;
}

.stSelectbox, .stTextInput, .stNumberInput, .stFileUploader {
    border-radius: 8px !important;
    transition: all 0.3s ease;
}

.stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
    box-shadow: 0 6px 16px rgba(26, 188, 156, 0.2);
    transform: translateY(-2px);
}

/* Gamification elements */
.game-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 12px;
    margin: 4px;
    box-shadow: 0 4px 12px rgba(243, 156, 18, 0.3);
    animation: bounce 0.6s ease-in-out;
}

.star {
    display: inline-block;
    animation: pulse 1.5s ease-in-out infinite;
}

.progress-ring {
    animation: float 3s ease-in-out infinite;
}
</style>
""", height=0)

# --- Page Rendering Logic ---

if app_mode == t('home'):
    from features.stats_manager import StatsManager, format_badge_display
    
    # Initialize stats manager
    if 'stats_manager' not in st.session_state:
        st.session_state.stats_manager = StatsManager("farmer_default")
    
    stats_mgr = st.session_state.stats_manager
    user_profile = stats_mgr.get_user_profile()
    
    st.header("🌾 KRISHIMITRA - PLANT DISEASE RECOGNITION SYSTEM")
    
    if os.path.exists("home_page.jpeg"):
        st.image("home_page.jpeg", use_container_width=True)
    else:
        st.info("home_page.jpeg not found in this copy. Upload or place it next to main.py to display the homepage image.")
    
    st.markdown(t('welcome'))
    
    st.divider()
    
    # User Profile Section
    st.subheader("👨‍🌾 Your Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Predictions", user_profile['predictions_made'])
    with col2:
        st.metric("⭐ Points", user_profile['total_points'])
    with col3:
        st.metric("🔥 Streak", user_profile['current_streak'])
    with col4:
        st.metric("🏆 Badges", user_profile['badges_count'])
    
    # Display badges
    if user_profile['badges']:
        st.subheader("🏅 Your Badges")
        badge_cols = st.columns(4)
        for idx, badge in enumerate(user_profile['badges']):
            with badge_cols[idx % 4]:
                st.success(format_badge_display(badge))
    
    st.divider()
    
    # Leaderboard
    st.subheader("🏆 Top Farmers Leaderboard")
    leaderboard = stats_mgr.get_leaderboard(limit=10)
    
    if leaderboard:
        leaderboard_df = pd.DataFrame(leaderboard)
        st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
    else:
        st.info("Leaderboard will appear as farmers use the app.")

elif app_mode == "About":
    st.header("About KrishiMitra – CropScout AI-oT")
    st.markdown(
        """
        ### 🌾 Overview
        KrishiMitra helps farmers identify plant diseases from leaf images using a deep-learning model trained on the New Plant Diseases Dataset (Augmented). The app also includes live monitoring (ESP32‑CAM), marketplace tools, market prices, gamification, and multi‑language support.

        ---

        ### 🧠 How it works (high‑level)
        1. You upload a leaf image (or use the live camera feed)
        2. The image is resized to 128×128 and converted to an RGB array
        3. The model predicts probabilities across 38 disease classes
        4. The top results, confidence and treatment insights are shown

        Notes:
        - This model expects images in the 0‑255 pixel range (no /255 normalization)
        - Input shape: 128×128×3 (RGB)
        - Output classes: 38 plant diseases (see Disease Recognition for full list)

        ---

        ### 📚 Dataset
        - New Plant Diseases Dataset (Augmented)
        - ~87K RGB images across 38 classes
        - Train/Validation split preserved by folder structure

        Reference inspiration: animesh1012/machineLearning – Plant_Disease_Prediction

        ---

        ### ✨ App features
        - 🔍 Disease Recognition: AI predictions with confidence and top‑k results
        - 📡 Live Monitoring: ESP32‑CAM image feed (Supabase storage integration)
        - 💰 Market Prices: quick glance at current trends
        - 🛒 Marketplace: simple buyer/seller flow
        - 🌍 Multi‑language UI (English / Hindi / Kannada) + Read‑Aloud
        - 🎮 Gamification: points, streaks, badges, leaderboard

        ---

        ### ✅ Best practices for accurate results
        - Capture clear, well‑lit images of a single leaf
        - Keep the leaf centered with minimal background clutter
        - Avoid blur and strong shadows
        - Try multiple angles if the first result seems uncertain

        ---

        ### ⚠️ Responsible use
        - This tool supports decision‑making; always confirm with an agronomist when in doubt
        - Environmental conditions and look‑alike symptoms can affect results

        ---

        ### 🛠️ Tech stack
        - Streamlit UI, TensorFlow/Keras model
        - Firebase/JSON for stats, Supabase for ESP32‑CAM images
        - Python ecosystem: NumPy, Pillow, Pandas, Plotly

        ---

        ### 🙌 Credits & Acknowledgements
        - Dataset: New Plant Diseases Dataset (Augmented)
        - Community inspiration: animesh1012/machineLearning (Plant_Disease_Prediction)
        - Open‑source libraries and the Streamlit community

        ---

        ### 📞 Support
        - See the README for setup and troubleshooting
        - If predictions look off, ensure the trained model file is in place and that images are uploaded as clear 128×128 RGB crops (no manual normalization required)
        """
    )

elif app_mode == t('disease_recognition'):
    st.header(t('disease_recognition'))
    
    # Initialize stats manager
    if 'stats_manager' not in st.session_state:
        from features.stats_manager import StatsManager
        st.session_state.stats_manager = StatsManager("farmer_default")
    
    stats_mgr = st.session_state.stats_manager
    user_profile = stats_mgr.get_user_profile()
    
    # Gamification: Streak & Score tracking from persistent storage
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Predictions", user_profile['predictions_made'])
    with col2:
        st.metric("⭐ Points", user_profile['total_points'])
    with col3:
        st.metric("🔥 Streak", user_profile['current_streak'])
    with col4:
        st.metric("🏆 Badges", user_profile['badges_count'])
    
    st.divider()
    
    test_image = st.file_uploader(t('choose_image'))
    
    if test_image is not None:
        if st.button(t('show_image')):
            st.image(test_image, caption="Uploaded Image", use_container_width=True)
        
        if st.button(t('predict')):
            # Choose one celebration effect (alternating)
            import random
            if random.choice([True, False]):
                st.snow()  # Falling snow
            else:
                st.balloons()  # Balloons from bottom
            
            # Process image and get prediction
            image_bytes = test_image.getvalue()
            processed_image = preprocess_image(image_bytes)
            
            # Get raw predictions
            raw_predictions = model.predict(processed_image, verbose=0)
            result_index = np.argmax(raw_predictions[0])
            confidence = float(raw_predictions[0][result_index])
            
            # Debug output
            print(f"DEBUG: Predicted class index: {result_index}, Confidence: {confidence:.4f}")
            print(f"DEBUG: Top 3 predictions:")
            top3_idx = np.argsort(raw_predictions[0])[::-1][:3]
            for idx in top3_idx:
                print(f"  Class {idx}: {raw_predictions[0][idx]:.4f}")
            
            from data.class_names import CLASS_NAMES as class_name
            from data.disease_insights import get_disease_insight, format_disease_insight_for_display
            
            predicted_disease = class_name[result_index]
            
            # Update persistent stats with ACTUAL confidence
            updated_stats = stats_mgr.update_prediction(predicted_disease, confidence=confidence)
            user_profile = stats_mgr.get_user_profile()
            
            # Create celebration HTML
            celebration_html = f"""
            <div style="text-align: center; padding: 20px;">
                <h2 style="color: #27ae60; animation: bounce 0.6s ease-in-out;">✨ Analysis Complete! ✨</h2>
                <p style="font-size: 18px; color: #1abc9c;">+10 Points Earned!</p>
                <div style="margin: 20px 0;">
                    <span style="background: linear-gradient(135deg, #f39c12, #e74c3c); color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; display: inline-block;">
                        🎯 Prediction #{user_profile['predictions_made']}
                    </span>
                </div>
            </div>
            """
            components.html(celebration_html, height=120)
            
            # Display user stats after prediction
            st.markdown("---")
            st.subheader("📊 Your Updated Stats")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Total", user_profile['predictions_made'])
            with col2:
                st.metric("⭐ Points", user_profile['total_points'])
            with col3:
                st.metric("🔥 Streak", user_profile['current_streak'])
            with col4:
                st.metric("🏆 Badges", user_profile['badges_count'])
            
            # Check for new badges
            if len(updated_stats.get('badges', [])) > len(updated_stats.get('badges', [])):
                st.success("🎉 NEW BADGE UNLOCKED!")
            
            # Display detected disease
            st.markdown("---")
            prediction_text = f"🔍 **Detected:** {predicted_disease.replace('_', ' ')}"
            st.info(prediction_text)
            
            # Show confidence percentage
            st.metric("🎯 Confidence", f"{confidence*100:.1f}%")
            
            # Show top 3 predictions
            with st.expander("📊 Top 3 Predictions"):
                top3_idx = np.argsort(raw_predictions[0])[::-1][:3]
                for rank, idx in enumerate(top3_idx, 1):
                    disease_name = class_name[idx].replace('_', ' ')
                    conf_pct = raw_predictions[0][idx] * 100
                    st.write(f"{rank}. **{disease_name}** - {conf_pct:.1f}%")
                    st.progress(float(raw_predictions[0][idx]))
            
            # Get comprehensive disease insight
            st.markdown("---")
            insight = get_disease_insight(predicted_disease, lang)
            
            # Display severity and timeline
            col1, col2, col3 = st.columns(3)
            with col1:
                severity_colors = {"high": "🔴", "medium": "🟡", "low": "🟢", "unknown": "⚪"}
                severity_icon = severity_colors.get(insight.get('severity', 'unknown'), '⚪')
                st.metric(f"{severity_icon} Severity", insight.get('severity', 'unknown').upper())
            with col2:
                st.metric("⏱️ Cure Timeline", insight.get('cure_timeline', 'Consult expert'))
            with col3:
                st.metric("📋 Steps", f"{len(insight.get('steps_to_cure', []))} steps")
            
            st.markdown("---")
            
            # Disease Description
            st.subheader("📖 Understanding the Disease")
            desc = insight.get('description', {})
            if isinstance(desc, dict):
                st.write(desc.get(lang, desc.get('en', 'Information not available')))
            
            # Symptoms
            st.subheader("🔍 Key Symptoms to Watch")
            symptoms = insight.get('symptoms', {})
            if isinstance(symptoms, dict):
                st.write(symptoms.get(lang, symptoms.get('en', 'Information not available')))
            
            # Treatment Options
            st.subheader("💊 Treatment Options")
            
            # Chemical Treatments
            if insight.get('pesticides'):
                st.write("**🧪 Recommended Chemical/Pesticide Treatments:**")
                for i, pesticide in enumerate(insight['pesticides'], 1):
                    with st.expander(f"Option {i}: {pesticide['name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Dosage:** {pesticide.get('dosage', 'As per label')}")
                            st.write(f"**Cost:** {pesticide.get('cost_range', 'Variable')}")
                        with col2:
                            st.write(f"**Spray Interval:** {pesticide.get('spray_interval', 'As needed')}")
                        st.warning(f"⚠️ **Precautions:** {pesticide.get('precautions', 'Follow label instructions')}")
            else:
                st.info("Specific chemical treatments not yet documented. Please consult local expert.")
            
            st.divider()
            
            # Organic Treatment
            st.write("**🌱 Organic/Natural Treatment:**")
            organic = insight.get('organic_treatment', {})
            if isinstance(organic, dict):
                st.write(organic.get(lang, organic.get('en', 'Information not available')))
            else:
                st.write(organic if organic else "Information not available")
            
            st.divider()
            
            # Step-by-Step Cure Plan
            st.subheader("👨‍🌾 Step-by-Step Cure Plan")
            steps = insight.get('steps_to_cure', [])
            if steps:
                for step_info in steps:
                    with st.expander(f"Step {step_info['step']}: {step_info['action']}"):
                        st.write(step_info['details'])
            
            st.divider()
            
            # Prevention for future
            st.subheader("🛡️ Prevention Measures")
            prevention = insight.get('prevention', {})
            if isinstance(prevention, dict):
                st.write(prevention.get(lang, prevention.get('en', 'Information not available')))
            else:
                st.write(prevention if prevention else "Information not available")
            
            st.divider()
            
            # Get Help Section
            st.subheader("🆘 Need Expert Help?")
            help_info = insight.get('nearest_help', {})
            if isinstance(help_info, dict):
                help_text = help_info.get(lang, help_info.get('en', 'Contact your local agricultural office'))
            else:
                help_text = help_info if help_info else "Contact your local agricultural office"
            
            st.info(help_text)
            
            # Save this prediction
            if 'predictions_log' not in st.session_state:
                st.session_state.predictions_log = []
            st.session_state.predictions_log.append({
                'disease': predicted_disease,
                'timestamp': datetime.datetime.now(),
                'severity': insight.get('severity', 'unknown')
            })
            
            # Read Aloud for entire insight
            if st.button("🔊 " + t('read_aloud')):
                locale_map = {'en': 'en-US', 'hi': 'hi-IN', 'kn': 'kn-IN'}
                locale = locale_map.get(lang, 'en-US')
                
                # Prepare comprehensive text for reading
                read_parts = [
                    f"Disease: {predicted_disease.replace('_', ' ')}",
                    insight.get('description', {}).get(lang, insight.get('description', {}).get('en', '')),
                    f"Severity: {insight.get('severity', 'unknown')}",
                    f"Cure timeline: {insight.get('cure_timeline', 'unknown')}",
                    insight.get('symptoms', {}).get(lang, insight.get('symptoms', {}).get('en', ''))
                ]
                read_text = ". ".join(filter(None, read_parts))
                
                try:
                    # Use Web Speech API with better error handling
                    safe_text = json.dumps(read_text)
                    html_code = f"""
                    <script>
                    (function() {{
                        try {{
                            const text = {safe_text};
                            const utter = new SpeechSynthesisUtterance(text);
                            utter.lang = '{locale}';
                            utter.rate = 0.85;
                            utter.pitch = 1.0;
                            utter.volume = 1.0;
                            
                            // Cancel any ongoing speech
                            if (window.speechSynthesis.speaking) {{
                                window.speechSynthesis.cancel();
                            }}
                            
                            // Wait a bit then speak
                            setTimeout(() => {{
                                window.speechSynthesis.speak(utter);
                            }}, 100);
                        }} catch(e) {{
                            console.error('Speech error:', e);
                        }}
                    }})();
                    </script>
                    """
                    components.html(html_code, height=0)
                    st.success("🔊 Reading aloud... (Check your speakers!)")
                except Exception as e:
                    st.error(f"Read aloud error: {e}")

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

elif app_mode == 'Market Prices':
    st.header('Market Prices')
    st.markdown('Check today\'s market prices (sample data).')

    # Sample markets for South India regions
    sample_prices = [
        {'crop': 'Tomato', 'market': 'Bengaluru', 'price': 14.50},
        {'crop': 'Tomato', 'market': 'Mysuru', 'price': 13.75},
        {'crop': 'Potato', 'market': 'Coimbatore', 'price': 18.20},
        {'crop': 'Onion', 'market': 'Tiruchirapalli', 'price': 22.00},
    ]
    df = pd.DataFrame(sample_prices)
    st.dataframe(df)

    st.markdown('You can set simple alerts for a crop price target:')
    with st.form('price_alert'):
        crop = st.selectbox('Crop', df['crop'].unique())
        target = st.number_input('Target price (₹ per kg)', min_value=0.0, value=20.0)
        submit = st.form_submit_button('Set Alert')
        if submit:
            st.success(f'Alert set for {crop} at ₹{target:.2f} — (note: alerts are demo-only in this copy).')

elif app_mode == 'Marketplace':
    st.header('🌾 Zero-Fee Marketplace (Sellers & Buyers)')
    
    # Create two tabs: Sellers and Buyers
    tab1, tab2 = st.tabs(["👨‍🌾 Seller Listings", "🛒 Buyer Demands"])
    
    # ============ SELLER TAB ============
    with tab1:
        st.markdown('### 👨‍🌾 Sell Your Produce (Free - No Commission!)')
        st.markdown('Post what you have to sell. Buyers can find and contact you directly.')
        
        with st.expander('➕ Create a Seller Listing'):
            with st.form('seller_form'):
                st.write("**Your Contact Info**")
                seller_name = st.text_input('Your name', key='seller_name')
                seller_phone = st.text_input('Your phone number', key='seller_phone')
                
                st.write("**What You're Selling**")
                crop = st.text_input('Crop/Product (e.g., Tomato, Apple)', key='seller_crop')
                qty = st.number_input('Quantity (kg)', min_value=1, key='seller_qty')
                price = st.number_input('Asking price (₹ per kg)', min_value=0.0, format='%.2f', key='seller_price')
                region = st.text_input('Region (e.g., South India - Karnataka)', key='seller_region')
                description = st.text_area('Description (quality, variety, etc.)', key='seller_desc')
                
                post = st.form_submit_button('✅ Post Listing (FREE!)')
                if post and seller_name and seller_phone and crop and qty and price and region:
                    listing = {
                        'type': 'seller',
                        'seller_name': seller_name,
                        'seller_phone': seller_phone,
                        'crop': crop,
                        'qty': int(qty),
                        'price': float(price),
                        'region': region,
                        'description': description,
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    try:
                        db.collection('market_listings').add(listing)
                        st.success(f'✅ Your listing posted! Buyers can contact you at {seller_phone}')
                    except Exception as e:
                        st.info('Listing saved locally (demo mode)')
                        st.write(listing)
                elif post:
                    st.error('⚠️ Please fill all required fields!')
        
        st.markdown('---')
        st.markdown('### 📋 Current Seller Listings')
        try:
            docs = db.collection('market_listings').where('type', '==', 'seller').stream()
            listings = [d.to_dict() for d in docs]
            if listings:
                for i, listing in enumerate(listings):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{listing.get('crop', 'Product')}** - {listing.get('qty')}kg @ ₹{listing.get('price')}/kg")
                        st.write(f"📍 {listing.get('region', 'Unknown region')}")
                        st.write(f"**Seller:** {listing.get('seller_name', 'Unknown')} | **Phone:** {listing.get('seller_phone', 'N/A')}")
                        if listing.get('description'):
                            st.write(f"*{listing.get('description')}*")
                    with col2:
                        st.write(f"📅 {listing.get('timestamp', 'N/A')[:10]}")
                    st.divider()
            else:
                st.info('📭 No seller listings yet. Be the first to post!')
        except Exception as e:
            st.info('Listings unavailable (demo mode)')
    
    # ============ BUYER TAB ============
    with tab2:
        st.markdown('### 🛒 Post Your Demand (What You Want to Buy)')
        st.markdown('Tell sellers what you want and how much you\'re willing to pay. They can contact you!')
        
        with st.expander('➕ Create a Buyer Demand'):
            with st.form('buyer_form'):
                st.write("**Your Contact Info**")
                buyer_name = st.text_input('Your name', key='buyer_name')
                buyer_phone = st.text_input('Your phone number', key='buyer_phone')
                buyer_location = st.text_input('Your location', key='buyer_location')
                
                st.write("**What You Want to Buy**")
                wanted_crop = st.text_input('What crop/product do you want?', key='wanted_crop')
                wanted_qty = st.number_input('Quantity needed (kg)', min_value=1, key='wanted_qty')
                max_price = st.number_input('Maximum price you can pay (₹ per kg)', min_value=0.0, format='%.2f', key='max_price')
                
                st.write("**Additional Info**")
                quality_pref = st.selectbox('Quality preference', ['Any', 'Standard', 'Premium'], key='quality_pref')
                notes = st.text_area('Special requirements (variety, timing, etc.)', key='buyer_notes')
                
                post_demand = st.form_submit_button('✅ Post Your Demand (FREE!)')
                if post_demand and buyer_name and buyer_phone and buyer_location and wanted_crop and wanted_qty and max_price:
                    demand = {
                        'type': 'buyer',
                        'buyer_name': buyer_name,
                        'buyer_phone': buyer_phone,
                        'buyer_location': buyer_location,
                        'wanted_crop': wanted_crop,
                        'wanted_qty': int(wanted_qty),
                        'max_price': float(max_price),
                        'quality_pref': quality_pref,
                        'notes': notes,
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    try:
                        db.collection('market_listings').add(demand)
                        st.success(f'✅ Your demand posted! Farmers with {wanted_crop} can contact you at {buyer_phone}')
                    except Exception as e:
                        st.info('Demand saved locally (demo mode)')
                        st.write(demand)
                elif post_demand:
                    st.error('⚠️ Please fill all required fields!')
        
        st.markdown('---')
        st.markdown('### 📋 Current Buyer Demands')
        try:
            docs = db.collection('market_listings').where('type', '==', 'buyer').stream()
            demands = [d.to_dict() for d in docs]
            if demands:
                for i, demand in enumerate(demands):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Looking for:** {demand.get('wanted_crop', 'Product')} - {demand.get('wanted_qty')}kg")
                        st.write(f"**Willing to pay up to:** ₹{demand.get('max_price')}/kg | **Quality:** {demand.get('quality_pref', 'Any')}")
                        st.write(f"📍 **Buyer location:** {demand.get('buyer_location', 'Unknown')}")
                        st.write(f"**Buyer:** {demand.get('buyer_name', 'Unknown')} | **Phone:** {demand.get('buyer_phone', 'N/A')}")
                        if demand.get('notes'):
                            st.write(f"**Requirements:** *{demand.get('notes')}*")
                    with col2:
                        st.write(f"📅 {demand.get('timestamp', 'N/A')[:10]}")
                    st.divider()
            else:
                st.info('📭 No buyer demands yet. Post one to find sellers!')
        except Exception as e:
            st.info('Demands unavailable (demo mode)')
    
    st.markdown('---')
    st.markdown('### ℹ️ How It Works')
    st.markdown('''
    1. **Farmers/Sellers:** Post what you have to sell - completely FREE, no commission!
    2. **Buyers:** Post what you're looking for - specify quantity and price.
    3. **Direct Contact:** Buyers and sellers can see each other's phone numbers and contact directly.
    4. **Negotiate:** Agree on final price and quantity.
    5. **Direct Transaction:** No middleman, no fees, all profit to farmers!
    
    **Benefits:**
    - 🌾 Farmers get better prices (no middleman)
    - 💰 Buyers get better rates (direct from farm)
    - 📱 Easy communication with phone numbers
    - ✅ Completely FREE - zero commission
    - 🤝 Direct farmer-to-buyer relationships
    ''')
