# 🌾 KrishiMitra - AI-Powered Smart Farming Platform

**End-to-End AIoT Solution for Precision Agriculture**

An intelligent agricultural IoT system combining mobile hardware sensing with AI-powered disease recognition. This platform enables farmers to scout fields with a robotic rover equipped with ESP32-CAM and environmental sensors, streaming live data to a cloud-based Streamlit dashboard for real-time crop health analysis.

---

## 🤖 Hardware Components (AIoT System)

- **📷 ESP32-CAM** - Captures live leaf images and streams to cloud (Supabase)
- **🚗 Bluetooth Rover** - Mobile platform for field navigation
- **🌡️ Temperature Sensor** - Monitors field temperature
- **💨 Gas Sensor** - Detects air quality and gas emissions
- **💧 Soil Moisture Sensor** - Measures soil water content
- **⚗️ pH Sensor** - Tests soil acidity levels

All hardware code included in `/pdarduinocode/` and `/bluetooth/` directories.

---

## ✨ Software Features

- 🔍 **AI Disease Recognition** - Identifies 38 plant diseases from leaf images using CNN
- 📡 **Live Monitoring** - Real-time ESP32-CAM video feed with auto-refresh
- 🌡️ **Multi-Sensor Dashboard** - Gas, temperature, soil moisture, pH readings
- 🎯 **Gamification** - Points, badges, and achievement tracking
- 🛒 **Marketplace** - Buy/sell agricultural products
- 🌍 **Multi-language** - English, Hindi (हिंदी), Kannada (ಕನ್ನಡ)
- 🗣️ **Read Aloud** - Text-to-speech for disease information
- 🔥 **Cloud Integration** - Firebase (user stats) + Supabase (images)
- 📊 **Real-time Analytics** - Track predictions, confidence levels, and field history

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (recommended for TensorFlow compatibility)
- ESP32-CAM module (optional, for live monitoring)
- Firebase and Supabase accounts (for cloud features)

### Installation & Setup

```bash
# Clone repository
git clone https://github.com/Alyssa-286/KrishiMitra.git
cd KrishiMitra

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run core/main.py

# Or use Python directly
.\venv\Scripts\python.exe -m streamlit run core/main.py

# Open browser at http://localhost:8501
```

### Hardware Setup (Optional)

1. Upload `/pdarduinocode/pdarduinocode.ino` to ESP32-CAM
2. Configure WiFi credentials in Arduino code
3. Set Supabase bucket URL in `streamlit_app.py`
4. Upload `/bluetooth/bluetooth.ino` to rover Arduino
5. Connect sensors (gas, temp, soil, pH) as per wiring diagram

---

## 📁 Project Structure

```
cropscoutaiot/
├── core/
│   ├── main.py              # Main Streamlit app (6 pages)
│   ├── model_handler.py     # Model loading utilities
│   └── app.py               # Flask API (optional)
├── data/
│   ├── class_names.py       # 38 disease class names
│   └── disease_insights.py  # Treatment recommendations DB
├── features/
│   └── stats_manager.py     # Gamification system (Firebase)
├── models/
│   └── trained_model.h5     # Trained CNN model (90 MB)
├── pdarduinocode/
│   ├── pdarduinocode.ino    # ESP32-CAM main code
│   ├── app_httpd.cpp        # HTTP streaming server
│   └── camera_pins.h        # Pin configurations
├── bluetooth/
│   ├── bluetooth.ino        # Rover control code
│   └── SENSORSONBB.ino      # Multi-sensor integration
├── streamlit_app.py         # Dashboard with live feed
├── requirements.txt
└── README.md
```

---

## 🧠 AI Disease Recognition Model

### Model Specifications

- **File:** `models/trained_model.h5`
- **Architecture:** Convolutional Neural Network (CNN) - 14 layers
- **Size:** 89.85 MB
- **Training Dataset:** New Plant Diseases Dataset (Augmented) - 87,000+ images
- **Input:** 128×128 RGB images (0-255 pixel range)
- **Output:** 38 disease classes with confidence scores
- **Performance:** ✅ 70-99% confidence on real-world images
- **Critical Note:** Model expects NON-NORMALIZED input (0-255 range, NOT 0-1)

### Supported Diseases (38 Classes)

**Apple (4):** Scab, Black Rot, Cedar Apple Rust, Healthy

**Corn (4):** Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy

**Grape (4):** Black Rot, Esca, Leaf Blight, Healthy

**Tomato (10):** Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy

**Others (16):** Blueberry, Cherry, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry (+ their diseases)

---

## 🔧 System Workflow

### Hardware → Cloud → AI Pipeline

```
ESP32-CAM (Rover) → Capture Leaf Image → Upload to Supabase
    ↓
Streamlit Dashboard → Retrieve Image → Preprocess (Resize 128×128)
    ↓
TensorFlow CNN Model → Predict Disease (38 classes)
    ↓
Display Results → Show Confidence + Treatment + Multi-language
    ↓
Firebase → Save Stats (Points, Badges, History)
```

### Sensor Data Flow

```
Gas/Temp/Soil/pH Sensors → Arduino → Bluetooth → Mobile/Dashboard
    ↓
Real-time Monitoring → Alerts & Analytics
```

**⚠️ CRITICAL:** Model expects **NON-NORMALIZED** input (0-255 range, NOT 0-1)

---

## 🐛 Troubleshooting

### App won't start?

```bash
# Kill existing Python processes
taskkill /F /IM python.exe /T

# Restart app
.\venv\Scripts\python.exe -m streamlit run core/main.py
```

### ESP32-CAM not connecting?

- Check WiFi credentials in `pdarduinocode.ino`
- Verify Supabase bucket URL and API keys
- Ensure ESP32-CAM has stable power supply (5V/2A recommended)

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

### 1. Disease Recognition

- Upload leaf images from gallery or ESP32-CAM
- AI analyzes image using CNN (128×128 input)
- Top 3 disease predictions with confidence scores
- Detailed treatment recommendations
- Multi-language explanations

### 2. Live Monitoring Dashboard

- Real-time ESP32-CAM video feed (auto-refresh every 5 seconds)
- Gas, temperature, soil moisture, pH sensor readings
- Historical data visualization
- Alert system for abnormal readings

### 3. Gamification System

- **+10 points** per prediction
- Unlock badges for milestones (Beginner, Explorer, Expert, etc.)
- Track daily/weekly streaks
- Leaderboard with rankings
- Firebase cloud sync

### 4. Marketplace

- List agricultural products (seeds, equipment, produce)
- Browse buyer/seller listings
- Contact system for transactions
- Community-driven pricing

### 5. Multi-Language Support

- UI: English, Hindi (हिंदी), Kannada (ಕನ್ನಡ)
- Text-to-speech for accessibility
- Localized disease information

---

## 🛠️ Tech Stack

### Hardware

- **ESP32-CAM** - Image capture (OV2640 2MP camera)
- **Arduino Uno/Nano** - Sensor interfacing
- **HC-05/HC-06** - Bluetooth communication
- **Gas Sensor (MQ-135)** - Air quality monitoring
- **DHT22** - Temperature & humidity
- **Soil Moisture Sensor** - Capacitive/resistive
- **pH Sensor** - Analog pH measurement

### Software

- **Frontend:** Streamlit (Python 3.11+)
- **AI/ML:** TensorFlow 2.16, Keras, NumPy
- **Cloud:** Firebase (Firestore), Supabase (Storage)
- **Image Processing:** Pillow, OpenCV
- **Languages:** gTTS (text-to-speech)
- **Database:** JSON fallback for offline mode

---

## 📦 Dependencies

**Core Libraries:**

```txt
streamlit==1.31.0
tensorflow==2.16.1
Pillow==10.2.0
numpy==1.26.4
firebase-admin==6.4.0
supabase==2.3.4
gTTS==2.5.0
opencv-python==4.9.0.80
```

See [requirements.txt](requirements.txt) for complete list.

---

## � Usage Guide

### For Farmers (Field Use)

1. **Power on Rover**: Connect battery to ESP32-CAM and Arduino
2. **Navigate Field**: Use Bluetooth app to control rover
3. **Position Camera**: Align ESP32-CAM with diseased leaf
4. **Capture Image**: Image auto-uploads to Supabase every 5 seconds
5. **Check Dashboard**: Open Streamlit app to view live feed
6. **Analyze Disease**: Click on captured image to get AI prediction
7. **Follow Treatment**: Read recommendations in your language
8. **Monitor Sensors**: Track gas, temp, soil, pH in real-time

### For Web Dashboard

1. Run `streamlit run core/main.py`
2. Select page from sidebar:
   - **Home**: Overview and quick stats
   - **Disease Recognition**: Upload images for analysis
   - **Live Monitoring**: ESP32-CAM feed + sensor data
   - **Market Prices**: Agricultural commodity prices
   - **Marketplace**: Buy/sell products
   - **About**: Project documentation
3. Upload image or select from ESP32-CAM feed
4. Click "Predict Disease"
5. View results: Top 3 predictions with confidence
6. Read treatment in English/Hindi/Kannada
7. Earn +10 points and track badges

---

## 🚫 Not in Git Repository

These files are excluded (too large or contain secrets):

- `venv/`, `venv_tf/` - Virtual environments (recreate with `python -m venv venv`)
- `New Plant Diseases Dataset(Augmented)/` - 87K training images (download separately)
- `firebase_credentials.json` - Firebase service account key (add your own)
- `models/trained_model.h5` - 90MB model file (upload to GitHub LFS or download from release)

---

## 📞 Quick Commands

### Start App

```bash
.\venv\Scripts\python.exe -m streamlit run core/main.py
```

### Stop App

````bash
```bash
taskkill /F /IM python.exe /T
````

### Upload Arduino Code

```bash
# Install Arduino CLI (first time only)
# Then upload ESP32-CAM code:
arduino-cli upload -p COM3 --fqbn esp32:esp32:esp32cam pdarduinocode/

# Upload rover code:
arduino-cli upload -p COM4 --fqbn arduino:avr:uno bluetooth/
```

### Check Model

```powershell
Get-Item models/trained_model.h5 | Select-Object Name, Length
```

### Test ESP32-CAM

```bash
# Check if ESP32-CAM is streaming
curl http://<ESP32-CAM-IP>/capture

# View Supabase bucket
# Visit: https://supabase.com/dashboard/project/<project-id>/storage/buckets
```

---

## ✅ Project Status

### Completed Features ✅

- ✅ AI disease recognition (38 classes, 70-99% accuracy)
- ✅ ESP32-CAM integration with live streaming
- ✅ Multi-sensor data collection (gas, temp, soil, pH)
- ✅ Bluetooth rover control
- ✅ Gamification system (points, badges, streaks)
- ✅ Multi-language UI (English, Hindi, Kannada)
- ✅ Firebase + Supabase cloud integration
- ✅ Marketplace for agricultural products
- ✅ Text-to-speech accessibility
- ✅ Real-time dashboard with auto-refresh

### Known Issues 🐛

- Model file (90MB) not in repository - download from [Releases](../../releases)
- Firebase credentials required for cloud features
- ESP32-CAM requires 5V/2A power supply (USB may not suffice)

### Roadmap 🚀

- [ ] Mobile app (React Native)
- [ ] Automated rover navigation with GPS
- [ ] Weather API integration
- [ ] Crop yield prediction model
- [ ] Multi-farm management dashboard
- [ ] Offline mode with local database

---

## 📄 License & Credits

**Dataset:** New Plant Diseases Dataset (Augmented) from [Kaggle](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

**Framework:** Built with Streamlit, TensorFlow, Firebase, Supabase

**Contributors:** Alyssa-286 (Project Lead)

**License:** MIT (See LICENSE file)

---

## 🤝 Contributing

Pull requests welcome! For major changes:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📧 Support

For issues or questions:

- **GitHub Issues**: https://github.com/Alyssa-286/KrishiMitra/issues
- **Email**: [Contact through GitHub profile]

---

**⭐ If this project helps you, please give it a star on GitHub!**

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
