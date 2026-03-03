import streamlit as st
import joblib
import numpy as np

# HOSPITAL THEME CONFIG
st.set_page_config(page_title="🏥 Patient Vital Monitor", page_icon="🚨", layout="wide")

# PERFECT CSS - FORCING LAYOUT STABILITY
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Main background */
    .stApp { 
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); 
    }
    
    /* Target Streamlit's native containers to look like hospital cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, #1a1a2e, #16213e) !important;
        border-radius: 15px !important;
        border-left: 5px solid #00d4ff !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        padding: 20px !important;
        margin-bottom: 10px !important;
    }

    /* Global Text Color */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #ffffff !important;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Fixed Input Boxes */
    .stNumberInput input {
        background-color: #0f2027 !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #00d4ff, #0099cc) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 3em !important;
        width: 100% !important;
    }

    /* Emergency Flashing */
    .critical-box {
        background: linear-gradient(45deg, #ff1a1a, #ff4444) !important;
        border-left: 5px solid #ffffff !important;
        padding: 20px;
        border-radius: 15px;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,68,68,0.7); }
        70% { box-shadow: 0 0 0 20px rgba(255,68,68,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,68,68,0); }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    # Ensure these files are in your GitHub repo!
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

try:
    model, scaler = load_models()
except Exception as e:
    st.error("Model files not found. Please ensure model.pkl and scaler.pkl are in the repository.")

# HEADER
st.markdown("""
<div style='background: linear-gradient(145deg, #1a1a2e, #16213e); padding: 20px; border-radius: 15px; border-bottom: 4px solid #00d4ff; margin-bottom: 25px;'>
    <h1 style='text-align: center; margin: 0;'>🚨 PATIENT VITAL SIGNS MONITOR</h1>
    <p style='text-align: center; color: #00ff88; margin: 5px 0 0 0;'>AI Emergency Detection System • Hospital Grade</p>
</div>
""", unsafe_allow_html=True)

# INPUTS - ORGANIZED IN NATIVE CONTAINERS FOR ALIGNMENT
st.markdown("<h2 style='text-align: center;'>📊 Clinical Vital Input</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("💓 Cardiovascular")
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=0.0, value=72.0, key="hr")
        systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=0.0, value=120.0, key="sbp")
        diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=0.0, value=80.0, key="dbp")

with col2:
    with st.container(border=True):
        st.subheader("🫁 Respiratory & Temp")
        respiratory_rate = st.number_input("Resp Rate (br/min)", min_value=0.0, value=16.0, key="rr")
        oxygen_saturation = st.number_input("O₂ Sat (%)", min_value=0.0, value=98.0, key="o2")
        body_temperature = st.number_input("Body Temp (°C)", min_value=20.0, value=36.8, key="temp")

# MAP Calculation (Usually required by medical models)
mean_arterial_pressure = (systolic_bp + (2 * diastolic_bp)) / 3

st.markdown("<br>", unsafe_allow_html=True)

# EMERGENCY SCAN
if st.button("🚨 RUN EMERGENCY AI DIAGNOSIS"):
    
    with st.spinner("🔬 Analyzing Physiological Patterns..."):
        # Prepare data for model
        raw_features = np.array([[heart_rate, respiratory_rate, systolic_bp, diastolic_bp, 
                                 mean_arterial_pressure, oxygen_saturation, body_temperature]])
        scaled_features = scaler.transform(raw_features)
        prediction = model.predict(scaled_features)[0]
    
    st.markdown("---")
    
    if prediction == -1:
        # CRITICAL ALERT
        st.markdown("""
        <div class='critical-box'>
            <h1 style='text-align: center; color: white; margin: 0;'>🚨 CODE BLUE: CRITICAL</h1>
            <p style='text-align: center; color: #ffff00; font-weight: bold;'>IMMEDIATE CLINICAL INTERVENTION REQUIRED</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Breakdown of critical values
        c1, c2 = st.columns(2)
        with c1:
            if heart_rate > 120 or heart_rate < 50: st.error(f"Heart Rate: {heart_rate} BPM")
            if oxygen_saturation < 92: st.error(f"Low Oxygen: {oxygen_saturation}%")
        with c2:
            if systolic_bp > 160 or systolic_bp < 90: st.error(f"Critical BP: {systolic_bp}/{diastolic_bp}")
            if body_temperature > 39: st.error(f"High Fever: {body_temperature}°C")
    else:
        st.markdown("""
        <div style='background: #00b140; padding: 20px; border-radius: 15px; text-align: center;'>
            <h1 style='color: white; margin: 0;'>✅ PATIENT STABLE</h1>
            <p style='color: white; margin: 0;'>Vitals are within acceptable clinical range.</p>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("<br><p style='text-align: center; color: #666;'>Hospital Emergency Monitor v2.1 • Streamlit Cloud Optimized</p>", unsafe_allow_html=True)