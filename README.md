# 🌾 CropScout AI - Plant Disease Recognition SystemKrishiMitra

**AI-Powered Disease Detection for Farmers | KrishiMitra Project**This repository contains the application source for the Plant Disease Recognition project. Large datasets, trained model binaries, virtual environments and credential files are intentionally excluded from this repo.

A comprehensive Streamlit web application that uses deep learning to identify **38 different plant diseases** from leaf images, with gamification features, marketplace, and multi-language support.Included files:

---- `app.py`

- `main.py`

## ✨ Features- `download_script.py`

- `test_api.py`

- 🔍 **Disease Recognition** - Upload plant images and get instant AI predictions- `requirements.txt`

- 🎯 **Gamification** - Earn points, badges, and track your progress - `.gitignore`

- 🛒 **Marketplace** - Buy/sell agricultural products

- 📊 **Live Monitoring** - Real-time crop health trackingExcluded (NOT in repo):

- 🌍 **Multi-language** - English, Hindi (हिंदी), Kannada (ಕನ್ನಡ)

- 🗣️ **Read Aloud** - Text-to-speech for disease information- `venv/`, `venv_tf/`

- 🔥 **Firebase Integration** - Cloud storage for user data- `New Plant Diseases Dataset(Augmented)/` (dataset and trained models)

- `firebase_credentials.json` (secrets)

---

To run locally:

## 🚀 Quick Start

1. Create a Python 3.11 virtualenv (recommended for TensorFlow compatibility).

### Run the App2. Activate venv and install dependencies: `python -m pip install -r requirements.txt`.

3. Run `streamlit run main.py` or `python app.py` for the Flask API.

```bash
# Activate venv
.\venv\Scripts\activate

# Run app
streamlit run core/main.py

# Open browser
http://localhost:8501
```

### Or use Python directly:

```bash
.\venv\Scripts\python.exe -m streamlit run core/main.py
```

---

## 📁 Project Structure

```
cropscoutaiot/
├── core/
│   ├── main.py              # Main Streamlit app
│   ├── model_handler.py     # Model utilities
│   └── app.py              # Flask API
├── data/
│   ├── class_names.py       # 38 disease names
│   └── disease_insights.py  # Treatment database
├── features/
│   └── stats_manager.py     # Gamification system
├── models/
│   └── trained_model.h5     # YOUR TRAINED MODEL (90 MB) ✅
├── requirements.txt
└── README.md
```

---

## 🧠 Your Trained Model

- **File:** `models/trained_model.h5`
- **Size:** 89.85 MB
- **Input:** 128×128 RGB images (0-255 range)
- **Output:** 38 disease classes
- **Status:** ✅ Working with 70-99% confidence!

### Supported Diseases (38 Classes)

**Apple:** Apple Scab, Black Rot, Cedar Apple Rust, Healthy

**Corn:** Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy

**Grape:** Black Rot, Esca, Leaf Blight, Healthy

**Tomato:** Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy

**Others:** Blueberry, Cherry, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry

---

## 🔧 How It Works

```
Upload Image → Resize to 128×128 → Convert to array (0-255)
    → Feed to CNN model → Get predictions → Display top 3 results
```

**⚠️ CRITICAL:** Model expects **NON-NORMALIZED** input (0-255 range, NOT 0-1)

---

## 🐛 Troubleshooting

### App won't start?

```bash
taskkill /F /IM python.exe /T
.\venv\Scripts\python.exe -m streamlit run core/main.py
```

### Model not found?

```bash
# Check if file exists (should be 90 MB)
ls models/trained_model.h5
```

### Wrong predictions?

- Ensure using `trained_model.h5` (NOT `disease_cnn.keras`)
- Upload clear images of diseased leaves
- Check debug output in terminal

---

## 📊 Key Fix Applied

### Problem Solved ✅

**Issue:** App predicted "Corn Northern Leaf Blight" for everything

**Root Cause:** Preprocessing was normalizing images (dividing by 255), but trained model expects 0-255 range

**Solution:** Removed normalization from `preprocess_image()` function

**Result:** Now getting accurate predictions with high confidence!

---

## 🎮 Features Overview

### Disease Recognition

- Upload crop leaf images
- Get instant AI predictions
- View top 3 likely diseases
- See confidence percentages
- Read treatment information

### Gamification

- **+10 points** per prediction
- Unlock badges for milestones
- Track daily streaks
- View leaderboard rankings

### Marketplace

- List agricultural products
- Browse items for sale
- Contact buyers/sellers

### Multi-Language

- English, Hindi, Kannada
- UI translations
- Read aloud in all languages

---

## 📦 Dependencies

Main requirements:

- `streamlit` - Web UI framework
- `tensorflow` - Deep learning
- `Pillow` - Image processing
- `numpy` - Arrays
- `firebase-admin` - Cloud storage

See `requirements.txt` for full list.

---

## 🚫 Not in Git Repository

These files are excluded (too large or sensitive):

- `venv/` - Virtual environment (recreate locally)
- `New Plant Diseases Dataset(Augmented)/` - Training data (87K images)
- `firebase_credentials.json` - Secrets

---

## 🎯 Usage Example

1. Run `streamlit run core/main.py`
2. Click "Disease Recognition" in sidebar
3. Upload crop leaf image
4. Click "Predict"
5. View disease, confidence, and treatments
6. Earn points and badges!

---

## 📞 Quick Reference

### Start App

```bash
.\venv\Scripts\python.exe -m streamlit run core/main.py
```

### Stop App

```bash
taskkill /F /IM python.exe /T
```

### Check Model

```bash
Get-Item models/trained_model.h5
```

---

## ✅ Status: WORKING!

- ✅ Model loading correctly
- ✅ Accurate predictions (70-99% confidence)
- ✅ Different images → Different results
- ✅ Multi-language support
- ✅ Gamification active
- ✅ Firebase integrated

---

## 🌟 Highlights

- **38 Plant Diseases** detected
- **3 Languages** supported
- **90 MB Trained Model** with high accuracy
- **Modern Web UI** with Streamlit
- **Gamification** to engage farmers
- **Cloud Storage** with Firebase

**Built for farmers to protect crops using AI!** 🌾

---

_KrishiMitra by Alyssa-286 | Last Updated: October 22, 2025_
