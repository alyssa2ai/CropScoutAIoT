"""
Plant Disease Recognition App
Loads and displays predictions from your trained model
NO TWEAKS - JUST YOUR MODEL
"""

import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import io

# Page config
st.set_page_config(
    page_title="Plant Disease Recognition",
    page_icon="🌾",
    layout="wide"
)

# Load model (cached to run only once)
@st.cache_resource
def load_trained_model():
    """Load your trained model from disk"""
    model_path = "models/trained_model.h5"
    print(f"Loading model: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print(f"Model loaded! Classes: {model.output_shape[1]}")
    return model

# Load disease names
@st.cache_resource
def load_diseases():
    """Load disease class names"""
    try:
        from data.class_names import CLASS_NAMES
        return CLASS_NAMES
    except:
        return [f"Class {i}" for i in range(38)]

# Preprocess image
def prepare_image(image_input):
    """Prepare image for model prediction"""
    # Open image
    if isinstance(image_input, bytes):
        image = Image.open(io.BytesIO(image_input)).convert('RGB')
    else:
        image = image_input.convert('RGB')
    
    # Resize to 128x128
    image = image.resize((128, 128))
    
    # Convert to array
    image_array = np.array(image, dtype=np.float32)
    
    # Normalize to 0-1
    if np.max(image_array) > 1.0:
        image_array = image_array / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

# Main app
st.title("🌾 Plant Disease Recognition")
st.write("Upload a crop leaf image to detect diseases using your trained model")

# Load resources
model = load_trained_model()
diseases = load_diseases()

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image (JPG, PNG, BMP, WEBP)",
    type=["jpg", "jpeg", "png", "bmp", "webp"]
)

if uploaded_file:
    # Display two columns
    col1, col2 = st.columns(2)
    
    # Left column - image
    with col1:
        st.subheader("Image")
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, use_column_width=True)
    
    # Right column - prediction
    with col2:
        st.subheader("Prediction")
        
        # Prepare image
        processed = prepare_image(image)
        
        # Get prediction
        predictions = model.predict(processed, verbose=0)
        
        # Get top 5
        top_5_idx = np.argsort(predictions[0])[::-1][:5]
        
        # Display each prediction
        for rank, idx in enumerate(top_5_idx, 1):
            conf = predictions[0][idx]
            disease = diseases[idx].replace('_', ' ').replace('___', ' - ')
            
            col_text, col_bar = st.columns([2, 1])
            with col_text:
                st.write(f"**{rank}. {disease}**")
            with col_bar:
                st.progress(float(conf))
            st.write(f"Confidence: {conf*100:.1f}%")
            st.divider()

st.divider()
st.caption("Model: Your trained CNN | Classes: 38 diseases")
