"""
Simple Plant Disease Recognition App - Uses Your Trained Model
NO TWEAKS - Just loads your model and shows predictions
"""

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

# Configure Streamlit
st.set_page_config(page_title="Plant Disease Recognition", layout="wide")

# Load your trained model (32.44 MB - your actual model!)
@st.cache_resource
def load_model():
    model_path = "models/disease_cnn.keras"
    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print(f"Model loaded! Output classes: {model.output_shape[1]}")
    return model

# Load class names
@st.cache_resource
def load_class_names():
    try:
        from data.class_names import CLASS_NAMES
        return CLASS_NAMES
    except:
        # Fallback - create 38 dummy names
        return [f"Class_{i}" for i in range(38)]

# Preprocess image - SIMPLE AND DIRECT
def preprocess_image(image_file):
    """
    Preprocess image exactly as your model was trained
    Input: uploaded image file
    Output: (1, 128, 128, 3) array ready for prediction
    """
    # Open and resize
    image = Image.open(image_file).convert('RGB')
    image = image.resize((128, 128))
    
    # Convert to numpy array
    image_array = np.array(image, dtype=np.float32)
    
    # Normalize to 0-1 range (if not already done by Rescaling layer)
    if np.max(image_array) > 1.0:
        image_array = image_array / 255.0
    
    # Add batch dimension: (128, 128, 3) -> (1, 128, 128, 3)
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

# Main app
st.title("🌾 Plant Disease Recognition System")
st.subheader("Using Your Trained Model")

# Load resources
model = load_model()
class_names = load_class_names()

# Sidebar
st.sidebar.title("Instructions")
st.sidebar.info("""
1. Upload a crop/plant leaf image
2. Click "Predict"
3. View the disease prediction and confidence
""")

# Main interface
st.write("Upload a crop leaf image to identify diseases:")

uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "bmp", "webp"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    # Display uploaded image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Uploaded Image")
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, use_column_width=True)
    
    with col2:
        st.subheader("🧠 Model Prediction")
        
        # Preprocess
        processed_image = preprocess_image(uploaded_file)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get top predictions
        top_5_indices = np.argsort(predictions[0])[::-1][:5]
        
        # Display predictions
        st.write("**Top 5 Predictions:**")
        for rank, idx in enumerate(top_5_indices, 1):
            confidence = predictions[0][idx]
            disease_name = class_names[idx] if idx < len(class_names) else f"Class_{idx}"
            
            # Format disease name nicely
            disease_name = disease_name.replace('___', ' - ').replace('_', ' ')
            
            # Display with progress bar
            st.write(f"{rank}. **{disease_name}**")
            st.progress(float(confidence))
            st.write(f"   Confidence: {confidence*100:.2f}%")
        
        # Highlight top prediction
        top_idx = top_5_indices[0]
        top_confidence = predictions[0][top_idx]
        top_disease = class_names[top_idx] if top_idx < len(class_names) else f"Class_{top_idx}"
        top_disease = top_disease.replace('___', ' - ').replace('_', ' ')
        
        st.success(f"🎯 **Main Diagnosis: {top_disease}**")
        st.info(f"Confidence: {top_confidence*100:.1f}%")

st.divider()
st.caption("Plant Disease Recognition System | Your Trained Model")
