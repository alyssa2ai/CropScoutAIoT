# streamlit_app.py - Dashboard Version with Multiple Pages
import streamlit as st
from supabase import create_client, Client
import time

# ----------------- SUPABASE CONFIG -----------------
SUPABASE_URL = "https://czctjuqudiutvofdgoqn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN6Y3RqdXF1ZGl1dHZvZmRnb3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExMjE3NzcsImV4cCI6MjA3NjY5Nzc3N30.AzHYtF5a8UrIz7JExKfBmMe7gJrJVysppToBAcL2T1g"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "leaf-images"

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="AgroIntelliSense Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- SIDEBAR NAVIGATION -----------------
st.sidebar.title("🌿 AgroIntelliSense")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Select Page",
    ["🏠 Home", "🔍 Disease Recognition", "📡 Live Monitoring", "💰 Market Prices", "🛒 Marketplace", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.info("ESP32-CAM Live Feed Integration")

# ----------------- HOME PAGE -----------------
if page == "🏠 Home":
    st.title("🌿 Welcome to AgroIntelliSense")
    
    st.markdown("""
    ### AI-Powered Plant Disease Recognition System
    
    Our system helps farmers identify plant diseases quickly and accurately using cutting-edge AI technology.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🔍 Disease Detection\nUpload leaf images for instant AI analysis")
    
    with col2:
        st.success("### 📡 Live Monitoring\nReal-time ESP32-CAM feed")
    
    with col3:
        st.warning("### 💰 Market Info\nLatest agricultural prices")
    
    st.markdown("---")
    
    st.subheader("🎯 How It Works")
    st.markdown("""
    1. **Upload** a plant leaf image or use live camera feed
    2. **Analyze** with our AI model trained on 87,000+ images
    3. **Detect** diseases from 38 different categories
    4. **Get** treatment recommendations instantly
    """)
    
    st.success("👈 Use the sidebar to navigate to different features!")

# ----------------- DISEASE RECOGNITION PAGE -----------------
elif page == "🔍 Disease Recognition":
    st.title("🔍 Plant Disease Recognition")
    
    st.info("⚠️ For full disease detection features, please use the main app: `streamlit run core/main.py`")
    
    st.markdown("""
    ### Available in Main App:
    - ✅ Upload and analyze plant leaf images
    - ✅ AI predictions with confidence scores
    - ✅ Top 3 disease predictions
    - ✅ Detailed treatment recommendations
    - ✅ Multi-language support (English, Hindi, Kannada)
    - ✅ Gamification (points, badges, streaks)
    
    ### Quick Access:
    ```bash
    streamlit run core/main.py
    ```
    """)
    
    st.warning("This dashboard focuses on live monitoring. Full disease recognition is in the main app.")

# ----------------- LIVE MONITORING PAGE -----------------
elif page == "📡 Live Monitoring":
    st.title("📡 Live Monitoring - ESP32-CAM Feed")
    
    st.info("This feed refreshes automatically every 5 seconds to show the latest leaf image uploaded by your ESP32-CAM.")
    
    # Add controls
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Latest Leaf Image")
    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Placeholder for the image
    image_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Auto-refresh loop
    refresh_count = 0
    max_refreshes = 60  # Stop after 60 refreshes (5 minutes)
    
    while refresh_count < max_refreshes:
        try:
            # List all files in the bucket
            files = supabase.storage.from_(BUCKET_NAME).list()
            
            if files:
                # Sort files by name (latest one last)
                latest_file = sorted(files, key=lambda x: x['name'], reverse=True)[0]['name']
                
                # Get public URL
                public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(latest_file)
                
                # Display image
                image_placeholder.image(public_url, caption=f"Latest Leaf: {latest_file}", use_column_width=True)
                
                status_placeholder.success(f"✅ Connected | Last update: {time.strftime('%H:%M:%S')}")
            else:
                image_placeholder.warning("📷 No images found in the bucket yet! Waiting for ESP32-CAM upload...")
                status_placeholder.info("Waiting for first image...")
        
        except Exception as e:
            image_placeholder.error(f"❌ Error fetching image: {e}")
            status_placeholder.error("Connection error")
        
        time.sleep(5)  # refresh every 5 seconds
        refresh_count += 1
    
    st.info("Auto-refresh stopped. Click 'Refresh Now' to continue.")

# ----------------- MARKET PRICES PAGE -----------------
elif page == "💰 Market Prices":
    st.title("💰 Market Prices")
    
    st.info("Real-time agricultural market prices")
    
    # Sample market data (you can replace with real API)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Today's Prices")
        st.metric("Wheat", "₹2,100/quintal", "+50")
        st.metric("Rice", "₹3,200/quintal", "-30")
        st.metric("Cotton", "₹6,500/quintal", "+150")
        st.metric("Sugarcane", "₹350/quintal", "+10")
    
    with col2:
        st.subheader("📈 Weekly Trends")
        st.info("Wheat: 📈 Rising")
        st.warning("Rice: 📉 Falling")
        st.success("Cotton: 🚀 Strong Growth")
        st.info("Sugarcane: ➡️ Stable")
    
    st.markdown("---")
    st.caption("💡 For detailed market analysis, use the main app: `streamlit run core/main.py`")

# ----------------- MARKETPLACE PAGE -----------------
elif page == "🛒 Marketplace":
    st.title("🛒 Agricultural Marketplace")
    
    st.info("Buy and sell agricultural products")
    
    tab1, tab2 = st.tabs(["🛍️ Browse Products", "📦 List Product"])
    
    with tab1:
        st.subheader("Available Products")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.image("https://via.placeholder.com/150", caption="Organic Fertilizer")
            st.write("**Price:** ₹500/bag")
            st.button("Contact Seller", key="prod1")
        
        with col2:
            st.image("https://via.placeholder.com/150", caption="Seeds")
            st.write("**Price:** ₹200/kg")
            st.button("Contact Seller", key="prod2")
        
        with col3:
            st.image("https://via.placeholder.com/150", caption="Pesticides")
            st.write("**Price:** ₹350/bottle")
            st.button("Contact Seller", key="prod3")
    
    with tab2:
        st.subheader("List Your Product")
        
        with st.form("list_product"):
            product_name = st.text_input("Product Name")
            product_price = st.number_input("Price (₹)", min_value=0)
            product_desc = st.text_area("Description")
            product_image = st.file_uploader("Upload Image")
            
            submitted = st.form_submit_button("List Product")
            if submitted:
                st.success("✅ Product listed successfully!")
    
    st.markdown("---")
    st.caption("💡 Full marketplace features available in main app: `streamlit run core/main.py`")

# ----------------- ABOUT PAGE -----------------
elif page == "ℹ️ About":
    st.title("ℹ️ About AgroIntelliSense")
    
    st.markdown("""
    ### 🌿 Plant Disease Recognition System
    
    **AgroIntelliSense** is an AI-powered platform designed to help farmers identify plant diseases 
    quickly and accurately using deep learning technology.
    
    ### 📊 Features:
    - 🔍 **Disease Detection** - Identifies 38 different plant diseases
    - 📡 **Live Monitoring** - ESP32-CAM integration for real-time monitoring
    - 💰 **Market Prices** - Real-time agricultural market information
    - 🛒 **Marketplace** - Buy and sell agricultural products
    - 🌍 **Multi-language** - English, Hindi, Kannada support
    
    ### 🧠 Technology:
    - Deep Learning CNN Model
    - Trained on 87,000+ images
    - 38 disease classifications
    - ESP32-CAM integration
    - Supabase cloud storage
    
    ### 🚀 Get Started:
    Use the sidebar to navigate through different features.
    
    For full features, run the main application:
    ```bash
    streamlit run core/main.py
    ```
    
    ---
    
    ### 📞 Support:
    - Check README.md for documentation
    - Repository: KrishiMitra by Alyssa-286
    """)

# ----------------- FOOTER -----------------
st.sidebar.markdown("---")
st.sidebar.caption("🌾 AgroIntelliSense | KrishiMitra Project")
st.sidebar.caption("Last Updated: Oct 22, 2025")
